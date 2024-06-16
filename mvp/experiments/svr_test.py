import math
import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR


def train(history: pd.DataFrame) -> tuple[SVR, StandardScaler]:
    feature_columns = ['time', 'temperature', 'oil_age', 'mechanical_wear']
    target_column = 'rul'

    X = history[feature_columns]
    y = history[target_column]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize and train the SVR model
    svr_model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
    svr_model.fit(X_train_scaled, y_train)

    # Make predictions
    y_train_pred = svr_model.predict(X_train_scaled)
    y_test_pred = svr_model.predict(X_test_scaled)

    # Evaluate the model
    train_mse = mean_squared_error(y_train, y_train_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)

    print(f'Training MSE: {train_mse}')
    print(f'Testing MSE: {test_mse}')
    print(f'Training R^2: {train_r2}')
    print(f'Testing R^2: {test_r2}')

    # Plotting unscaled feature data vs health percentage and predictions
    plt.figure(figsize=(14, 8))

    # Training data
    plt.subplot(1, 2, 1)
    plt.scatter(X_train['time'], y_train, alpha=0.5, label='True Values')
    plt.scatter(X_train['time'], y_train_pred, alpha=0.5, label='Predicted Values')
    plt.title(f'Training Data: Time vs {target_column}')
    plt.xlabel('Time')
    plt.ylabel(f'{target_column}')
    plt.legend()
    plt.grid(True)

    # Testing data
    plt.subplot(1, 2, 2)
    plt.scatter(X_test['time'], y_test, alpha=0.5, label='True Values')
    plt.scatter(X_test['time'], y_test_pred, alpha=0.5, label='Predicted Values')
    plt.title(f'Testing Data: Time vs {target_column}')
    plt.xlabel('Time')
    plt.ylabel(f'{target_column}')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    joblib.dump(svr_model, './artifacts/svr_model.pkl')
    joblib.dump(scaler, './artifacts/svr_scaler.pkl')

    return svr_model, scaler


def validate(history: pd.DataFrame, svr_model: SVR, scaler: StandardScaler):
    # Define feature columns and target column
    feature_columns = ['time', 'temperature', 'oil_age', 'mechanical_wear']
    target_column = 'rul'

    X = history[feature_columns]
    y = history[target_column]

    # Split the data into training and testing sets
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features & make predictions
    X_test_scaled = scaler.transform(X_test)
    y_test_pred = svr_model.predict(X_test_scaled)

    # Evaluate the model
    test_mse = mean_squared_error(y_test, y_test_pred)
    test_r2 = r2_score(y_test, y_test_pred)

    print(f'Testing MSE: {test_mse}')
    print(f'Testing R^2: {test_r2}')

    # Plotting unscaled feature data vs health percentage and predictions
    plt.figure(figsize=(14, 8))
    plt.scatter(X_test['time'], y_test, alpha=0.5, label='True Values')
    plt.scatter(X_test['time'], y_test_pred, alpha=0.5, label='Predicted Values')
    plt.title(f'Testing Data: Time vs {target_column}')
    plt.xlabel('Time')
    plt.ylabel(f'{target_column}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # history = pd.read_pickle("./artifacts/history_run_to_failure.pkl")
    history = pd.read_pickle("./artifacts/history_with_maintenance.pkl")

    if os.path.exists('./artifacts/svr_model.pkl') and os.path.exists('./artifacts/svr_scaler.pkl'):
        model = joblib.load('./artifacts/svr_model.pkl')
        scaler = joblib.load('./artifacts/svr_scaler.pkl')
        validate(history, model, scaler)
    else:
        model, scaler = train(history)

    # Using the model to predict the RUL for a random example
    example = history.sample(1)
    example_scaled = scaler.transform(example[['time', 'temperature', 'oil_age', 'mechanical_wear']])
    example_pred = math.floor(model.predict(example_scaled)[0])

    print("Example input:")
    print(example)
    print(f'Predicted RUL: {example_pred} (error = {abs(example_pred - example["rul"].values[0])} timesteps)\n')

    # Predict RUL with an incomplete input (e.g. when some sensor data is missing)
    example = history.sample(1)
    example.loc[:, 'temperature'] = np.finfo(np.float64).max
    # example.loc[:, 'oil_age'] = np.finfo(np.float64).max
    # example.loc[:, 'mechanical_wear'] = np.finfo(np.float64).max
    example_scaled = scaler.transform(example[['time', 'temperature', 'oil_age', 'mechanical_wear']])
    example_pred = math.floor(model.predict(example_scaled)[0])

    print("Example input (corrupted):")
    print(example)
    print(f'Predicted RUL: {example_pred} (error = {abs(example_pred - example["rul"].values[0])} timesteps)')
