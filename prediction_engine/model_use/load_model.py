import joblib


def load_artifacts():

    print("STEP 3 → Load Artifacts")

    model = joblib.load("artifacts/advanced_model/best_catboost_model.pkl")

    scaler = joblib.load("artifacts/advanced_model/scaler.pkl")

    features = joblib.load("artifacts/advanced_model/feature_list.pkl")

    return model, scaler, features