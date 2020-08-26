import json
import requests
import environ

def get_rte_access_token():

    env = environ.Env()
    rte_token = env("RTE_TOKEN")

    url = "https://digital.iservices.rte-france.com/token/oauth/"
    headers = {
        "Authorization": f"Basic {rte_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post(url, headers=headers)
    data = json.loads(r.text)
    token = data["access_token"]
    return token
