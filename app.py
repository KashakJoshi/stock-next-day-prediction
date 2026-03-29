from fastapi import FastAPI
from prediction_engine.pipeline_run.run_pipeline import run_prediction_pipeline

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Stock Prediction API Running 🚀"}


@app.get("/predict")
def predict(ticker: str, date: str):
    result = run_prediction_pipeline(ticker, date)

    return {
        "ticker": ticker,
        "predicted_return": result['predicted_return'],
        "used_date": str(result['date']),
        "graphs": result['graphs']
    }