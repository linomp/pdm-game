from typing import Any, Callable

from pydantic import BaseModel

from mvp.server.core.constants import TEMPERATURE_STARTING_POINT, HEALTH_RECOVERY_FACTOR_ON_MAINTENANCE, \
    MECHANICAL_WEAR_REDUCTION_FACTOR_ON_MAINTENANCE
from mvp.server.core.machine.OperationalParameters import OperationalParameters
from mvp.server.core.math_utils import round_from_0_to_100


class MachineState(BaseModel):
    predicted_rul: int | None = None
    health_percentage: int
    operational_parameters: OperationalParameters

    @staticmethod
    def new_machine_state() -> "MachineState":
        return MachineState(
            health_percentage=100,
            operational_parameters=OperationalParameters(
                temperature=TEMPERATURE_STARTING_POINT,
                oil_age=0,
                mechanical_wear=0
            )
        )

    def get_purchasable_sensors(self) -> set[str]:
        return self.operational_parameters.get_purchasable_sensors()

    def get_purchasable_predictions(self) -> set[str]:
        return {"predicted_rul"}

    def update_parameters(self, timestep: int) -> None:
        self.operational_parameters.update(timestep)
        self.health_percentage = self.compute_health_percentage(timestep)

    def update_prediction(self, timestep: int, rul_predictor: Callable[[int], int | None] = None,
                          latest_states=list['MachineState']):
        self.predicted_rul = rul_predictor(timestep)

    def compute_health_percentage(self, current_timestep: int) -> int:
        return self.operational_parameters.compute_health_percentage(current_timestep, self.health_percentage)

    def do_maintenance(self) -> None:
        self.operational_parameters = OperationalParameters(
            temperature=TEMPERATURE_STARTING_POINT,
            oil_age=0,
            mechanical_wear=self.operational_parameters.mechanical_wear / MECHANICAL_WEAR_REDUCTION_FACTOR_ON_MAINTENANCE
        )
        self.health_percentage = round_from_0_to_100(self.health_percentage * HEALTH_RECOVERY_FACTOR_ON_MAINTENANCE)

    def is_broken(self) -> bool:
        # return self.health_percentage <= 0
        return True

    @staticmethod
    def from_dict(json: dict[str, Any]) -> "MachineState":
        return MachineState(
            predicted_rul=json.get("predicted_rul", None),
            health_percentage=json.get("health_percentage", 0),
            operational_parameters=OperationalParameters.from_dict(
                json.get("operational_parameters", {})
            )
        )

    def __str__(self) -> str:
        return (f"MachineState(predicted_rul={self.predicted_rul}, health_percentage={self.health_percentage}, "
                f"operational_parameters={self.operational_parameters})")
