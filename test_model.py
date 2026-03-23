import pandas as pd
from prediction_engine.pipeline_run.run_pipeline import run_prediction_pipeline
from prediction_engine.data_fetch.fetch_data import fetch_data

ticker = "RELIANCE.NS"

print("Fetching full data...")
df = fetch_data(ticker)

df = df.reset_index()

test_df = df.tail(60).reset_index(drop=True)

results = []

for i in range(1, 50):

    try:

        date = test_df.loc[i, "Date"]

        output = run_prediction_pipeline(
            ticker=ticker,
            specified_date=str(date.date())
        )

        predicted_return = output["predicted_return"]

        today_price = test_df.loc[i, "Close"]
        prev_price = test_df.loc[i - 1, "Close"]

        actual_return = (today_price - prev_price) / prev_price

        results.append({
            "date": date,
            "predicted_return": predicted_return,
            "actual_return": actual_return
        })

        print("✅ Done:", date.date())

    except Exception as e:
        print("❌ Skipped:", e)
        continue


results_df = pd.DataFrame(results)

print("\n======================")
print("Testing Finished")
print("======================")

print(results_df.head())