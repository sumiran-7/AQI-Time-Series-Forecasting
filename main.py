"""
AQI Time Series Forecasting
---------------------------
Main entry point for generating Delhi AQI forecasts
using the final trained LSTM model.
"""

import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)
from tensorflow.keras.models import load_model


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "delhi_aqi_timeseries.csv"
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "final_lstm_model.keras"
)

SCALER_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "lstm_scaler.pkl"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "outputs",
    "forecasts"
)

OUTPUT_PATH = os.path.join(
    OUTPUT_DIR,
    "main_lstm_forecast.csv"
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

LOOKBACK = 30

TEST_START = "2019-07-03"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data():

    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["Date"]
    )

    df = (
        df
        .sort_values("Date")
        .set_index("Date")
    )

    return df


# --------------------------------------------------
# CREATE LSTM SEQUENCES
# --------------------------------------------------

def create_sequences(data, lookback):

    X = []

    for i in range(
        lookback,
        len(data)
    ):

        X.append(
            data[
                i - lookback:i
            ]
        )

    return np.array(X)


# --------------------------------------------------
# FORECASTING
# --------------------------------------------------

def generate_forecast(
    model,
    scaler,
    train_validation,
    test
):

    # Scale data using the final scaler
    train_validation_scaled = scaler.transform(
        train_validation[["AQI"]]
    )

    test_scaled = scaler.transform(
        test[["AQI"]]
    )

    # Use the last 30 observations from
    # train + validation as context
    test_input = np.concatenate([
        train_validation_scaled[-LOOKBACK:],
        test_scaled
    ])

    X_test = create_sequences(
        test_input,
        LOOKBACK
    )

    # Generate predictions
    predictions_scaled = model.predict(
        X_test,
        verbose=0
    )

    # Convert predictions back to AQI scale
    predictions = scaler.inverse_transform(
        predictions_scaled
    ).flatten()

    forecast = pd.Series(
        predictions,
        index=test.index,
        name="LSTM_Forecast"
    )

    return forecast


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

def evaluate_forecast(
    actual,
    forecast
):

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


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("=" * 60)
    print("DELHI AQI TIME SERIES FORECASTING")
    print("=" * 60)

    # Load data
    print("\nLoading processed AQI data...")

    df = load_data()

    print(
        f"Dataset shape: {df.shape}"
    )

    print(
        f"Date range: "
        f"{df.index.min().date()} "
        f"to "
        f"{df.index.max().date()}"
    )

    # Split data
    train_validation = df[
        df.index < TEST_START
    ]

    test = df[
        df.index >= TEST_START
    ]

    print(
        f"\nTrain + Validation: "
        f"{len(train_validation)} observations"
    )

    print(
        f"Final Test: "
        f"{len(test)} observations"
    )

    # Load model
    print("\nLoading trained LSTM model...")

    model = load_model(
        MODEL_PATH
    )

    # Load scaler
    print("Loading scaler...")

    scaler = joblib.load(
        SCALER_PATH
    )

    # Generate forecast
    print("\nGenerating test forecast...")

    forecast = generate_forecast(
        model,
        scaler,
        train_validation,
        test
    )

    # Evaluate
    metrics = evaluate_forecast(
        test["AQI"],
        forecast
    )

    # Create output directory
    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    # Save forecast
    output = pd.DataFrame({
        "Date": test.index,
        "Actual_AQI": test["AQI"].values,
        "LSTM_Forecast": forecast.values
    })

    output.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # Results
    print("\n" + "=" * 60)
    print("FINAL LSTM TEST PERFORMANCE")
    print("=" * 60)

    print(
        f"MAE  : {metrics['MAE']:.2f}"
    )

    print(
        f"RMSE : {metrics['RMSE']:.2f}"
    )

    print(
        f"MAPE : {metrics['MAPE']:.2f}%"
    )

    print("\nFirst 5 predictions:")

    print(
        output.head()
    )

    print(

        f"\nForecast saved to:\n{OUTPUT_PATH}"
    )

    print("\n" + "=" * 60)
    print("FORECASTING COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()