import pandas as pd
import numpy as np


# ======================================================
# NORMAL FEATURE ENGINEERING (MODEL TRAINING FEATURES)
# ======================================================

def build_features(df):

    df = df.copy()

    # ---- returns
    df["returns"] = df["Close"].pct_change()

    # ---- volatility
    df["volatility"] = df["returns"].rolling(10).std()

    # ---- range
    df["range"] = (df["High"] - df["Low"]) / df["Close"]

    # ---- momentum
    df["momentum_3"] = df["Close"] / df["Close"].shift(3) - 1
    df["momentum_5"] = df["Close"] / df["Close"].shift(5) - 1
    df["momentum_7"] = df["Close"] / df["Close"].shift(7) - 1

    # ---- trend
    df["trend_3"] = df["Close"].rolling(3).mean() / df["Close"] - 1
    df["trend_7"] = df["Close"].rolling(7).mean() / df["Close"] - 1
    df["trend_10"] = df["Close"].rolling(10).mean() / df["Close"] - 1

    # ---- rolling stats
    df["roll_mean_3"] = df["returns"].rolling(3).mean()
    df["roll_std_3"] = df["returns"].rolling(3).std()

    df["roll_mean_5"] = df["returns"].rolling(5).mean()
    df["roll_std_5"] = df["returns"].rolling(5).std()

    df["roll_mean_10"] = df["returns"].rolling(10).mean()
    df["roll_std_10"] = df["returns"].rolling(10).std()

    df["roll_mean_20"] = df["returns"].rolling(20).mean()
    df["roll_std_20"] = df["returns"].rolling(20).std()

    # ---- lag returns
    df["ret_lag_1"] = df["returns"].shift(1)
    df["ret_lag_2"] = df["returns"].shift(2)
    df["ret_lag_3"] = df["returns"].shift(3)
    df["ret_lag_5"] = df["returns"].shift(5)
    df["ret_lag_7"] = df["returns"].shift(7)
    df["ret_lag_10"] = df["returns"].shift(10)
    df["ret_lag_15"] = df["returns"].shift(15)

    # ---- volume features
    df["vol_ratio"] = df["Volume"] / df["Volume"].rolling(10).mean()
    df["vol_pressure"] = df["Volume"] * df["returns"]
    df["vol_shock"] = df["Volume"].pct_change()

    # ---- price strength
    df["price_strength"] = (df["Close"] - df["Low"]) / (df["High"] - df["Low"])

    # ---- ratios
    df["high_low_ratio"] = df["High"] / df["Low"]
    df["close_open_ratio"] = df["Close"] / df["Open"]

    # ---- drawdown
    df["drawdown_5"] = df["Close"] / df["Close"].rolling(5).max() - 1

    # ---- breakout
    df["break_high_10"] = df["Close"] > df["Close"].rolling(10).max().shift(1)

    # ---- vol regime
    df["vol_regime"] = df["volatility"] > df["volatility"].rolling(20).mean()

    # ---- day
    df["Date"] = pd.to_datetime(df["Date"])
    df["day"] = df["Date"].dt.dayofweek

    return df


# ======================================================
# FUTURE PRICE SIMULATION ENGINE
# ======================================================

def build_future_features(df, future_days=5):

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    future_rows = []

    last_close = df.iloc[-1]["Close"]
    last_date = df.iloc[-1]["Date"]

    # ⭐ assume small constant drift
    drift = 0.002

    for i in range(future_days):

        new_date = last_date + pd.Timedelta(days=1)

        new_close = last_close * (1 + drift)

        new_row = {
            "Date": new_date,
            "Close": new_close,
            "Open": new_close,
            "High": new_close,
            "Low": new_close,
            "Volume": df["Volume"].mean()
        }

        future_rows.append(new_row)

        last_close = new_close
        last_date = new_date

    future_df = pd.DataFrame(future_rows)

    df = pd.concat([df, future_df], ignore_index=True)

    return df