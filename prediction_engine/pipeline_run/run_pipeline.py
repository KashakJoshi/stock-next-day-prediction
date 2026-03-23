import pandas as pd
import joblib

from prediction_engine.data_fetch.fetch_data import fetch_data
from prediction_engine.feature_build.build_features import build_features
from prediction_engine.visualization.plot_history import plot_year_history
from prediction_engine.visualization.plot_history import plot_month_history


def run_prediction_pipeline(ticker, specified_date):

    print("STEP 1 → Fetching data...")
    df = fetch_data(ticker)

    if df is None or len(df) == 0:
        raise Exception("❌ No data fetched")

    df = df.reset_index()

    print("STEP 2 → Feature Engineering...")
    df = build_features(df)

    df = df.dropna().reset_index(drop=True)

    print("STEP 3 → Load Model...")
    model = joblib.load("artifacts/advanced_model/best_catboost_model.pkl")

    print("STEP 4 → Convert Date...")
    specified_date = pd.to_datetime(specified_date)

    if specified_date not in df["Date"].values:
        raise Exception("❌ Specified date not available in dataset")

    row = df[df["Date"] == specified_date]

    feature_cols = [c for c in df.columns if c not in ["Date", "Close"]]

    X = row[feature_cols]

    print("STEP 5 → Predicting...")
    prediction = model.predict(X)[0]

    print("✅ Predicted Return:", prediction)

    print("STEP 6 → Plotting Graphs...")

    plot_year_history(df, ticker, specified_date)
    plot_month_history(df, ticker, specified_date)

    return {
        "predicted_return": float(prediction),
        "date": specified_date.date()
    }