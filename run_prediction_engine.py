from prediction_engine.pipeline_run.run_pipeline import run_prediction_pipeline

output = run_prediction_pipeline(
    ticker="RELIANCE.NS",
    specified_date="2026-03-20"
)

print(output)