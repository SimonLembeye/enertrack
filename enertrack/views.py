import datetime
import json
from django.shortcuts import render
from pytz import timezone

from enertrack.utils import get_forecasts


def index(request):
    paris = timezone("Europe/Amsterdam")
    today = datetime.datetime.now(paris)
    tmw = today + datetime.timedelta(days=1)

    today_data = get_forecasts(today, country_code="FR")
    tmw_data = get_forecasts(tmw, country_code="FR")

    data = {
        "today_data": today_data,
        "tmw_data": tmw_data,
    }

    dates = {
        "today": today,
        "tmw": tmw,
    }

    context = {"chart_data": json.dumps(data), "dates": dates}
    return render(request, "enertrack/home.html", context)
