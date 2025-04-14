import streamlit as st
import requests
from geopy.geocoders import Nominatim
from recommender import get_clothing_recommendation
from main import get_weather_data, estimate_uv_index

# ----------------------------
# Get coordinates from city name
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
        font-family: "Figtree", sans-serif;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Clothcast")

city_input = st.text_input("Enter a place (like Oslo or Budapest)", value="Budapest")

if city_input:
    lat, lon = get_coordinates_from_city(city_input)

    if lat and lon:
        st.markdown(f" **Location**: {city_input} **Coordinates:** {lat:.2f}, {lon:.2f}")

        try:
            data = get_weather_data(lat, lon)
            current = data["properties"]["timeseries"][0]

            # Extract data
            temp = current["data"]["instant"]["details"]["air_temperature"]
            wind = current["data"]["instant"]["details"]["wind_speed"]
            cloudiness = current["data"]["instant"]["details"].get("cloud_area_fraction", 50)
            precip = current["data"].get("next_1_hours", {}).get("details", {}).get("precipitation_amount", 0)
            uv = estimate_uv_index(cloudiness)

            # Show weather data
            st.markdown("### Today's weather:")
            st.markdown(f"Tempe: **{temp}°C**")
            st.markdown(f"Wind: **{wind} m/s**")
            st.markdown(f"Rain or things: **{precip} mm**")
            st.markdown(f"Clouds: **{cloudiness}%**")
            st.markdown(f"Estimated UV: **{uv}**")

            # Show recommendations
            st.markdown("### Recommended clothing:")
            tips = get_clothing_recommendation(temp, wind, precip, uv, cloudiness)
            for tip in tips:
                st.write(tip)

        except Exception as e:
            st.error("An error occurred while fetching the weather data.")
            st.exception(e)
    else:
        st.warning("Could'nt find that location, try being more specific??.")
