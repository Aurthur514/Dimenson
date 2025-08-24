import pandas as pd
import yfinance as yf
import joblib
import os
import json
from datetime import datetime, timedelta

# Note: For a real cloud deployment, consider packaging the model with the function
# or loading it from a cloud storage bucket.
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'crypto_model.joblib')

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

def get_trading_signal(ticker):
    """
    Fetches new data, preprocesses it, and generates a trading signal.
    Returns a dictionary with signal and status.
    """
    if not os.path.exists(MODEL_PATH):
        return {
            "status": "error",
            "message": f"Model not found at {MODEL_PATH}"
        }

    model = joblib.load(MODEL_PATH)

    # Fetch the last 100 days of data for feature calculation
    end_date = datetime.now()
    start_date = end_date - timedelta(days=100)

    try:
        new_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

        if new_data.empty:
            return {
                "status": "error",
                "message": "No new data fetched."
            }

        # If columns are a MultiIndex, flatten them to the first level
        if isinstance(new_data.columns, pd.MultiIndex):
            new_data.columns = new_data.columns.get_level_values(0)

        featured_data = calculate_technical_indicators(new_data.copy())
        latest_features = featured_data.iloc[-1:][['SMA_20', 'SMA_50', 'RSI']]

        if latest_features.isnull().values.any():
            return {
                "ticker": ticker,
                "timestamp": datetime.now().isoformat(),
                "signal": "HOLD",
                "status": "success",
                "message": "Not enough data to calculate features."
            }

        prediction = model.predict(latest_features)[0]
        signal = "BUY" if prediction == 1 else "SELL"

        return {
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "signal": signal,
            "status": "success",
            "features": latest_features.to_dict('records')[0]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def handler(request):
    """
    Cloud Function entry point.
    Can be triggered by an HTTP request.
    """
    # For simplicity, we'll use a fixed ticker.
    # In a real application, you might get the ticker from the request.
    # request_json = request.get_json(silent=True)
    # ticker = request_json.get('ticker', 'BTC-USD')

    ticker = 'BTC-USD'
    result = get_trading_signal(ticker)

    # Return a JSON response
    return json.dumps(result, indent=4), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    # This block allows local testing of the handler function.
    print("--- Crypto Trading Bot (Local Test) ---")

    # Mock request object for local testing
    class MockRequest:
        def get_json(self, silent=False):
            return {}

    response_data, status_code, headers = handler(MockRequest())

    print(f"Status Code: {status_code}")
    print("Response:")
    print(response_data)
    print("---------------------------------------")
