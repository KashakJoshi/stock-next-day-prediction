import matplotlib.pyplot as plt
import pandas as pd


def plot_full_history(df, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close'], label='Close Price')

    plt.title(f"{ticker} - Full Price History")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()

    plt.show()


def plot_recent_with_prediction(df, ticker, predicted_return, specified_date):
    df = df.copy()

    # last 100 data points (zoom)
    df_recent = df.tail(100)

    last_date = df_recent['Date'].iloc[-1]
    last_price = df_recent['Close'].iloc[-1]

    # predicted price
    predicted_price = last_price * (1 + predicted_return)

    plt.figure(figsize=(12, 6))

    # plot recent prices
    plt.plot(df_recent['Date'], df_recent['Close'], label='Recent Price')

    # vertical line (used date)
    plt.axvline(x=last_date, linestyle='--', label='Prediction Base Date')

    # predicted point
    plt.scatter(last_date, predicted_price, label='Predicted Price', s=100)

    # arrow for direction
    if predicted_return > 0:
        plt.annotate("UP", (last_date, predicted_price))
    else:
        plt.annotate("DOWN", (last_date, predicted_price))

    plt.title(f"{ticker} - Recent Trend + Prediction")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()

    plt.show()


def plot_all(df, ticker, predicted_return, specified_date):
    # ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'])

    print("📈 Plotting Full History...")
    plot_full_history(df, ticker)

    print("📊 Plotting Recent + Prediction...")
    plot_recent_with_prediction(df, ticker, predicted_return, specified_date)