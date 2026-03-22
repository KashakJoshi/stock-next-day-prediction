from prediction_engine.pipeline_run.run_pipeline import run_prediction_pipeline


if __name__ == "__main__":
    
    ticker = "ITC.NS"
    prediction_date = "2024-01-01"
    
    run_prediction_pipeline(ticker, prediction_date)