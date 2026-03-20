from src.components.data_ingestion import download_stock_data

download_stock_data(
    ticker="ITC.NS",
    start_date="2015-01-01",
    end_date="2024-12-31"
)