import pandas as pd
import os

def calculate_technical_indicators(data):
    """
    Calculates technical indicators and adds them to the dataframe.
    """
    # Simple Moving Averages (SMA)
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()

    # Relative Strength Index (RSI)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    return data

def create_target_variable(data):
    """
    Creates the target variable for prediction.
    Target = 1 if the next day's closing price is higher than today's, 0 otherwise.
    """
    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
    return data

def process_data(input_filepath, output_filepath):
    """
    Loads raw data, adds features and a target, and saves the processed data.
    """
    if not os.path.exists(input_filepath):
        print(f"Error: Input file not found at {input_filepath}")
        return

    # Load the raw data, skipping the first 2 metadata rows and manually setting header
    data = pd.read_csv(input_filepath, index_col=0, parse_dates=True, skiprows=3, header=None)
    data.columns = ['Close', 'High', 'Low', 'Open', 'Volume']

    # Calculate technical indicators
    data = calculate_technical_indicators(data)

    # Create the target variable
    data = create_target_variable(data)

    # Drop rows with NaN values created by rolling windows or shifts
    data.dropna(inplace=True)

    # Save the processed data
    output_dir = os.path.dirname(output_filepath)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data.to_csv(output_filepath)
    print(f"Processed data with features saved to {output_filepath}")

if __name__ == '__main__':
    # --- Configuration ---
    INPUT_FILE = 'crypto_trader/data/BTC-USD_history.csv'
    OUTPUT_FILE = 'crypto_trader/data/BTC-USD_features.csv'

    # --- Execution ---
    process_data(INPUT_FILE, OUTPUT_FILE)
