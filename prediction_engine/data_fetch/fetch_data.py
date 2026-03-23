import yfinance as yf
import pandas as pd


def fetch_data(ticker):

    df = yf.download(ticker, period="max")

    # ⭐ VERY IMPORTANT → remove multi index columns
    df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    df = df.rename(columns={
        "Adj Close": "Close"
    })

    df = df.sort_values("Date")

    return df