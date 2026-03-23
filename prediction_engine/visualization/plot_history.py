import matplotlib.pyplot as plt


def plot_year_history(df, ticker, specified_date):

    year = specified_date.year

    year_df = df[df["Date"].dt.year == year]

    plt.figure(figsize=(12,6))

    plt.plot(year_df["Date"], year_df["Close"], color="blue")

    plt.title(f"{ticker} Price Trend - Year {year}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)

    plt.show()


def plot_month_history(df, ticker, specified_date):

    year = specified_date.year
    month = specified_date.month

    month_df = df[
        (df["Date"].dt.year == year) &
        (df["Date"].dt.month == month)
    ]

    plt.figure(figsize=(12,6))

    plt.plot(month_df["Date"], month_df["Close"], color="green")

    plt.title(f"{ticker} Price Trend - {year}-{month}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)

    plt.show()