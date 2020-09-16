import datetime

import pytz
from pytz import timezone
from enertrack.models import Forecast


def get_forecasts(date, country_code="FR"):

    if country_code == "FR":
        paris = timezone("Europe/Paris")
        ub_date = datetime.datetime(date.year, date.month, date.day + 1, 0, 0, 0, 0)
        ub_date = paris.localize(ub_date)
        lb_date = datetime.datetime(date.year, date.month, date.day)
        lb_date = paris.localize(lb_date)

    forecast_q = Forecast.objects.filter(
        start_date__gte=lb_date,
        start_date__lte=ub_date,
        country__code=country_code,
    )

    if not forecast_q.exists():
        return {"data_available": False}

    labels = [f"{h}h" for h in range(24)]
    solar_values = [0 for _ in range(24)]
    wind_values = [0 for _ in range(24)]
    sum_values = [0 for _ in range(24)]

    solar_q = forecast_q.filter(forecast_production_type="SOLAR")
    wind_q = forecast_q.filter(forecast_production_type="WIND")

    for h in range(24):
        date = (lb_date + datetime.timedelta(hours=h))
        print(date)

        h_solar_q = solar_q.filter(start_date=date).order_by("-updated_date")
        if h_solar_q.exists():
            h_solar_forecast = h_solar_q.first()
            solar_values[h] = h_solar_forecast.value / 1000
            sum_values[h] += h_solar_forecast.value / 1000

        h_wind_q = wind_q.filter(start_date=date).order_by("-updated_date")
        if h_wind_q.exists():
            h_wind_forecast = h_wind_q.first()
            wind_values[h] = h_wind_forecast.value / 1000
            sum_values[h] += h_wind_forecast.value / 1000

    return {
        "data_available": True,
        "values": {
            "solar": solar_values,
            "wind": wind_values,
            "sum": sum_values,
        },
        "labels": labels,
    }
