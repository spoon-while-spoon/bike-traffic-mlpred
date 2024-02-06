import requests
import json

with open('config.json', 'r') as file:
    config = json.load(file)
jahre = config['jahre']

api_url_feiert = "https://feiertage-api.de/api/"
api_url_ferien = "https://ferien-api.maxleistner.de/api/v1/"
datumsangaben = []
ferienzeiten = []
rad_saisons = []

for jahr in jahre:
    response_feiert = requests.get(f"{api_url_feiert}?jahr={jahr}&nur_land=NW")
    feiertage = response_feiert.json()
    for details in feiertage.values():
        datumsangaben.append(details["datum"])

for jahr in jahre:
    response_ferien = requests.get(f"{api_url_ferien}{jahr}/NW")
    ferien = response_ferien.json()
    for ferienzeit in ferien:
        ferienzeiten.append({
            "start": ferienzeit["start"],
            "end": ferienzeit["end"]
        })

for jahr in jahre:
    rad_saisons.append({
        "start": f"{jahr}-04-01",
        "end": f"{jahr}-10-31"
    })

combined_data = {
    "Feiertage": datumsangaben,
    "Ferienzeiten": ferienzeiten,
    "Rad_Saison": rad_saisons
}

dateiname = 'zeitangaben.json'

with open(dateiname, 'w') as file:
    json.dump(combined_data, file, indent=4)
