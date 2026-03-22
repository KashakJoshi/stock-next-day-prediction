import os
import json
import joblib
import logging
import pandas as pd
import matplotlib.pyplot as plt

from src.components.data_ingestion import download_stock_data
from src.components.data_transformation import transform_data


def run_prediction_pipeline(ticker: str, date: str):

    logging.info("Starting prediction pipeline")

    # ---------------- LOAD MODEL ----------------
    model = joblib.load("artifacts/model/model.pkl")
    scaler = joblib.load("artifacts/model/scaler.pkl")

    logging.info("Model and scaler loaded")

    # ---------------- DOWNLOAD FRESH DATA ----------------
    raw_path = download_stock_data(
        ticker,
        start_date="2015-01-01",
        end_date=date
    )

    logging.info("Fresh data downloaded")

    # ---------------- TRANSFORM DATA ----------------
    df = transform_data(raw_path)

    logging.info("Fresh data transformed")

    # ---------------- SELECT ROW ----------------
    date = pd.to_datetime(date)

    if date not in df.index:
        logging.warning("Date not trading day → using last available row")
        row = df.iloc[-1]
    else:
        row = df.loc[date]

    logging.info("Prediction row selected")

    features = [
        "returns",
        "volatility",
        "day",
        "range",
        "momentum_5",
        "Volume"
    ]

    X = row[features].values.reshape(1, -1)

    # ---------------- SCALE ----------------
    X_scaled = scaler.transform(X)

    logging.info("Features scaled")

    # ---------------- PREDICT ----------------
    pred = model.predict(X_scaled)[0]

    logging.info(f"Prediction generated: {pred}")

    trend = "UP" if pred > 0 else "DOWN"

    # ---------------- GRAPH ----------------
    plt.figure(figsize=(12, 5))
    plt.plot(df.index[-100:], df["Close"].tail(100))
    plt.scatter(df.index[-1], df["Close"].iloc[-1], color="red")
    plt.title(f"{ticker} Price Trend")

    os.makedirs("artifacts/plots", exist_ok=True)

    graph_path = f"artifacts/plots/{ticker}_prediction.png"

    plt.savefig(graph_path)
    plt.close()

    logging.info("Prediction graph generated")

    logging.info("Prediction pipeline completed")

    # ---------------- SAVE RESULT JSON ----------------
    result = {
        "ticker": ticker,
        "date": str(date),
        "predicted_return": float(pred),
        "trend": trend,
        "graph": graph_path
    }

    os.makedirs("artifacts/predictions", exist_ok=True)

    pred_path = f"artifacts/predictions/{ticker}_prediction.json"

    with open(pred_path, "w") as f:
        json.dump(result, f, indent=4)

    logging.info(f"Prediction result saved at {pred_path}")

    return result