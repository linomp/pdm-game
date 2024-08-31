from typing import Any

from pydantic import BaseModel

from mvp.server.core.Machine import Machine


class MachineDTO(BaseModel):
    temperature: float | None
    oil_age: float | None
    mechanical_wear: float | None
    predicted_rul: int | None

    def hide_sensor_data(self, sensor_name: str) -> None:
        if hasattr(self, sensor_name):
            setattr(self, sensor_name, None)

    def hide_prediction(self, prediction_name: str) -> None:
        if hasattr(self, prediction_name):
            setattr(self, prediction_name, None)

    @staticmethod
    def from_machine(machine: Machine) -> "MachineDTO":
        return MachineDTO(
            temperature=machine.temperature,
            oil_age=machine.oil_age,
            mechanical_wear=machine.mechanical_wear,
            predicted_rul=machine.predicted_rul
        )

    @staticmethod
    def from_dict(json: dict[str, Any]) -> "MachineDTO":
        return MachineDTO(
            temperature=json.get("temperature", None),
            oil_age=json.get("oil_age", None),
            mechanical_wear=json.get("mechanical_wear", None),
            predicted_rul=json.get("predicted_rul", None)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "temperature": self.temperature,
            "oil_age": self.oil_age,
            "mechanical_wear": self.mechanical_wear,
            "predicted_rul": self.predicted_rul
        }

    def __str__(self) -> str:
        return (f"MachineDTO(temperature={self.temperature}, oil_age={self.oil_age}, "
                f"mechanical_wear={self.mechanical_wear}, predicted_rul={self.predicted_rul}")
