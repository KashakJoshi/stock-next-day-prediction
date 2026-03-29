import matplotlib 
matplotlib.use('Agg')   

import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

def convert_plot_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_base64

def plot_full_history(df, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close'], label='Close Price')

    plt.title(f"{ticker} - Full Price History")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()



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



def plot_all(df, ticker, predicted_return, specified_date):
    df['Date'] = pd.to_datetime(df['Date'])

    # ===== FULL HISTORY =====
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Close'])
    plt.title(f"{ticker} - Full History")

    img1 = convert_plot_to_base64()

    # ===== RECENT =====
    df_recent = df.tail(100)
    last_price = df_recent['Close'].iloc[-1]
    predicted_price = last_price * (1 + predicted_return)

    plt.figure(figsize=(10, 5))
    plt.plot(df_recent['Date'], df_recent['Close'])

    plt.scatter(df_recent['Date'].iloc[-1], predicted_price)
    plt.title(f"{ticker} - Prediction")

    img2 = convert_plot_to_base64()

    return {
        "full_graph": img1,
        "recent_graph": img2
    }