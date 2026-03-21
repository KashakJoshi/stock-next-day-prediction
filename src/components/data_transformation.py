import pandas as pd
import logging
import os
from src.utils.common import safe_run
from sklearn.preprocessing import StandardScaler


@safe_run
def transform_data(file_path: str):

    logging.info("Starting data transformation")

    df = pd.read_csv(file_path)

    # remove top useless rows
    df = df.iloc[2:].copy()

    # rename first column → Date
    df.rename(columns={df.columns[0]: "Date"}, inplace=True)

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df.set_index("Date", inplace=True)
    
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df["High"] = pd.to_numeric(df["High"], errors="coerce")
    df["Low"] = pd.to_numeric(df["Low"], errors="coerce")
    df["Open"] = pd.to_numeric(df["Open"], errors="coerce")
    df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce")

    # feature engineering
    df["returns"] = df["Close"].pct_change()
    df["volatility"] = df["returns"].rolling(20).std()
    df["range"] = df["High"] - df["Low"]
    df["momentum_5"] = df["Close"].pct_change(5)
    df["day"] = df.index.dayofweek

    # target
    df["target"] = df["returns"].shift(-1)

    df = df.dropna()

    logging.info("Data transformation completed")

    return df


@safe_run
def split_data(df):

    logging.info("Starting train test split")

    split_ratio = 0.8
    split_index = int(len(df) * split_ratio)

    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    logging.info("Train test split completed")

    return train_df, test_df


@safe_run
def save_processed_data(train_df, test_df):

    logging.info("Saving processed datasets")

    os.makedirs("artifacts/processed", exist_ok=True)

    train_path = "artifacts/processed/train.csv"
    test_path = "artifacts/processed/test.csv"

    train_df.to_csv(train_path)
    test_df.to_csv(test_path)

    logging.info("Processed data saved successfully")

    return train_path, test_path


@safe_run
def feature_target_split(train_df, test_df):

    logging.info("Starting feature target split")

    features = [
        "returns",
        "volatility",
        "day",
        "range",
        "momentum_5",
        "Volume"
    ]

    target = "target"

    X_train = train_df[features]
    y_train = train_df[target]

    X_test = test_df[features]
    y_test = test_df[target]

    logging.info("Feature target split completed")

    return X_train, X_test, y_train, y_test


@safe_run
def scale_features(X_train, X_test):

    logging.info("Starting feature scaling")

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    logging.info("Feature scaling completed")

    return X_train_scaled, X_test_scaled, scaler