from typing import Any

from pydantic import BaseModel

from mvp.server.core.machine import MachineState
from mvp.server.core.machine.OperationalParameters import OperationalParameters


class MachineStateDTO(BaseModel):
    operational_parameters: OperationalParameters
    predicted_rul: int | None

    def hide_sensor_data(self, sensor_name) -> None:
        if hasattr(self.operational_parameters, sensor_name):
            setattr(self.operational_parameters, sensor_name, None)

    def hide_prediction(self, prediction_name) -> None:
        if hasattr(self, prediction_name):
            setattr(self, prediction_name, None)

    @staticmethod
    def from_machine_state(machine_state: MachineState) -> "MachineStateDTO":
        return MachineStateDTO(
            operational_parameters=OperationalParameters(**machine_state.operational_parameters.to_dict()),
            predicted_rul=machine_state.predicted_rul,
        )

    @staticmethod
    def from_dict(json: dict[str, Any]) -> "MachineStateDTO":
        return MachineStateDTO(
            operational_parameters=OperationalParameters.from_dict(
                json.get("operational_parameters", {})
            ),
            predicted_rul=json.get("predicted_rul", None),
        )
