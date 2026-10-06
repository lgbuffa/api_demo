import json
import requests

URL = "http://137.131.185.161:8102/machine-alarms"

headers = {"Authorization": "Bearer x"}

response = requests.get(URL, headers=headers, timeout=10)
response.raise_for_status()
data = response.json()

alarms = response.json()["data"]

print(json.dumps(data, indent=2))
