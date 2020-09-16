from enertrack.models import Forecast


def get_forecasts(date, country_code="FR"):

    forecast_q = Forecast.objects.filter(
        start_date__day=date.day,
        start_date__month=date.month,
        start_date__year=date.year,
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
        h_solar_q = solar_q.filter(start_date__hour=h).order_by("-updated_date")
        if h_solar_q.exists():
            h_solar_forecast = h_solar_q.first()
            solar_values[h] = h_solar_forecast.value / 1000
            sum_values[h] += h_solar_forecast.value / 1000

        h_wind_q = wind_q.filter(start_date__hour=h).order_by("-updated_date")
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