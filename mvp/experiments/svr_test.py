import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

history = pd.read_pickle("./history.pkl")

x = np.array(history["time"])
y = np.array(history["health_percentage"])

ax4 = (plt.figure()).add_subplot(1, 1, 1)
ax4.scatter(x, y, s=0.5)
ax4.set_title("Machine health vs time")
plt.show()

# Define feature columns and target column
feature_columns = ['time', 'temperature', 'oil_age', 'mechanical_wear']
target_column = 'health_percentage'

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
plt.title('Training Data: Time vs Health Percentage')
plt.xlabel('Time')
plt.ylabel('Health Percentage')
plt.legend()
plt.grid(True)

# Testing data
plt.subplot(1, 2, 2)
plt.scatter(X_test['time'], y_test, alpha=0.5, label='True Values')
plt.scatter(X_test['time'], y_test_pred, alpha=0.5, label='Predicted Values')
plt.title('Testing Data: Time vs Health Percentage')
plt.xlabel('Time')
plt.ylabel('Health Percentage')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

joblib.dump(svr_model, 'svr_model.pkl')
