from src.utils.logger import logging
from src.utils.exception import CustomException
import sys

def safe_run(func):
    def wrapper(*args, **kwargs):
        try:
            logging.info(f"Started: {func.__name__}")
            result = func(*args, **kwargs)
            logging.info(f"Completed: {func.__name__}")
            return result
        except Exception as e:
            logging.error(f"Error in: {func.__name__}")
            raise CustomException(e, sys)
    return wrapper