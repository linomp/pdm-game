import math
import random
from typing import Any, Callable

import numpy as np
from pydantic import BaseModel

from mvp.server.core.constants import *
from mvp.server.core.math_utils import (
    constrain_from_0_to_100, linear_growth_with_reset, map_value, exponential_decay
)


def get_purchasable_sensors() -> set[str]:
    return {"temperature", "oil_age", "mechanical_wear"}


def get_purchasable_predictions() -> set[str]:
    return {"predicted_rul"}


class Machine(BaseModel):
    predicted_rul: int | None = None
    health_percentage: float = 100.0
    temperature: float | None = TEMPERATURE_STARTING_POINT
    oil_age: float | None = 0
    mechanical_wear: float | None = 0

    def do_maintenance(self) -> None:
        self.temperature = TEMPERATURE_STARTING_POINT
        self.oil_age = 0
        self.mechanical_wear /= MECHANICAL_WEAR_REDUCTION_FACTOR_ON_MAINTENANCE
        self.health_percentage = constrain_from_0_to_100(self.health_percentage * HEALTH_RECOVERY_FACTOR_ON_MAINTENANCE)

    def is_broken(self) -> bool:
        return self.health_percentage <= 0

    def update_parameters(self, timestep: int) -> None:
        self.temperature = self.compute_machine_temperature(timestep)
        self.oil_age = self.compute_oil_age(timestep)
        self.mechanical_wear = self.compute_mechanical_wear(timestep)
        self.health_percentage = self.compute_health_percentage(timestep)

    def update_prediction(self, timestep: int,
                          rul_predictor: Callable[[np.array], int | None] = None,
                          available_sensors: list[str] = None) -> None:
        if available_sensors is None:
            available_sensors = []

        feature_vec = np.array([
            [timestep],
            [100 * random.random()],
            [100 * random.random()],
            [100 * random.random()]
        ], dtype=np.float32)

        if 'temperature' in available_sensors:
            feature_vec[1] = self.temperature
        if 'oil_age' in available_sensors:
            feature_vec[2] = self.oil_age
        if 'mechanical_wear' in available_sensors:
            feature_vec[3] = self.mechanical_wear

        self.predicted_rul = rul_predictor(feature_vec)

    def compute_health_percentage(self, timestep: int) -> float:
        raw_value = round(
            exponential_decay(
                timestep,
                initial_value=self.health_percentage,
                decay_speed=self.compute_decay_speed()
            )
        )

        raw_value -= random.random() * (0.005 * raw_value)

        return constrain_from_0_to_100(raw_value)

    def compute_decay_speed(self) -> float:
        temperature_weight = 0.01
        oil_age_weight = 0.001
        mechanical_wear_weight = 0.1

        # Made-up calculation involving operational parameters:  temperature, oil age, mechanical wear
        computed = (self.temperature * temperature_weight +
                    self.oil_age * oil_age_weight +
                    self.mechanical_wear * mechanical_wear_weight)

        mapping_max = (TEMPERATURE_MAPPING_MAX * temperature_weight +
                       OIL_AGE_MAPPING_MAX * oil_age_weight +
                       MECHANICAL_WEAR_MAPPING_MAX * mechanical_wear_weight)

        computed = min(mapping_max, computed)

        return map_value(computed, from_low=0, from_high=mapping_max, to_low=0, to_high=0.005)

    def compute_machine_temperature(self, timestep: int) -> float:
        # temperature grows linearly over the 8 hours of a shift (resets every 8 hours)
        raw_value = self.mechanical_wear * linear_growth_with_reset(
            initial_value=0,
            period=TIMESTEPS_PER_MOVE,
            current_timestep=timestep
        )

        raw_value += random.random() * raw_value

        return map_value(
            raw_value,
            from_low=0,
            from_high=TIMESTEPS_PER_MOVE - 1,
            to_low=TEMPERATURE_STARTING_POINT,
            to_high=TEMPERATURE_MAPPING_MAX
        )

    def compute_oil_age(self, timestep: int) -> float:
        # oil age grows monotonically and resets only after every maintenance routine
        raw_value = min(1e6, self.oil_age + ((timestep / 1000) * (self.temperature ** 2)))
        raw_value += random.random() * raw_value

        return map_value(
            raw_value,
            from_low=self.oil_age,
            from_high=1e6,
            to_low=self.oil_age,
            to_high=OIL_AGE_MAPPING_MAX
        )

    def compute_mechanical_wear(self, timestep: int) -> float:
        # mechanical wear grows monotonically, directly proportional to oil ag.
        # for now it never resets (such that at some point, the machine will definitely break and game over)
        raw_value = min(1e6, math.exp(timestep / 200) * self.oil_age)
        raw_value += random.random() * raw_value

        return map_value(
            raw_value,
            from_low=0,
            from_high=1e6,
            to_low=self.mechanical_wear,
            to_high=MECHANICAL_WEAR_MAPPING_MAX
        )

    @staticmethod
    def new_machine() -> "Machine":
        return Machine(
            health_percentage=100.0,
            temperature=TEMPERATURE_STARTING_POINT,
            oil_age=0,
            mechanical_wear=0
        )

    @staticmethod
    def from_dict(json: dict[str, Any]) -> "Machine":
        return Machine(
            predicted_rul=json.get("predicted_rul", None),
            health_percentage=json.get("health_percentage", 100.0),
            temperature=json.get("temperature", TEMPERATURE_STARTING_POINT),
            oil_age=json.get("oil_age", 0),
            mechanical_wear=json.get("mechanical_wear", 0)
        )

    def to_dict(self) -> dict[str, float]:
        return {
            "predicted_rul": self.predicted_rul,
            "health_percentage": self.health_percentage,
            "temperature": self.temperature,
            "oil_age": self.oil_age,
            "mechanical_wear": self.mechanical_wear
        }

    def __str__(self) -> str:
        return (f"Machine(predicted_rul={self.predicted_rul}, health_percentage={self.health_percentage}, "
                f"temperature={self.temperature}, oil_age={self.oil_age}, "
                f"mechanical_wear={self.mechanical_wear})")
