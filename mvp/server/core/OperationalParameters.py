import math

from pydantic import BaseModel

from mvp.server.constants import TIMESTEPS_PER_MOVE, TEMPERATURE_STARTING_POINT, TEMPERATURE_MAPPING_MAX, \
    OIL_AGE_MAPPING_MAX, MECHANICAL_WEAR_MAPPING_MAX
from mvp.server.math_utils import linear_growth_with_reset, map_value


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