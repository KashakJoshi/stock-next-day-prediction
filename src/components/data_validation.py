import os
import pandas as pd
import logging
from src.exception import CustomException
import sys
from src.utils.common import safe_run


@safe_run
def validate_data(file_path: str):
    
    logging.info("Starting data validation")

    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    required_columns = ["Close", "High", "Low", "Open", "Volume"]

    for col in required_columns:
        if col not in df.columns:
            raise Exception(f"Missing column: {col}")

    if df.isnull().sum().sum() > 100:
        raise Exception("Too many missing values")

    logging.info("Data validation completed successfully")

    return True