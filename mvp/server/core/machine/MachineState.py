from typing import Any, Callable

from pydantic import BaseModel

from mvp.server.core.constants import TEMPERATURE_STARTING_POINT
from mvp.server.core.machine.OperationalParameters import OperationalParameters
from mvp.server.core.math_utils import exponential_decay


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

    def get_purchasable_sensors(self) -> set[str]:
        return self.operational_parameters.get_purchasable_sensors()

    def get_purchasable_predictions(self) -> set[str]:
        return {"predicted_rul"}

    def update_parameters(self, timestep: int):
        self.operational_parameters.update(timestep)
        self.health_percentage = self.compute_health_percentage(timestep)

    def update_prediction(self, timestep: int, rul_predictor: Callable[[int], int | None] = None,
                          latest_states=list['MachineState']):
        self.predicted_rul = rul_predictor(timestep)

    def compute_health_percentage(self, current_timestep: int) -> int:
        raw_value = round(
            exponential_decay(
                current_timestep,
                initial_value=self.health_percentage,
                decay_speed=self.operational_parameters.compute_decay_speed()
            )
        )
        return min(100, max(0, raw_value))

    def do_maintenance(self):
        self.operational_parameters = OperationalParameters(
            temperature=TEMPERATURE_STARTING_POINT,
            oil_age=0,
            mechanical_wear=self.operational_parameters.mechanical_wear / 100
        )
        # TODO: decide if it makes sense to restore some health percentage; maybe should be kept as is,
        #  maintenance does not mean  "new" machine, only slows down the decay
        self.health_percentage = min(100, max(0, round(self.health_percentage * 1.1)))

    def is_broken(self) -> bool:
        return self.health_percentage <= 0

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
