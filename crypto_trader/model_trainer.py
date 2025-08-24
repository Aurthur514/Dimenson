import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os

def train_model(input_filepath, model_dir="crypto_trader/models"):
    """
    Trains a classification model and saves it.
    """
    if not os.path.exists(input_filepath):
        print(f"Error: Input file not found at {input_filepath}")
        return

    # Load the processed data
    data = pd.read_csv(input_filepath, index_col=0, parse_dates=True)

    # Define features (X) and target (y)
    features = ['SMA_20', 'SMA_50', 'RSI']
    target = 'Target'

    X = data[features]
    y = data[target]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )

    # Initialize and train the model
    print("Training the RandomForestClassifier model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")

    # Save the trained model
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_filepath = os.path.join(model_dir, 'crypto_model.joblib')
    joblib.dump(model, model_filepath)
    print(f"Model saved to {model_filepath}")

if __name__ == '__main__':
    # --- Configuration ---
    INPUT_FILE = 'crypto_trader/data/BTC-USD_features.csv'

    # --- Execution ---
    train_model(INPUT_FILE)
