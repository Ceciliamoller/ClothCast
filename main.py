import requests
from datetime import datetime
from recommender import get_clothing_recommendation

# ----------------------------
# SETTINGS: LOCATION (Budapest)
# ----------------------------
LAT = 47.4979
LON = 19.0402

# ----------------------------
# Function: Estimate UV index (simple logic)
# ----------------------------
def estimate_uv_index(cloudiness):
    if cloudiness < 20:
        return 6
    elif cloudiness < 60:
        return 4
    else:
        return 2
    

    import requests
from datetime import datetime, timezone


# ----------------------------
# Function: Fetch sunset data from MET API
# ----------------------------
def get_sunset_time(lat, lon):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=0"

    headers = {
        "User-Agent": "ClothCast/1.0"  # Met.no requires User-Agent!
    }

    response = requests.get(url)
    data = response.json()

    # Navigate to the sunset time
    sunset_str = data["results"]["sunset"]

    # Convert to datetime object
    sunset_time = datetime.fromisoformat(sunset_str)

    return sunset_time


# ----------------------------
# Function: Fetch weather data from MET API
# ----------------------------
def get_weather_data(lat, lon):
    headers = {
        "User-Agent": "clothcast/1.0 ceciliamollerblom@gmail.com"
    }
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Kaster feil hvis noe går galt
    return response.json()

# ----------------------------
# Main script
# ----------------------------
def main():
    data = get_weather_data(LAT, LON)
    
    # Henter første tidspunkt i serien (nærmeste time)
    current = data["properties"]["timeseries"][0]

    # Ekstraherer værdata
    temp = current["data"]["instant"]["details"]["air_temperature"]
    wind = current["data"]["instant"]["details"]["wind_speed"]
    cloudiness = current["data"]["instant"]["details"].get("cloud_area_fraction", 50)
    precip = current["data"].get("next_1_hours", {}).get("details", {}).get("precipitation_amount", 0)
    uv = estimate_uv_index(cloudiness)

    # Få anbefalinger
    recommendations = get_clothing_recommendation(
        temp=temp,
        wind=wind,
        precipitation=precip,
        uv_index=uv,
        cloudiness=cloudiness
    )

    # Skriv ut resultatet
    print("\n📍 Location: Budapest")
    print(f"🕒 Time: {current['time']}")
    print(f"🌡️ Temp: {temp}°C | 💨 Wind: {wind} m/s | 🌧️ rain or something: {precip} mm | ☁️ cloudiness: {cloudiness}% | ☀️ UV-index (est.): {uv}")
    print("\n👕 Clothcast recommends:")
    for item in recommendations:
        print("–", item)

if __name__ == "__main__":
    main()
