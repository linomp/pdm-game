import math
from typing import List

import joblib
import numpy as np

from mvp.server.core.machine.OperationalParameters import OperationalParameters

model = joblib.load("mvp/server/core/analysis/artifacts/svr_model.pkl")
scaler = joblib.load("mvp/server/core/analysis/artifacts/svr_scaler.pkl")


def default_rul_prediction_fn(current_timestep: int, parameters: OperationalParameters,
                              available_sensors: set[str] = None) -> int | None:
    return None


def svr_rul_prediction_fn(current_timestep: int, parameters: OperationalParameters,
                          purchased_sensors: List[str] | None = None) -> int | None:
    try:
        if purchased_sensors is None:
            purchased_sensors = []

        x = np.array([
            current_timestep,
            np.finfo(np.float64).max,
            np.finfo(np.float64).max,
            np.finfo(np.float64).max
        ], dtype=np.float64)

        if 'temperature' in purchased_sensors:
            x[1] = parameters.temperature
        if 'oil_age' in purchased_sensors:
            x[2] = parameters.oil_age
        if 'mechanical_wear' in purchased_sensors:
            x[3] = parameters.mechanical_wear

        x_scaled = scaler.transform([x])

        return math.floor(model.predict(x_scaled)[0])

    except Exception as e:
        print(f"Error in svr_rul_prediction_fn: {e}")
        return None
