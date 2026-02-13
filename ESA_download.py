#ASTR 302 downloading ESA asteroid data (Slow)
import sys; print(sys.executable)
import requests
import datetime
import json

url = "https://neo.ssa.esa.int/PSDB-portlet/download?file=esa_risk_list"
response = requests.get(url)

if response.status_code == 200:
    with open('ESA_download.txt', 'wb') as f:
        f.write(response.content)
    print("ESA NEO list downloaded successfully!")
else:
    print(f"Failed to download. Status code: {response.status_code}")

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"data_{timestamp}.json"
