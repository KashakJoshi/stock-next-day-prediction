import pandas as pd
import joblib

from prediction_engine.data_fetch.fetch_data import fetch_data
from prediction_engine.feature_build.build_features import (
    build_features,
    build_future_features
)


def run_prediction_pipeline(ticker, specified_date, future_days=5):

    print("STEP 1 → Fetching data...")
    df = fetch_data(ticker)

    if df is None or len(df) == 0:
        raise Exception("❌ No data fetched")

    df = df.reset_index()

    print("STEP 2 → Simulating future prices...")
    prediction_df = build_future_features(df, future_days=future_days)

    print("STEP 3 → Feature Engineering...")
    prediction_df = build_features(prediction_df)

    prediction_df = prediction_df.dropna().reset_index(drop=True)

    print("STEP 4 → Load artifacts...")
    model = joblib.load("artifacts/advanced_model/best_catboost_model.pkl")
    scaler = joblib.load("artifacts/advanced_model/scaler.pkl")
    features = joblib.load("artifacts/advanced_model/feature_list.pkl")

    prediction_df["Date"] = pd.to_datetime(prediction_df["Date"]).dt.date
    specified_date = pd.to_datetime(specified_date).date()

    if specified_date not in prediction_df["Date"].values:
        raise Exception("❌ Specified date not available")

    print("STEP 5 → Predicting future sequence...")

    future_slice = prediction_df[prediction_df["Date"] >= specified_date].head(future_days)

    X = future_slice[features]
    X_scaled = scaler.transform(X)

    predictions = model.predict(X_scaled)

    specified_return = predictions[0]
    avg_future_return = predictions.mean()

    print("\n✅ Specified Date Return:", specified_return)
    print("✅ Avg Future Return:", avg_future_return)

    return {
        "specified_return": specified_return,
        "avg_future_return": avg_future_return,
        "predictions": predictions,
        "dates": future_slice["Date"].tolist()
    }