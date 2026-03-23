import numpy as np
import pandas as pd
import joblib

from prediction_engine.data_fetch.fetch_data import fetch_data
from prediction_engine.feature_build.build_features import build_features


print("Downloading data...")
df = fetch_data("RELIANCE.NS")

print("Feature engineering...")
df = build_features(df)

# ⭐ TARGET = next day return
df["target"] = df["returns"].shift(-1)

df = df.dropna().reset_index(drop=True)

# ⭐ Load artifacts
model = joblib.load("artifacts/model/model.pkl")
scaler = joblib.load("artifacts/model/scaler.pkl")
feature_cols = joblib.load("artifacts/model/feature_cols.pkl")

X = df[feature_cols]
y_true = df["target"]

# ⭐ Safety check
if len(X) == 0:
    print("❌ No samples available after cleaning")
    exit()

# ⭐ Scale
X_scaled = scaler.transform(X)

# ⭐ Predict
y_pred = model.predict(X_scaled)

# ⭐ Metrics
rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
mae = np.mean(np.abs(y_true - y_pred))

direction_acc = np.mean(
    (np.sign(y_true) == np.sign(y_pred)).astype(int)
)

print("\n========== MODEL PERFORMANCE ==========")
print("RMSE :", rmse)
print("MAE :", mae)
print("Directional Accuracy :", direction_acc)
print("=======================================\n")