import math
import os

import matplotlib.pyplot as plt
import numpy as np
import onnxruntime as rt
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

feature_columns = ['time', 'temperature', 'oil_age', 'mechanical_wear']
target_column = 'rul'


def train(dataset: pd.DataFrame) -> str:
    X = dataset[feature_columns]
    y = dataset[target_column]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a pipeline that includes scaling and SVR
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('svr', SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1))
    ])

    # Train the pipeline
    pipeline.fit(X_train, y_train)

    # Make predictions
    y_train_pred = pipeline.predict(X_train)
    y_test_pred = pipeline.predict(X_test)

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

    # Convert the pipeline to ONNX
    initial_type = [('float_input', FloatTensorType([None, len(feature_columns)]))]
    onnx_model = convert_sklearn(pipeline, initial_types=initial_type)
    onnx_path = './artifacts/svr_pipeline.onnx'
    with open(onnx_path, 'wb') as f:
        f.write(onnx_model.SerializeToString())

    return onnx_path


def validate(dataset: pd.DataFrame, session: rt.InferenceSession):
    X = dataset[feature_columns].astype(np.float32)
    y_true = dataset[target_column]

    # Prepare input for ONNX model
    input_name = session.get_inputs()[0].name
    label_name = session.get_outputs()[0].name

    # Make predictions
    y_pred = session.run([label_name], {input_name: X.values})[0]

    # Evaluate the model
    test_mse = mean_squared_error(y_true, y_pred)
    test_r2 = r2_score(y_true, y_pred)

    print(f'Testing MSE: {test_mse}')
    print(f'Testing R^2: {test_r2}')

    # Plotting unscaled feature data vs health percentage and predictions
    plt.figure(figsize=(14, 8))
    plt.scatter(X['time'], y_true, alpha=0.5, label='True Values')
    plt.scatter(X['time'], y_pred, alpha=0.5, label='Predicted Values')
    plt.title(f'Testing Data: Time vs {target_column}')
    plt.xlabel('Time')
    plt.ylabel(f'{target_column}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    train_test_set = pd.read_pickle("./artifacts/train_test_run_to_failure.pkl")
    validation_set = pd.read_pickle("./artifacts/validation_set_run_to_failure.pkl")

    # train_test_set = pd.read_pickle("./artifacts/train_test_with_maintenance.pkl")
    # validation_set = pd.read_pickle("./artifacts/validation_set_with_maintenance.pkl")

    onnx_path = './artifacts/svr_pipeline.onnx'
    if os.path.exists(onnx_path):
        session = rt.InferenceSession(onnx_path)
        validate(validation_set, session)
    else:
        onnx_path = train(train_test_set)
        session = rt.InferenceSession(onnx_path)

    # Using the model to predict the RUL for a random example
    example = train_test_set.sample(1)
    example_input = example[feature_columns].astype(np.float32)
    example_pred = math.floor(session.run(None, {session.get_inputs()[0].name: example_input.values})[0][0].item())

    print("Example input:")
    print(example)
    print(f'Predicted RUL: {example_pred} (error = {abs(example_pred - example["rul"].values[0])} timesteps)\n')

    # Predict RUL with an incomplete input (e.g. when some sensor data is missing)
    example = train_test_set.sample(1)
    example.loc[:, 'temperature'] = np.finfo(np.float32).max
    # example.loc[:, 'oil_age'] = np.finfo(np.float32).max
    # example.loc[:, 'mechanical_wear'] = np.finfo(np.float32).max
    example_input = example[feature_columns].astype(np.float32)
    example_pred = math.floor(session.run(None, {session.get_inputs()[0].name: example_input.values})[0][0].item())

    print("Example input (corrupted):")
    print(example)
    print(f'Predicted RUL: {example_pred} (error = {abs(example_pred - example["rul"].values[0])} timesteps)')
