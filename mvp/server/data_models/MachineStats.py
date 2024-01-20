import math
from typing import Any, Callable

from pydantic import BaseModel

from mvp.server.analysis import compute_decay_speed
from mvp.server.constants import TEMPERATURE_MAPPING_MAX, \
    TIMESTEPS_PER_MOVE, TEMPERATURE_STARTING_POINT, OIL_AGE_MAPPING_MAX, MECHANICAL_WEAR_MAPPING_MAX
from mvp.server.math_utils import map_value, linear_growth_with_reset, exponential_decay


class OperationalParameters(BaseModel):
    temperature: float
    oil_age: float
    mechanical_wear: float

    def update(self, current_timestep: int) -> None:
        self.temperature = self.compute_machine_temperature(current_timestep)
        self.oil_age = self.compute_oil_age(current_timestep)
        self.mechanical_wear = self.compute_mechanical_wear(current_timestep)

    def compute_machine_temperature(self, current_timestep: int) -> float:
        # temperature grows linearly over the 8 hours of a shift (resets every 8 hours)
        raw_value = linear_growth_with_reset(
            initial_value=0,
            period=TIMESTEPS_PER_MOVE,
            current_timestep=current_timestep
        )
        return map_value(
            raw_value,
            from_low=0,
            from_high=TIMESTEPS_PER_MOVE - 1,
            to_low=TEMPERATURE_STARTING_POINT,
            to_high=TEMPERATURE_MAPPING_MAX
        )

    def compute_oil_age(self, current_timestep: int) -> float:
        # oil age grows monotonically and resets only after every maintenance routine
        raw_value = self.oil_age + (current_timestep * self.temperature)
        return map_value(
            raw_value,
            from_low=self.oil_age,
            from_high=1e5,
            to_low=self.oil_age,
            to_high=OIL_AGE_MAPPING_MAX
        )

    def compute_mechanical_wear(self, current_timestep: int) -> float:
        # mechanical wear grows monotonically, directly proportional to oil ag.
        # for now it never resets (such that at some point, the machine will definitely break and game over)
        raw_value = math.exp(current_timestep) * self.oil_age / 1e6
        return map_value(
            raw_value,
            from_low=0,
            from_high=1e12,
            to_low=self.mechanical_wear,
            to_high=MECHANICAL_WEAR_MAPPING_MAX
        )

    def to_dict(self) -> dict[str, float]:
        return {
            "temperature": self.temperature,
            "oil_age": self.oil_age,
            "mechanical_wear": self.mechanical_wear
        }

    @staticmethod
    def from_dict(json: dict[str, float]) -> 'OperationalParameters':
        return OperationalParameters(
            temperature=json.get("temperature", 0),
            oil_age=json.get("oil_age", 0),
            mechanical_wear=json.get("mechanical_wear", 0)
        )


class MachineStats(BaseModel):
    predicted_rul: int | None = None
    health_percentage: int
    operational_parameters: OperationalParameters

    @staticmethod
    def new_machine_stats():
        return MachineStats(
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
            mechanical_wear=self.operational_parameters.mechanical_wear / 2
        )
        # TODO: confirm if it makes sense to reset the health percentage; maybe should be kept as is,
        #  maintenance does not mean  "new" machine, only slows down the decay
        # self.health_percentage = 100

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
        return MachineStats(
            predicted_rul=json.get("predicted_rul", None),
            health_percentage=json.get("health_percentage", 0),
            operational_parameters=OperationalParameters.from_dict(
                json.get("operational_parameters", {})
            )
        )

    def __str__(self):
        return (f"MachineStats(predicted_rul={self.predicted_rul}, health_percentage={self.health_percentage}, "
                f"operational_parameters={self.operational_parameters})")
