from datetime import datetime

from datetime import datetime

def estimate_feels_like_temp(temp, wind, cloudiness, now=None, sunset_time=None):
    """
    Estimate 'feels like' temperature based on temperature, wind, clouds, and sunset proximity.
    - temp: Current temperature (°C)
    - wind: Wind speed (m/s)
    - cloudiness: Cloud coverage (%)
    - now: Current datetime (UTC)
    - sunset_time: Sunset datetime (UTC)
    """

    adjusted_temp = temp

    # 1. Adjust for wind
    if wind >= 8:
        adjusted_temp -= 4
    elif wind >= 5:
        adjusted_temp -= 2
    elif wind >= 3:
        adjusted_temp -= 1

    # 2. Adjust for cloudiness
    if cloudiness > 80:
        adjusted_temp -= 2
    elif cloudiness > 50:
        adjusted_temp -= 1

    # 3. Adjust for sunset (if times are provided)
    if now and sunset_time:
        time_to_sunset = (sunset_time - now).total_seconds() / 3600  # in hours

        if time_to_sunset > 2:
            sunset_penalty = 0
        elif 1 <= time_to_sunset <= 2:
            sunset_penalty = 1
        elif 0 <= time_to_sunset < 1:
            sunset_penalty = 3
        else:  # After sunset
            sunset_penalty = 5

        adjusted_temp -= sunset_penalty

    return adjusted_temp


def is_daytime(current_hour):
    """Determine if it is daytime (6AM to 7PM)."""
    return 6 <= current_hour <= 19

def get_clothing_recommendation(temp, wind, precip, uv, cloudiness, upcoming_precip=[], upcoming_temps=[], now=None, sunset_time=None):
    tips = []

    # --- Adjust temp for wind and clouds ---
    adjusted_temp = estimate_feels_like_temp(temp, wind, cloudiness, now, sunset_time)

    # Wind effect
    if wind > 6:
        adjusted_temp -= 4
    elif wind > 3:
        adjusted_temp -= 2

    # Cloud effect
    if cloudiness > 80:
        adjusted_temp -= 2
    elif cloudiness > 50:
        adjusted_temp -= 1

    # --- Base clothing recommendations ---
    if adjusted_temp >= 25:
        tips.append("Light summer clothes are recommended (shorts, T-shirt, dress).")
    elif adjusted_temp >= 20:
        tips.append("T-shirt or light clothing are fine.")
    elif adjusted_temp >= 15:
        tips.append("Long-sleeved shirt or light sweater is a good idea.")
    elif adjusted_temp >= 10:
        tips.append("Wear a sweater and consider a light jacket.")
    elif adjusted_temp >= 5:
        tips.append("Jacket and possibly a thin sweater underneath.")
    else:
        tips.append("warm clothes: recommend coat, scarf, and layers.")

    # --- Precipitation ---
    if precip > 0.5:
        tips.append("Rain expected! Bring an umbrella or raincoat.")

    # --- UV index ---
    if uv >= 5 and now and sunset_time:
        time_to_sunset = (sunset_time - now).total_seconds() / 3600
        if time_to_sunset > 0:  # It's still before sunset
            tips.append("High UV! Use sunscreen and sunglasses.")

    
    # --- Future weather (upcoming 6h) ---
    if upcoming_temps:
        max_temp_change = max(upcoming_temps) - temp
        min_temp_change = min(upcoming_temps) - temp

        if max_temp_change >= 5:
            tips.append("It will get warmer later, maybe bring lighter clothing")
        if min_temp_change <= -5:
            tips.append("It will get colder later, maybe bring extra clothes")

    if upcoming_precip:
        if any(p > 0.5 for p in upcoming_precip):
            tips.append("It might start raining later, maybe bring an umbrella just in case")

    return tips
