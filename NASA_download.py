#ASTR 302 downloading NASA asteroid data
import sys
print(sys.executable)
import requests
import datetime
import json

requests.get("GET https://ssd-api.jpl.nasa.gov/sentry.api

")



response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    with open('NASA_download.csv', 'w') as f:
        json.dump(data, f, indent=4)
    print("Data saved!")
else:
    print("Failed. {response.status_code}")

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"data_{timestamp}.json"
