import json
import requests
import datetime
from django.core.management import BaseCommand
from enertrack.api_utils import get_rte_access_token
from enertrack.models import Country, Measure


class Command(BaseCommand):
    help = "Get French current production form RTE API"

    def handle(self, *args, **options):

        rte_access_token = get_rte_access_token()
        france = Country.objects.filter(code="FR").first()

        url = f"https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_production_type"

        params = {}
        headers = {"Authorization": f"Bearer {rte_access_token}"}
        r = requests.get(url, params=params, headers=headers)
        data = json.loads(r.text)["actual_generations_per_production_type"]

        for prod in data:
            if prod["production_type"] in ["SOLAR", "WIND_OFFSHORE", "WIND_ONSHORE"]:
                for element in prod["values"]:

                    start_date = datetime.datetime.fromisoformat(element["start_date"])
                    updated_date = datetime.datetime.fromisoformat(
                        element["updated_date"]
                    )


                    measure = Measure.objects.update_or_create(
                        country=france,
                        production_type=prod["production_type"],
                        start_date=start_date,
                        updated_date=updated_date,
                        value=element["value"],
                    )

                    print("measure saved !")
