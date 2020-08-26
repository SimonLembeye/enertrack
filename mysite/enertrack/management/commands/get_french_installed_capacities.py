import json
import datetime
import requests
from django.core.management.base import BaseCommand
from enertrack.api_utils import get_rte_access_token
from enertrack.models import InstalledCapacity, Country

PRODUCTION_TYPES = [
    "FOSSIL_GAS",
    "FOSSIL_HARD_COAL",
    "HYDRO_PUMPED_STORAGE",
    "NUCLEAR",
    "SOLAR",
    "WIND_OFFSHORE",
    "WIND_ONSHORE",
]


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        rte_access_token = get_rte_access_token()

        now = datetime.datetime.now()
        year = now.year + 1

        france = Country.objects.filter(code="FR").first()

        for production_type in PRODUCTION_TYPES:

            url = (
                f"https://digital.iservices.rte-france.com/"
                f"open_api/generation_installed_capacities/v1/capacities_per_production_type"
            )
            params = {
                "production_type": production_type,
                "start_date": "2015-01-01T00:00:00+01:00",
                "end_date": f"{year}-01-01T00:00:00+01:00",
            }
            headers = {"Authorization": f"Bearer {rte_access_token}"}
            r = requests.get(url, params=params, headers=headers)
            data = json.loads(r.text)["capacities_per_production_type"]["values"]
            for element in data:
                date = datetime.datetime.strptime(
                    element["start_date"].split("T")[0], "%Y-%m-%d"
                )
                production_type = element["type"]
                value = (
                    int(element["value"]) * 1000
                )  # we want capacities to be expressed in kW
                if not InstalledCapacity.objects.filter(
                    country=france, date=date, production_type=production_type
                ).exists():
                    installed_capacity = InstalledCapacity.objects.create(
                        country=france,
                        date=date,
                        production_type=production_type,
                        value=value,
                    )
                    print("Creation success !")
                else:
                    print("Already done")

            print(data)
