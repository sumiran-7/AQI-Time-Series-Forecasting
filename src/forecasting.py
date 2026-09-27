import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


def evaluate_forecast(
    actual,
    forecast
):
    """
    Calculate MAE, RMSE and MAPE.
    """

    actual = pd.Series(actual)
    forecast = pd.Series(
        forecast,
        index=actual.index
    )

    mae = mean_absolute_error(
        actual,
        forecast
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            forecast
        )
    )

    non_zero = actual != 0

    mape = (
        np.mean(
            np.abs(
                (
                    actual[non_zero]
                    - forecast[non_zero]
                )
                / actual[non_zero]
            )
        )
        * 100
    )

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    }


def naive_forecast(
    train,
    horizon
):
    """
    Naive forecast:
    every future value equals the
    last observed training value.
    """

    last_value = train.iloc[-1]

    return pd.Series(
        last_value,
        index=pd.RangeIndex(horizon)
    )


def seasonal_naive_forecast(
    train,
    horizon,
    season=7
):
    """
    Seasonal naive forecast.

    Repeats the values from the previous
    seasonal cycle.
    """

    values = train.iloc[-season:].values

    repetitions = int(
        np.ceil(horizon / season)
    )

    forecast = np.tile(
        values,
        repetitions
    )[:horizon]

    return pd.Series(forecast)


def create_fourier_features(
    index,
    period=365,
    K=7
):
    """
    Create Fourier terms for yearly
    seasonality.
    """

    index = pd.DatetimeIndex(index)

    t = np.arange(len(index))

    features = {}

    for k in range(1, K + 1):

        features[f"sin_{k}"] = np.sin(
            2 * np.pi * k * t / period
        )

        features[f"cos_{k}"] = np.cos(
            2 * np.pi * k * t / period
        )

    return pd.DataFrame(
        features,
        index=index
    )