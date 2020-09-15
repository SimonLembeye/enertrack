import datetime
import json
from django.shortcuts import render
from pytz import timezone

from enertrack.models import Forecast


def index(request):
    paris = timezone("Europe/Amsterdam")
    today = datetime.datetime.now(paris)

    print(today.year, today.month, today.hour)

    solar_forecast_q = Forecast.objects.filter(start_date__day=(today.day+1), start_date__month=today.month,
                                              start_date__year=today.year, forecast_production_type="SOLAR",
                                              type="D-1")

    wind_forecast_q = Forecast.objects.filter(start_date__day=(today.day+1), start_date__month=today.month,
                                              start_date__year=today.year, forecast_production_type="WIND",
                                              type="D-1")

    labels = [f"{h}h" for h in range(24)]
    solar_values = [0 for _ in range(24)]
    wind_values = [0 for _ in range(24)]
    sum_values = [0 for _ in range(24)]

    for forecast in solar_forecast_q:
        solar_values[forecast.start_date.hour] = forecast.value / 1000
        sum_values[forecast.start_date.hour] += forecast.value / 1000

    for forecast in wind_forecast_q:
        wind_values[forecast.start_date.hour] = forecast.value / 1000
        sum_values[forecast.start_date.hour] += forecast.value / 1000


    data = {
        "values": {
            "solar": solar_values,
            "wind": wind_values,
            "sum": sum_values,
        },
        "labels": labels,
    }

    context = {'chart_data': json.dumps(data)}
    return render(request, "enertrack/home.html", context)
