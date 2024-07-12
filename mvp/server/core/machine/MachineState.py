import math
import random
from typing import Any, Callable

from pydantic import BaseModel

from mvp.server.core.constants import *
from mvp.server.core.math_utils import linear_growth_with_reset, map_value, exponential_decay, constrain_from_0_to_100


class OperationalParameters(BaseModel):
    temperature: float | None
    oil_age: float | None
    mechanical_wear: float | None

    def get_purchasable_sensors(self) -> set[str]:
        return self.model_fields_set

    def update(self, current_timestep: int) -> None:
        self.temperature = self.compute_machine_temperature(current_timestep)
        self.oil_age = self.compute_oil_age(current_timestep)
        self.mechanical_wear = self.compute_mechanical_wear(current_timestep)

    def compute_health_percentage(self, current_timestep: int, current_health: float) -> float:
        raw_value = round(
            exponential_decay(
                current_timestep,
                initial_value=current_health,
                decay_speed=self.compute_decay_speed()
            )
        )

        raw_value -= random.random() * (0.005 * raw_value)

        return constrain_from_0_to_100(raw_value)

    def compute_decay_speed(self) -> float:
        # TODO: calibrate these weights
        temperature_weight = 0.01
        oil_age_weight = 0.001
        mechanical_wear_weight = 0.1

        # Made-up calculation involving operational parameters:  temperature, oil age, mechanical wear
        computed = self.temperature * temperature_weight + \
                   self.oil_age * oil_age_weight + \
                   self.mechanical_wear * mechanical_wear_weight

        mapping_max = TEMPERATURE_MAPPING_MAX * temperature_weight + \
                      OIL_AGE_MAPPING_MAX * oil_age_weight + \
                      MECHANICAL_WEAR_MAPPING_MAX * mechanical_wear_weight

        computed = min(mapping_max, computed)

        return map_value(computed, from_low=0, from_high=mapping_max, to_low=0, to_high=0.005)

    def compute_machine_temperature(self, current_timestep: int) -> float:
        # temperature grows linearly over the 8 hours of a shift (resets every 8 hours)
        raw_value = self.mechanical_wear * linear_growth_with_reset(
            initial_value=0,
            period=TIMESTEPS_PER_MOVE,
            current_timestep=current_timestep
        )

        raw_value -= random.random() * raw_value

        return map_value(
            raw_value,
            from_low=0,
            from_high=TIMESTEPS_PER_MOVE - 1,
            to_low=TEMPERATURE_STARTING_POINT,
            to_high=TEMPERATURE_MAPPING_MAX
        )

    def compute_oil_age(self, current_timestep: int) -> float:
        # oil age grows monotonically and resets only after every maintenance routine
        raw_value = min(1e6, self.oil_age + ((current_timestep / 1000) * (self.temperature ** 2)))
        raw_value += random.random() * raw_value

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
        raw_value = min(1e6, math.exp(current_timestep / 200) * self.oil_age)
        raw_value += random.random() * raw_value

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


class MachineState(BaseModel):
    predicted_rul: int | None = None
    health_percentage: float
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

    def update_prediction(self, timestep: int,
                          rul_predictor: Callable[[int, OperationalParameters, list[str]], int | None] = None,
                          available_sensors: list[str] = None
                          ) -> None:
        self.predicted_rul = rul_predictor(timestep, self.operational_parameters, available_sensors)

    def compute_health_percentage(self, current_timestep: int) -> float:
        return self.operational_parameters.compute_health_percentage(current_timestep, self.health_percentage)

    def do_maintenance(self) -> None:
        self.operational_parameters = OperationalParameters(
            temperature=TEMPERATURE_STARTING_POINT,
            oil_age=0,
            mechanical_wear=self.operational_parameters.mechanical_wear / MECHANICAL_WEAR_REDUCTION_FACTOR_ON_MAINTENANCE
        )
        self.health_percentage = constrain_from_0_to_100(self.health_percentage * HEALTH_RECOVERY_FACTOR_ON_MAINTENANCE)

    def is_broken(self) -> bool:
        return self.health_percentage <= 0

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
