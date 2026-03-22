import pandas as pd
import joblib
import yfinance as yf
import matplotlib.pyplot as plt


def run_advanced_prediction_pipeline(ticker, prediction_date):

    print("Downloading data...")

    df = yf.download(ticker)

    df.reset_index(inplace=True)

    print("Applying feature engineering...")

    # ===== SAME FEATURE ENGINEERING =====

    df["returns"] = df["Close"].pct_change()

    df["ma5"] = df["Close"].rolling(5).mean()
    df["ma10"] = df["Close"].rolling(10).mean()
    df["ma20"] = df["Close"].rolling(20).mean()

    df["volatility"] = df["returns"].rolling(20).std()

    df["momentum"] = df["Close"] - df["Close"].shift(5)

    df["range"] = df["High"] - df["Low"]

    df["target_new"] = df["returns"].rolling(3).mean().shift(-1)

    df = df.dropna()

    print("Loading model artifacts...")

    model = joblib.load("artifacts/advanced_model/catboost_model.pkl")
    scaler = joblib.load("artifacts/advanced_model/scaler.pkl")
    features = joblib.load("artifacts/advanced_model/feature_list.pkl")

    X = df[features]

    X_scaled = scaler.transform(X)

    preds = model.predict(X_scaled)

    df["prediction"] = preds

    print("Prediction done")

    # ===== GRAPH =====

    plt.figure(figsize=(14,6))

    plt.plot(df["Date"], df["Close"], label="Price")

    plt.scatter(df["Date"], df["prediction"]*df["Close"].mean(),
                color="red", label="Prediction signal")

    plt.legend()

    plt.title(f"{ticker} Prediction Trend")

    plt.show()

    return df