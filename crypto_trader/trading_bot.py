import pandas as pd
import yfinance as yf
import joblib
import os
from datetime import datetime, timedelta

def calculate_technical_indicators(data):
    """
    Calculates technical indicators for the new data.
    """
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()

    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    return data

def get_trading_signal(ticker, model_path):
    """
    Fetches new data, preprocesses it, and generates a trading signal.
    """
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        return "ERROR"

    # Load the trained model
    model = joblib.load(model_path)

    # Fetch the last 100 days of data to have enough for feature calculation
    end_date = datetime.now()
    start_date = end_date - timedelta(days=100)

    try:
        print(f"Fetching latest data for {ticker}...")
        new_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

        if new_data.empty:
            print("No new data fetched. Cannot generate a signal.")
            return "HOLD"

        # Calculate features
        featured_data = calculate_technical_indicators(new_data.copy())

        # Get the most recent data point for prediction
        latest_features = featured_data.iloc[-1:][['SMA_20', 'SMA_50', 'RSI']]

        if latest_features.isnull().values.any():
            print("Not enough data to calculate features. Holding.")
            return "HOLD"

        # Make a prediction
        prediction = model.predict(latest_features)[0]

        # Generate signal
        if prediction == 1:
            signal = "BUY"
        else:
            signal = "SELL"

        return signal

    except Exception as e:
        print(f"An error occurred during signal generation: {e}")
        return "ERROR"

if __name__ == '__main__':
    # --- Configuration ---
    TICKER_SYMBOL = 'BTC-USD'
    MODEL_FILE_PATH = 'crypto_trader/models/crypto_model.joblib'

    # --- Execution ---
    print("--- Crypto Trading Bot ---")
    trading_signal = get_trading_signal(TICKER_SYMBOL, MODEL_FILE_PATH)

    print(f"\nTicker: {TICKER_SYMBOL}")
    print(f"Generated Signal: {trading_signal}")

    if trading_signal == "BUY":
        print("Action: Execute BUY order (simulation).")
    elif trading_signal == "SELL":
        print("Action: Execute SELL order (simulation).")
    else:
        print("Action: No trade (HOLD or an error occurred).")

    print("--------------------------")
