import streamlit as st
import requests
from datetime import datetime, timezone
from geopy.geocoders import Nominatim
from recommender import get_clothing_recommendation
from main import get_weather_data, get_sunset_time


# ----------------------------
# Get coordinates from city name
# ----------------------------
def get_coordinates_from_city(city_name):
    geolocator = Nominatim(user_agent="clothcast", timeout=10)
    try:
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        st.error("Could'nt reach the location service (OpenStreetMap). Try again later.")
        return None, None

# ----------------------------
# font and background
# ----------------------------

st.markdown("""
    <style>
    @font-face {
        font-family: 'Rubik';
        src: url('https://raw.githubusercontent.com/Ceciliamoller/ClothCast/main/rubik.woff2') format('woff2');
        font-weight: 400;
    }

    * {
        font-family: 'Rubik', sans-serif !important;
    }

    html, body, .stApp, .css-18ni7ap, .css-1d391kg, .css-1cpxqw2, .css-ffhzg2, .css-1v0mbdj, .css-1offfwp {
        font-family: 'Rubik', sans-serif !important;
        font-size: 16px;
    }

    </style>
""", unsafe_allow_html=True)








st.title("Clothcast")

city_input = st.text_input("Enter a place (like Oslo or Budapest)", value="Budapest")

if city_input:
    lat, lon = get_coordinates_from_city(city_input)

    if lat and lon:
        st.markdown(f" **Location**: {city_input}")

        try:
            data = get_weather_data(lat, lon)
            current = data["properties"]["timeseries"][0]

            # Extract data
            temp = current["data"]["instant"]["details"]["air_temperature"]
            wind = current["data"]["instant"]["details"]["wind_speed"]
            cloudiness = current["data"]["instant"]["details"].get("cloud_area_fraction", 50)
            precip = current["data"].get("next_1_hours", {}).get("details", {}).get("precipitation_amount", 0)

            # Show weather data
            st.markdown("### Weather today:")
            st.markdown(f"Temp: **{temp}°C**")
            st.markdown(f"Wind: **{wind} m/s**")
            st.markdown(f"Rain or things: **{precip} mm**")
            st.markdown(f"Clouds: **{cloudiness}%**")

            # --- Look ahead at next 6 hours ---
            upcoming_temps = []
            upcoming_precip = []

            for hour_data in data["properties"]["timeseries"][1:7]:
                upcoming_details = hour_data["data"]["instant"]["details"]
                upcoming_temps.append(upcoming_details.get("air_temperature", temp))  # fallback to current temp
                upcoming_precip.append(hour_data["data"].get("next_1_hours", {}).get("details", {}).get("precipitation_amount", 0))


            # get current time and sunset time
            sunset_time = get_sunset_time(lat, lon)
            now = datetime.now(timezone.utc)


            # --- Pass to recommender ---
            tips = get_clothing_recommendation(temp, wind, precip, cloudiness, upcoming_precip, upcoming_temps, now=now, sunset_time=sunset_time)

            st.markdown("### Recommended clothing:")
            for tip in tips:
                st.write(f"- {tip}")
            

        except Exception as e:
            st.error("An error occurred while fetching the weather data.")
            st.exception(e)
    else:
        st.warning("Could'nt find that location, try being more specific??.")
