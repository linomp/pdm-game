import math

from pydantic import BaseModel

from mvp.server.core.constants import *
from mvp.server.core.math_utils import linear_growth_with_reset, map_value


class OperationalParameters(BaseModel):
    temperature: float
    oil_age: float
    mechanical_wear: float

    def update(self, current_timestep: int) -> None:
        self.temperature = self.compute_machine_temperature(current_timestep)
        self.oil_age = self.compute_oil_age(current_timestep)
        self.mechanical_wear = self.compute_mechanical_wear(current_timestep)

    def compute_decay_speed(self) -> float:
        # TODO: calibrate these weights
        temperature_weight = 0.0005
        oil_age_weight = 0.001
        mechanical_wear_weight = 0.005

        # Made-up calculation involving operational parameters:  temperature, oil age, mechanical wear
        computed = self.temperature * temperature_weight + \
                   self.oil_age * oil_age_weight + \
                   self.mechanical_wear * mechanical_wear_weight

        mapping_max = TEMPERATURE_MAPPING_MAX * temperature_weight + \
                      OIL_AGE_MAPPING_MAX * oil_age_weight + \
                      MECHANICAL_WEAR_MAPPING_MAX * mechanical_wear_weight

        computed = min(mapping_max, computed)

        return map_value(computed, from_low=0, from_high=mapping_max, to_low=0, to_high=0.1)

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
        raw_value = min(1e6, self.oil_age + (current_timestep * self.temperature))
        return map_value(
            raw_value,
            from_low=self.oil_age,
            from_high=1e6,
            to_low=self.oil_age,
            to_high=OIL_AGE_MAPPING_MAX
        )

    def compute_mechanical_wear(self, current_timestep: int) -> float:
        # mechanical wear grows monotonically, directly proportional to oil ag.
        # for now it never resets (such that at some point, the machine will definitely break and game over)
        raw_value = min(1e6, math.exp(current_timestep) * self.oil_age / 1e16)
        return map_value(
            raw_value,
            from_low=0,
            from_high=1e6,
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
