from src.components.data_ingestion import download_stock_data
from src.components.model_evaluation import evaluate_model
from src.components.model_trainer import train_multiple_models, select_and_save_best_model
from src.components.data_transformation import (
    transform_data,
    split_data,
    save_processed_data,
    feature_target_split,
    scale_features
)
from src.components.model_trainer import train_multiple_models

def run_training_pipeline(ticker):

    # 1️⃣ Ingestion
    raw_path = download_stock_data(
    ticker,
    start_date="2015-01-01",
    end_date="2025-01-01"
)
    # 2️⃣ Transformation
    df = transform_data(raw_path)

    # 3️⃣ Split
    train_df, test_df = split_data(df)

    # 4️⃣ Save processed
    save_processed_data(train_df, test_df)

    # 5️⃣ Feature split
    X_train, X_test, y_train, y_test = feature_target_split(train_df, test_df)

    # 6️⃣ Scaling
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    # 7️⃣ Model training
    results, models = train_multiple_models(
    X_train_scaled,
    y_train,
    X_test_scaled,
    y_test
)

    model_path, scaler_path = select_and_save_best_model(results, models, scaler)
    best_model_name = min(results, key=results.get)
    best_model = models[best_model_name]
    metrics = evaluate_model(best_model, X_test_scaled, y_test)

    print(results)
    print(metrics)
    
    import json
    import os

    os.makedirs("artifacts/model", exist_ok=True)

    with open("artifacts/model/model_results.json", "w") as f:
        json.dump(results, f, indent=4)

    return model_path, scaler_path

    