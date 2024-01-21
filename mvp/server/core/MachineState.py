from typing import Any, Callable

from pydantic import BaseModel

from mvp.server.analysis import compute_decay_speed
from mvp.server.constants import TEMPERATURE_STARTING_POINT
from mvp.server.core.OperationalParameters import OperationalParameters
from mvp.server.math_utils import exponential_decay


class MachineState(BaseModel):
    predicted_rul: int | None = None
    health_percentage: int
    operational_parameters: OperationalParameters

    @staticmethod
    def new_machine_state():
        return MachineState(
            health_percentage=100,
            operational_parameters=OperationalParameters(
                temperature=TEMPERATURE_STARTING_POINT,
                oil_age=0,
                mechanical_wear=0
            )
        )

    def is_broken(self) -> bool:
        return self.health_percentage <= 0

    def simulate_maintenance(self):
        self.operational_parameters = OperationalParameters(
            temperature=TEMPERATURE_STARTING_POINT,
            oil_age=0,
            mechanical_wear=self.operational_parameters.mechanical_wear / 10
        )
        # TODO: decide if it makes sense to restore some health percentage; maybe should be kept as is,
        #  maintenance does not mean  "new" machine, only slows down the decay
        self.health_percentage = min(100, max(0, round(self.health_percentage * 1.05)))

    def update_stats_and_parameters(self, timestep: int, rul_predictor: Callable[[int], int | None] = None):
        self.operational_parameters.update(timestep)
        self.health_percentage = self.get_health_percentage(timestep)
        self.predicted_rul = rul_predictor(timestep)

    def get_health_percentage(self, current_timestep: int) -> int:
        health_decay_speed = compute_decay_speed(self.operational_parameters)
        raw_value = round(
            exponential_decay(
                current_timestep,
                initial_value=self.health_percentage,
                decay_speed=health_decay_speed
            )
        )
        return min(100, max(0, raw_value))

    @staticmethod
    def from_dict(json: dict[str, Any]):
        return MachineState(
            predicted_rul=json.get("predicted_rul", None),
            health_percentage=json.get("health_percentage", 0),
            operational_parameters=OperationalParameters.from_dict(
                json.get("operational_parameters", {})
            )
        )

    def __str__(self):
        return (f"MachineState(predicted_rul={self.predicted_rul}, health_percentage={self.health_percentage}, "
                f"operational_parameters={self.operational_parameters})")
