import joblib

from prediction_engine.data_fetch.fetch_data import fetch_data
from prediction_engine.feature_build.build_features import build_features


def run_prediction_pipeline(ticker, prediction_date):

    print("STEP 1 → Fetching data...")
    df = fetch_data(ticker)

    print("STEP 2 → Feature Engineering...")
    df = build_features(df)

    print("DF SHAPE AFTER FE:", df.shape)

    print("STEP 3 → Load Artifacts...")
    model = joblib.load("artifacts/advanced_model/best_catboost_model.pkl")
    scaler = joblib.load("artifacts/advanced_model/scaler.pkl")
    features = joblib.load("artifacts/advanced_model/feature_list.pkl")

    # ⭐ IMPORTANT → dropna AFTER features
    df = df.dropna()

    print("STEP 4 → Selecting prediction row...")

    df["Date"] = df["Date"].astype(str)

    if prediction_date in df["Date"].values:

        X = df[df["Date"] == prediction_date][features]

        print("✅ Using SPECIFIED date")

    else:

        X = df[features].tail(1)

        print("❌ Date not found → using LAST available row")

    # ⭐ SAFETY CHECK
    if len(X) == 0:
        raise Exception("❌ No valid row available for prediction")

    print("STEP 5 → Scaling...")
    X_scaled = scaler.transform(X)

    print("STEP 6 → Predicting...")
    pred = model.predict(X_scaled)[0]

    print("\n FINAL PREDICTION:", pred)

    return pred