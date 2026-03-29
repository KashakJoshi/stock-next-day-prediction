from prediction_engine.pipeline_run.run_pipeline import run_prediction_pipeline

ticker = "RELIANCE.NS"
specified_date = "2025-01-26"

output = run_prediction_pipeline(
    ticker=ticker,
    specified_date=specified_date
)

print(output)