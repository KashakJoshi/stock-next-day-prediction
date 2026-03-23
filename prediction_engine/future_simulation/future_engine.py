import pandas as pd


def simulate_future_prices(df, future_days=5):

    df = df.copy().reset_index(drop=True)

    future_rows = []

    last_close = df["Close"].iloc[-1]

    for i in range(future_days):

        new_date = pd.to_datetime(df["Date"].iloc[-1]) + pd.Timedelta(days=1)

        simulated_return = 0.002   # ⭐ small constant drift

        new_close = last_close * (1 + simulated_return)

        new_row = df.iloc[-1].copy()

        new_row["Date"] = new_date
        new_row["Close"] = new_close
        new_row["Open"] = new_close
        new_row["High"] = new_close
        new_row["Low"] = new_close
        new_row["Volume"] = new_row["Volume"]

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        future_rows.append(new_row)

        last_close = new_close

    future_df = pd.DataFrame(future_rows)

    return df, future_df