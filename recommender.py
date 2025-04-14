def get_clothing_recommendation(temp, wind, precipitation, uv_index=0, cloudiness=0):
    """
    Return a list of clothing recommendations based on weather input.

    Args:
        temp (float): Air temperature in °C
        wind (float): Wind speed in m/s
        precipitation (float): Precipitation amount in mm
        uv_index (float): Estimated UV index (optional)
        cloudiness (float): Cloud cover percentage (optional)

    Returns:
        list[str]: Clothing suggestions
    """
    recommendations = []

    # Temperature-based clothing
    if temp < 0:
        recommendations.extend(["winter jacket", "mittens and scarf"])
    elif temp < 5:
        recommendations.extend(["warm jacket"])
    elif temp < 12:
        recommendations.append("jacket or thick sweater")
    elif temp < 18:
        recommendations.append("long sleeved shirt")
    else:
        recommendations.append("t shirt or light clothing")

    # Wind
    if wind > 7:
        recommendations.append("wind jacket")

    # Rain
    if precipitation > 0:
        recommendations.append("rain jacket or umbrella")

    # UV
    if uv_index >= 5:
        recommendations.append("SUNSCREEN!!!!")

    # Cloudiness + UV
    if cloudiness < 20 and uv_index >= 3:
        recommendations.append("Caps or sunglasses")

    return recommendations
