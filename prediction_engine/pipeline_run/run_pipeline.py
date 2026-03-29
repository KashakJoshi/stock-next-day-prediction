import pandas as pd
import joblib

from prediction_engine.data_fetch.fetch_data import fetch_data
from prediction_engine.feature_build.build_features import build_features
from prediction_engine.visualization.plot_history import plot_all


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

    # if future date → use latest available data
    # Handle future + holiday separately

    last_date = df['Date'].max()

    if specified_date > last_date:
        print("Future date detected → using latest available data")
        specified_date = last_date

    elif specified_date not in df['Date'].values:
        print("Holiday/Weekend detected → using nearest trading day")
    
    nearest_idx = df['Date'].searchsorted(specified_date)
    
    if nearest_idx >= len(df):
        nearest_idx = len(df) - 1
    
    specified_date = df['Date'].iloc[nearest_idx]

    row = df[df["Date"] == specified_date]

    feature_cols = [c for c in df.columns if c not in ["Date", "Close"]]

    X = row[feature_cols]

    print("STEP 5 → Predicting...")
    prediction = model.predict(X)[0]

    print("✅ Predicted Return:", prediction)

    print("STEP 6 → Plotting Graphs...")

    graphs = plot_all(df, ticker, prediction, specified_date)
    
    current_price = df[df["Date"] == specified_date]["Close"].values[0]
    expected_price = current_price * (1 + prediction)
    print("DEBUG → returning:", current_price, expected_price)

    return {
        "predicted_return": prediction,
        "current_price": float(current_price),
        "expected_price": float(expected_price),
        "date": specified_date,
        "graphs": graphs
    }