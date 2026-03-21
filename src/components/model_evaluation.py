import os
import json
import logging
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from src.utils.common import safe_run
import numpy as np



@safe_run
def evaluate_model(model, X_test, y_test):

    logging.info("Starting model evaluation")

    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

    os.makedirs("artifacts/evaluation", exist_ok=True)

    with open("artifacts/evaluation/metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    logging.info(f"Evaluation completed → {metrics}")

    return metrics