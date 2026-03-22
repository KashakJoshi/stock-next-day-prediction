from prediction_engine.data_fetch.fetch_data import fetch_stock_data
from prediction_engine.feature_build.build_features import build_features
from prediction_engine.model_use.load_model import load_artifacts


def run_prediction_pipeline(ticker):

    df = fetch_stock_data(ticker)

    df = build_features(df)

    model, scaler, features = load_artifacts()

    X = df[features].tail(1)

    X_scaled = scaler.transform(X)

    pred = model.predict(X_scaled)

    print("\n FINAL PREDICTION:", pred[0])

    return pred[0]