import yfinance as yf
import pandas as pd
import os
import sys

from src.utils.logger import logging
from src.utils.exception import CustomException
from src.utils.common import safe_run


@safe_run
def download_stock_data(ticker: str, start_date: str, end_date: str):
    try:
        logging.info(f"Downloading data for {ticker} till {end_date}")

        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        os.makedirs("artifacts/raw", exist_ok=True)

        file_path = f"artifacts/raw/{ticker.replace('.', '_')}.csv"

        data.to_csv(file_path)

        logging.info(f"Data saved at {file_path}")

        return file_path

    except Exception as e:
        raise CustomException(e, sys)


@safe_run
def update_latest_data(ticker: str):
    try:
        logging.info(f"Updating latest data for {ticker}")

        latest_data = yf.download(ticker, period="5d")

        file_path = f"artifacts/raw/{ticker.replace('.', '_')}.csv"

        if os.path.exists(file_path):

            old_data = pd.read_csv(file_path, index_col=0)

            updated = pd.concat([old_data, latest_data])

            updated = updated[~updated.index.duplicated(keep="last")]

            updated.to_csv(file_path)

            logging.info("Latest data appended successfully")

        else:
            latest_data.to_csv(file_path)

        return file_path

    except Exception as e:
        raise CustomException(e, sys)