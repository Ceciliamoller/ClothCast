import streamlit as st
import requests
from geopy.geocoders import Nominatim
from recommender import get_clothing_recommendation
from main import get_weather_data, estimate_uv_index

# ----------------------------
# Finn koordinater fra bynavn
# ----------------------------
def get_coordinates_from_city(city_name):
    geolocator = Nominatim(user_agent="clothcast")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Clothcast", page_icon="🧥")
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: "Helvetica Neue", sans-serif;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Clothcast")

city_input = st.text_input("Skriv inn et sted (f.eks. Oslo, Budapest)", value="Budapest")

if city_input:
    lat, lon = get_coordinates_from_city(city_input)

    if lat and lon:
        st.markdown(f" **Sted**: {city_input} **Koordinater:** {lat:.2f}, {lon:.2f}")

        try:
            data = get_weather_data(lat, lon)
            current = data["properties"]["timeseries"][0]

            # Hent ut data
            temp = current["data"]["instant"]["details"]["air_temperature"]
            wind = current["data"]["instant"]["details"]["wind_speed"]
            cloudiness = current["data"]["instant"]["details"].get("cloud_area_fraction", 50)
            precip = current["data"].get("next_1_hours", {}).get("details", {}).get("precipitation_amount", 0)
            uv = estimate_uv_index(cloudiness)

            # Vis værdata
            st.markdown("###  Dagens vær:")
            st.markdown(f"Temperatur: **{temp}°C**")
            st.markdown(f"Vind: **{wind} m/s**")
            st.markdown(f"Nedbør: **{precip} mm**")
            st.markdown(f"Skydekke: **{cloudiness}%**")
            st.markdown(f"Estimert UV-indeks: **{uv}**")

            # Få anbefalinger
            st.markdown("### Anbefalte klær:")
            tips = get_clothing_recommendation(temp, wind, precip, uv, cloudiness)
            for tip in tips:
                st.write(tip)

        except Exception as e:
            st.error("Det oppstod en feil ved henting av værdata.")
            st.exception(e)
    else:
        st.warning("Fant ikke det stedet – prøv å skrive det mer presist.")
