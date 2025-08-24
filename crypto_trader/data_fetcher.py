import yfinance as yf
import pandas as pd
import os

def fetch_data(ticker, start_date, end_date, data_dir="data"):
    """
    Fetches historical market data for a given ticker and saves it to a CSV file.

    Args:
        ticker (str): The ticker symbol to fetch (e.g., 'BTC-USD').
        start_date (str): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the data in 'YYYY-MM-DD' format.
        data_dir (str): The directory where the data will be saved.

    Returns:
        str: The path to the saved CSV file, or None if fetching fails.
    """
    # Create the data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    filepath = os.path.join(data_dir, f"{ticker}_history.csv")

    try:
        print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
        # Download data from Yahoo Finance
        data = yf.download(ticker, start=start_date, end=end_date)

        if data.empty:
            print(f"No data found for ticker {ticker}. It might be delisted or the ticker is incorrect.")
            return None

        # Save the data to a CSV file
        data.to_csv(filepath)
        print(f"Data successfully saved to {filepath}")
        return filepath

    except Exception as e:
        print(f"An error occurred while fetching data for {ticker}: {e}")
        return None

if __name__ == '__main__':
    # --- Configuration ---
    TICKER_SYMBOL = 'BTC-USD'
    START_DATE = '2018-01-01'
    END_DATE = '2023-12-31'
    DATA_DIRECTORY = 'crypto_trader/data'

    # --- Execution ---
    fetch_data(TICKER_SYMBOL, START_DATE, END_DATE, data_dir=DATA_DIRECTORY)
