import os
import joblib
import logging
from src.utils.common import safe_run
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


@safe_run
def train_multiple_models(X_train, y_train, X_test, y_test):

    logging.info("Training multiple baseline models")

    models = {}

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    models["Linear"] = lr

    ridge = Ridge()
    ridge.fit(X_train, y_train)
    models["Ridge"] = ridge

    rf = RandomForestRegressor()
    rf.fit(X_train, y_train)
    models["RF"] = rf

    results = {}

    for name, model in models.items():
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        results[name] = mae

    logging.info(f"Baseline Results: {results}")

    return results, models

@safe_run
def select_and_save_best_model(results, models, scaler):

    logging.info("Selecting best model")

    best_model_name = min(results, key=results.get)
    best_model = models[best_model_name]

    logging.info(f"Best model is {best_model_name}")

    os.makedirs("artifacts/model", exist_ok=True)

    model_path = "artifacts/model/model.pkl"
    scaler_path = "artifacts/model/scaler.pkl"

    joblib.dump(best_model, model_path)
    joblib.dump(scaler, scaler_path)

    logging.info("Model and scaler saved")

    return model_path, scaler_path