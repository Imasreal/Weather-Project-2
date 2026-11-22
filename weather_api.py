import requests
from datetime import datetime, timezone
from config import LATITUDE, LONGITUDE, TIMEZONE

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather():
    """Fetch current model-based conditions and the next 48 hours of hourly forecast."""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "timezone": TIMEZONE,
        "current": (
            "temperature_2m,relative_humidity_2m,precipitation,"
            "wind_speed_10m"
        ),
        "hourly": (
            "temperature_2m,relative_humidity_2m,precipitation,"
            "wind_speed_10m"
        ),
        "forecast_days": 3
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    current = payload.get("current")
    hourly = payload.get("hourly")
    if not current or not hourly:
        raise ValueError("Open-Meteo response did not contain current/hourly data.")

    issued_at = datetime.now(timezone.utc).isoformat()
    actual = {
        "observed_at": current["time"],
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "rainfall": current.get("precipitation"),
        "wind_speed": current.get("wind_speed_10m"),
        "source": "Open-Meteo current model-based conditions"
    }

    forecasts = []
    for i, valid_time in enumerate(hourly["time"]):
        forecasts.append({
            "issued_at": issued_at,
            "valid_time": valid_time,
            "temperature": hourly["temperature_2m"][i],
            "humidity": hourly["relative_humidity_2m"][i],
            "rainfall": hourly["precipitation"][i],
            "wind_speed": hourly["wind_speed_10m"][i]
        })

    return actual, forecasts, payload.get("latitude"), payload.get("longitude")
