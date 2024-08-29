import math
import random
from typing import List

import numpy as np
import onnxruntime as rt

from mvp.server.core.game.MachineState import OperationalParameters

# Load the SVR pipeline from ONNX file
onnx_path = "mvp/server/core/analysis/artifacts/svr_pipeline_23_06_24.onnx"
session = rt.InferenceSession(onnx_path)


def default_rul_prediction_fn(current_timestep: int, parameters: OperationalParameters,
                              available_sensors: set[str] = None) -> int | None:
    return None


def svr_rul_prediction_fn(current_timestep: int, parameters: OperationalParameters,
                          purchased_sensors: List[str] | None = None) -> int | None:
    try:
        if purchased_sensors is None:
            purchased_sensors = []

        # Create input array with placeholder values
        x = np.array([
            [current_timestep],
            [100 * random.random()],
            [100 * random.random()],
            [100 * random.random()]
        ], dtype=np.float32)

        # Update input array with available sensor values
        if 'temperature' in purchased_sensors:
            x[1] = parameters.temperature
        if 'oil_age' in purchased_sensors:
            x[2] = parameters.oil_age
        if 'mechanical_wear' in purchased_sensors:
            x[3] = parameters.mechanical_wear

        # Reshape the input to match ONNX input requirements
        x = x.reshape(1, -1)

        # Make predictions using ONNX runtime
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        pred = session.run([output_name], {input_name: x})[0]

        return math.floor(pred)

    except Exception as e:
        print(f"Error in svr_rul_prediction_fn: {e}")
        return None
