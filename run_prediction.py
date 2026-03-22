import src.utils.logger
from src.pipeline.prediction_pipeline import run_prediction_pipeline

result = run_prediction_pipeline(
    ticker="ITC.NS",
    date="2024-12-02"
)

print(result)