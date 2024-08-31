import math

import numpy as np
import onnxruntime as rt

# Load the SVR pipeline from ONNX file
onnx_path = "mvp/server/analysis/artifacts/svr_pipeline_23_06_24.onnx"
session = rt.InferenceSession(onnx_path)


def default_rul_prediction_fn(x: np.array) -> int | None:
    return None


def svr_rul_prediction_fn(x: np.array) -> int | None:
    try:
        # Reshape the input to match ONNX input requirements
        x = x.reshape(1, -1)

        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        pred = session.run([output_name], {input_name: x})[0]

        return math.floor(pred)

    except Exception as e:
        print(f"Error in svr_rul_prediction_fn: {e}")
        return None
