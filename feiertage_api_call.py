import requests
import json

jahre = [2017, 2018, 2019] 
api_url = "https://feiertage-api.de/api/"
datumsangaben = []

for jahr in jahre:
    response = requests.get(api_url, params={"jahr": jahr, "nur_land": "NW"})
    feiertage = response.json()
    
    for details in feiertage.values():
        datumsangaben.append(details["datum"])

gefilterte_daten = {"Feiertage": datumsangaben}
dateiname = 'Feiertage.json'

with open(dateiname, 'w') as file:
    json.dump(gefilterte_daten, file, indent=4)