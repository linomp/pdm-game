import matplotlib.pyplot as plt
import pandas as pd
from darts import TimeSeries
from darts.models import ExponentialSmoothing

from mvp.server.core.constants import TIMESTEPS_PER_MOVE

full_history = pd.read_pickle("./history.pkl")
full_history.drop(columns=["predicted_rul"], inplace=True)
column_names = ["health_percentage"]

# Determine the number of windows based on the length of the full history
num_windows = (len(full_history) - TIMESTEPS_PER_MOVE * 3) // TIMESTEPS_PER_MOVE

# Initialize lists to store the full series and predictions
all_series = []
all_predictions = []

for window_index in range(num_windows):
    window_start = window_index * TIMESTEPS_PER_MOVE
    window_end = window_start + TIMESTEPS_PER_MOVE * 2

    if window_end > len(full_history):
        break

    history = full_history[window_start:window_end]

    for col in column_names:
        series = TimeSeries.from_dataframe(history, time_col='time', value_cols=col)

        train, val = series.split_after(window_end - TIMESTEPS_PER_MOVE)

        model = ExponentialSmoothing()
        model.fit(train)
        prediction = model.predict(len(val), num_samples=1)

        # Store the series and prediction
        all_series.append(series)
        all_predictions.append(prediction)

# Plot all series and predictions on the same plot
plt.figure(figsize=(12, 8))

for i, (series, prediction) in enumerate(zip(all_series, all_predictions)):
    if i == 0:
        series.plot(label=None, color='black', lw=0.5)
    else:
        series.plot(label=None, color='black', lw=0.5)
    prediction.plot(label=None, low_quantile=0.05, high_quantile=0.95, color='blue', linestyle='dotted')

plt.legend()
plt.title("Health percentage forecast every 24 steps")
plt.show()
