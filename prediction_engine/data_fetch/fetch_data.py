import yfinance as yf

def fetch_data(ticker):

    df = yf.download(
        ticker,
        start="2010-01-01",   # ⭐ BIG history
        progress=False
    )

    df.reset_index(inplace=True)

    return df