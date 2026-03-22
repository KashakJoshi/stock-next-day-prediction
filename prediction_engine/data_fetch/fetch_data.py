import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker):

    print("STEP 1 → Fetching Data")

    df = yf.download(ticker, period="5y", auto_adjust=True)

    # ⭐ VERY IMPORTANT FIX
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.reset_index(inplace=True)

    df = df[["Date","Open","High","Low","Close","Volume"]]

    return df