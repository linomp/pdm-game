import math
from typing import Any, Callable

from pydantic import BaseModel

from mvp.server.analysis import compute_decay_speed
from mvp.server.constants import OIL_AGE_MAPPING_MAX, TEMPERATURE_MAPPING_MAX, \
    MECHANICAL_WEAR_MAPPING_MAX, TIMESTEPS_PER_MOVE, TEMPERATURE_STARTING_POINT
from mvp.server.math_utils import map_value, linear_growth_with_reset, exponential_decay


class OperationalParameters(BaseModel):
    temperature: float
    oil_age: float
    mechanical_wear: float

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
    def new_machine_stats(current_step: int):
        return MachineStats(
            health_percentage=100,
            operational_parameters=OperationalParameters(
                temperature=TEMPERATURE_STARTING_POINT,
                oil_age=0,
                mechanical_wear=0
            )
        )

    def is_broken(self) -> bool:
        if self.health_percentage <= 0:
            return True

        if self.predicted_rul is not None and self.predicted_rul <= 0:
            return True

        return False

    def update_stats_and_parameters(self, timestep: int, rul_predictor: Callable[[int], int | None] = None):
        self.operational_parameters = self.get_operational_parameters(timestep)
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
        # return round(map_value(raw_value, from_low=0, from_high=sys.float_info.max, to_low=0, to_high=100))
        return min(100, max(0, raw_value))

    def get_operational_parameters(self, current_timestep: int) -> OperationalParameters:
        temperature = self.get_machine_temperature(current_timestep)
        oil_age = self.get_oil_age(current_timestep, temperature, initial_value=self.operational_parameters.oil_age)
        return OperationalParameters(
            temperature=temperature,
            oil_age=oil_age,
            mechanical_wear=self.get_mechanical_wear(current_timestep, oil_age)
        )

    def get_machine_temperature(self, current_timestep: int) -> float:
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

    def get_oil_age(self, current_timestep: int, machine_temperature: float, initial_value: float) -> float:
        # oil age grows monotonically and resets only after every maintenance routine
        raw_value = initial_value + (current_timestep * machine_temperature)
        return map_value(raw_value, from_low=0, from_high=1e5, to_low=0, to_high=OIL_AGE_MAPPING_MAX)

    def get_mechanical_wear(self, current_timestep: int, oil_age: float) -> float:
        # mechanical wear grows monotonically, directly proportional to oil ag.
        # for now it never resets (such that at some point, the machine will definitely break and game over)
        raw_value = math.exp(current_timestep) * oil_age / 1e6
        return map_value(raw_value, from_low=0, from_high=1e12, to_low=0, to_high=MECHANICAL_WEAR_MAPPING_MAX)

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
