import json
import requests
import datetime
from django.core.management import BaseCommand
from enertrack.api_utils import get_rte_access_token
from enertrack.models import Country, Forecast


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):

        rte_access_token = get_rte_access_token()

        now = datetime.datetime.now()

        france = Country.objects.filter(code="FR").first()

        url = f"https://digital.iservices.rte-france.com/open_api/generation_forecast/v2/forecasts"
        params = {
            "production_type": "WIND",
        }
        headers = {"Authorization": f"Bearer {rte_access_token}"}
        r = requests.get(url, params=params, headers=headers)
        data = json.loads(r.text)["forecasts"]

        for predictions in data:
            print()

            type = predictions["type"]
            production_type = predictions["production_type"]

            print("#################", type, production_type)

            for element in predictions["values"]:
                start_date = datetime.datetime.fromisoformat(element["start_date"])
                updated_date = datetime.datetime.fromisoformat(element["updated_date"])

                value = int(element["value"] * 100)

                forecast_q = Forecast.objects.filter(
                    country=france,
                    forecast_production_type=production_type,
                    type=type,
                    start_date=start_date,
                )

                if (
                    forecast_q.exists()
                    and forecast_q.first().updated_date >= updated_date
                ):
                    print("already seen ...")
                    continue

                forecast = Forecast.objects.update_or_create(
                    country=france,
                    forecast_production_type=production_type,
                    type=type,
                    start_date=start_date,
                    updated_date=updated_date,
                    value=value,
                )

                print("forecast saved !")
