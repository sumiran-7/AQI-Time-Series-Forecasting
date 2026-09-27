import pandas as pd


def create_time_features(df):
    """
    Create calendar-based time features.
    """

    result = df.copy()

    result["day_of_week"] = result.index.dayofweek
    result["day_of_year"] = result.index.dayofyear
    result["month"] = result.index.month

    return result


def create_lag_features(
    df,
    target="AQI",
    lags=(1, 7, 14, 30, 365)
):
    """
    Create lagged AQI features.
    """

    result = df.copy()

    for lag in lags:
        result[f"lag_{lag}"] = result[target].shift(lag)

    return result


def create_rolling_features(
    df,
    target="AQI"
):
    """
    Create rolling mean and standard deviation
    features used by the ML models.
    """

    result = df.copy()

    result["rolling_mean_7"] = (
        result[target]
        .rolling(7)
        .mean()
    )

    result["rolling_mean_30"] = (
        result[target]
        .rolling(30)
        .mean()
    )

    result["rolling_std_7"] = (
        result[target]
        .rolling(7)
        .std()
    )

    result["rolling_std_30"] = (
        result[target]
        .rolling(30)
        .std()
    )

    return result


def create_ml_features(df):
    """
    Create the complete feature set used
    for machine-learning forecasting.
    """

    result = df.copy()

    result = create_time_features(result)

    result = create_lag_features(result)

    result = create_rolling_features(result)

    return result