import requests

from recommender import get_clothing_recommendation

headers = {
    "User-Agent": "klestips-prosjektet/1.0 your-email@example.com"
}

url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=47.4979&lon=19.0402" # buda


response = requests.get(url, headers=headers)
data = response.json()

# Eksempel: print ut temperaturen for nå
current = data["properties"]["timeseries"][0]
print("Time:", current["time"])
print("Temperature:", current["data"]["instant"]["details"]["air_temperature"], "°C")