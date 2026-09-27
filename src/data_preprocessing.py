import pandas as pd


def load_city_day_data(path):
    """
    Load the city-day AQI dataset.
    """
    df = pd.read_csv(path)

    df["Date"] = pd.to_datetime(df["Date"])

    return df


def prepare_delhi_aqi(df):
    """
    Extract Delhi AQI time series and prepare it
    for forecasting.
    """

    delhi = df[df["City"] == "Delhi"].copy()

    delhi["Date"] = pd.to_datetime(delhi["Date"])

    delhi = (
        delhi[
            ["Date", "AQI"]
        ]
        .dropna(subset=["AQI"])
        .sort_values("Date")
        .set_index("Date")
    )

    delhi = delhi.asfreq("D")

    delhi["AQI"] = delhi["AQI"].interpolate(
        method="linear"
    )

    return delhi


def load_processed_aqi(path):
    """
    Load the already processed Delhi AQI dataset.
    """

    df = pd.read_csv(
        path,
        parse_dates=["Date"]
    )

    df = (
        df.sort_values("Date")
        .set_index("Date")
    )

    return df