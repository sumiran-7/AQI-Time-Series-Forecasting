import requests
import pandas as pd


# Delhi coordinates
LATITUDE = 28.6139
LONGITUDE = 77.2090

API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def get_live_aqi():
    """
    Fetch current Delhi air-quality conditions.
    """

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": (
            "us_aqi,"
            "pm2_5,"
            "pm10,"
            "nitrogen_dioxide,"
            "carbon_monoxide,"
            "ozone"
        ),
        "hourly": "us_aqi,pm2_5,pm10",
        "timezone": "Asia/Kolkata",
        "forecast_days": 5,
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


def get_current_conditions():
    """
    Return current AQI and pollutant values.
    """

    data = get_live_aqi()

    current = data["current"]

    return {
        "timestamp": current["time"],
        "aqi": current["us_aqi"],
        "pm2_5": current["pm2_5"],
        "pm10": current["pm10"],
        "no2": current["nitrogen_dioxide"],
        "co": current["carbon_monoxide"],
        "o3": current["ozone"],
    }


def get_hourly_forecast():
    """
    Return hourly AQI forecast as a DataFrame.
    """

    data = get_live_aqi()

    hourly = data["hourly"]

    df = pd.DataFrame({
        "datetime": pd.to_datetime(hourly["time"]),
        "aqi": hourly["us_aqi"],
        "pm2_5": hourly["pm2_5"],
        "pm10": hourly["pm10"],
    })

    return df


if __name__ == "__main__":

    print("=" * 50)
    print("DELHI LIVE AIR QUALITY")
    print("=" * 50)

    current = get_current_conditions()

    for key, value in current.items():
        print(f"{key}: {value}")

    print("\nHourly forecast:")
    print(get_hourly_forecast().head(10))