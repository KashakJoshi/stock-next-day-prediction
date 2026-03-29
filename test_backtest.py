from prediction_engine.pipeline_run.run_pipeline import run_prediction_pipeline
import pandas as pd
import yfinance as yf

ticker = "RELIANCE.NS"

test_dates = [
    "2025-01-10",
    "2025-02-10",
    "2025-03-10",
    "2025-04-10",
    "2025-05-10"
]

# =========================
# STEP 1 → PREDICTIONS
# =========================

results = []

for date in test_dates:
    print(f"\nTesting for date: {date}")
    
    output = run_prediction_pipeline(
        ticker=ticker,
        specified_date=date
    )
    
    pred_return = output['predicted_return']
    
    results.append({
        "date": date,
        "predicted_return": pred_return
    })

df_results = pd.DataFrame(results)

# =========================
# STEP 2 → ACTUAL RETURNS
# =========================

data = yf.download(ticker, start="2024-12-01", end="2025-06-01")
data['return'] = data['Close'].pct_change().shift(-1)

actuals = []

for d in test_dates:
    d = pd.to_datetime(d)

    try:
        nearest_idx = data.index.get_indexer([d], method='nearest')[0]
        nearest_date = data.index[nearest_idx]

        actual_return = data.loc[nearest_date]['return']

        # handle Series
        if hasattr(actual_return, "__len__"):
            actual_return = actual_return.iloc[0]

        # handle NaN
        if pd.isna(actual_return):
            actual_return = 0

    except:
        actual_return = 0

    actuals.append(actual_return)

df_results['actual_return'] = actuals

# =========================
# STEP 3 → DIRECTION
# =========================

df_results['pred_direction'] = (df_results['predicted_return'] > 0).astype(int)
df_results['actual_direction'] = (df_results['actual_return'] > 0).astype(int)

# =========================
# STEP 4 → ACCURACY
# =========================

accuracy = (df_results['pred_direction'] == df_results['actual_direction']).mean()

# =========================
# STEP 5 → STATS
# =========================

print("\n📊 Final Results:\n", df_results)

print("\n🎯 Direction Accuracy:", accuracy)

print("\n📈 Prediction Stats:\n", df_results['predicted_return'].describe())