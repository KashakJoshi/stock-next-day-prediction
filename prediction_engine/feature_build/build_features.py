import pandas as pd
import numpy as np


def build_features(df):

    print("STEP 2 → Feature Engineering")

    df["returns"] = df["Close"].pct_change()

    df["volatility"] = df["returns"].rolling(20).std()

    df["range"] = df["High"] - df["Low"]

    df["momentum_3"] = df["Close"] - df["Close"].shift(3)
    df["momentum_5"] = df["Close"] - df["Close"].shift(5)
    df["momentum_7"] = df["Close"] - df["Close"].shift(7)

    df["trend_3"] = df["Close"].rolling(3).mean()
    df["trend_7"] = df["Close"].rolling(7).mean()
    df["trend_10"] = df["Close"].rolling(10).mean()

    df["roll_mean_3"] = df["returns"].rolling(3).mean()
    df["roll_std_3"] = df["returns"].rolling(3).std()

    df["roll_mean_5"] = df["returns"].rolling(5).mean()
    df["roll_std_5"] = df["returns"].rolling(5).std()

    df["roll_mean_10"] = df["returns"].rolling(10).mean()
    df["roll_std_10"] = df["returns"].rolling(10).std()

    df["roll_mean_20"] = df["returns"].rolling(20).mean()
    df["roll_std_20"] = df["returns"].rolling(20).std()

    df["ret_lag_1"] = df["returns"].shift(1)
    df["ret_lag_2"] = df["returns"].shift(2)
    df["ret_lag_3"] = df["returns"].shift(3)
    df["ret_lag_5"] = df["returns"].shift(5)
    df["ret_lag_7"] = df["returns"].shift(7)
    df["ret_lag_10"] = df["returns"].shift(10)
    df["ret_lag_15"] = df["returns"].shift(15)

    df["vol_ratio"] = df["Volume"] / df["Volume"].rolling(20).mean()

    df["vol_pressure"] = df["Volume"] * df["returns"]

    df["break_high_10"] = df["High"] > df["High"].rolling(10).max()

    df["drawdown_5"] = df["Close"] / df["Close"].rolling(5).max() - 1

    df["high_low_ratio"] = df["High"] / df["Low"]

    df["close_open_ratio"] = df["Close"] / df["Open"]

    df["price_strength"] = df["Close"] - df["Open"]

    df["vol_shock"] = df["Volume"].pct_change()

    df["day"] = pd.to_datetime(df["Date"]).dt.day

    df["vol_regime"] = (df["volatility"] > df["volatility"].rolling(50).mean()).astype(int)

    df = df.dropna()

    print("DF SHAPE AFTER FE:", df.shape)

    return df