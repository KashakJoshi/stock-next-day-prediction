from src.pipeline.training_pipeline import run_training_pipeline
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

run_training_pipeline("ITC.NS")