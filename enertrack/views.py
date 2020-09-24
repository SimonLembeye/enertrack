import datetime
import json
from django.shortcuts import render
from pytz import timezone

from enertrack.models import Measure, InstalledCapacity
from enertrack.utils import get_forecasts


def index(request):
    paris = timezone("Europe/Amsterdam")
    today = datetime.datetime.now(paris)
    tmw = today + datetime.timedelta(days=1)

    today_data = get_forecasts(today, country_code="FR")
    tmw_data = get_forecasts(tmw, country_code="FR")

    charts_data = {
        "today_data": today_data,
        "tmw_data": tmw_data,
    }

    dates = {
        "today": today,
        "tmw": tmw,
    }

    solar_last_production = (
        Measure.objects.filter(production_type="SOLAR")
        .order_by("-start_date", "-updated_date")
        .first()
        .value
        / 1000
    )
    wind_last_production = (
        Measure.objects.filter(production_type="WIND_ONSHORE")
        .order_by("-start_date", "-updated_date")
        .first()
        .value
        / 1000
    )

    solar_installed_capacities = (
        InstalledCapacity.objects.filter(production_type="SOLAR")
        .order_by("-date")
        .first()
        .value
        / 1000000
    )
    wind_installed_capacities = (
        InstalledCapacity.objects.filter(production_type="WIND_ONSHORE")
        .order_by("-date")
        .first()
        .value
        / 1000000
    )

    prod_data = {
        "solar_last_production": round(solar_last_production, 2),
        "wind_last_production": round(wind_last_production, 2),
        "solar_load_factor": round(
            100 * solar_last_production / solar_installed_capacities, 2
        ),
        "wind_load_factor": round(
            100 * wind_last_production / wind_installed_capacities, 2
        ),
        "solar_installed_capacities": solar_installed_capacities,
        "wind_installed_capacities": wind_installed_capacities,
    }

    context = {
        "chart_data": json.dumps(charts_data),
        "dates": dates,
        "prod_data": prod_data,
        "prod_data_json": json.dumps(prod_data),
    }
    return render(request, "enertrack/home.html", context)
