from mvp.server.constants import OIL_AGE_MAPPING_MAX, TEMPERATURE_MAPPING_MAX, \
    MECHANICAL_WEAR_MAPPING_MAX
from mvp.server.math_utils import map_value


def compute_decay_speed(parameter_values: 'OperationalParameters') -> float:
    # TODO: calibrate these weights
    temperature_weight = 0.0005
    oil_age_weight = 0.001
    mechanical_wear_weight = 0.005

    # Made-up calculation involving operational parameters:  temperature, oil age, mechanical wear
    computed = parameter_values.temperature * temperature_weight + \
               parameter_values.oil_age * oil_age_weight + \
               parameter_values.mechanical_wear * mechanical_wear_weight

    mapping_max = TEMPERATURE_MAPPING_MAX * temperature_weight + \
                  OIL_AGE_MAPPING_MAX * oil_age_weight + \
                  MECHANICAL_WEAR_MAPPING_MAX * mechanical_wear_weight

    computed = min(mapping_max, computed)

    return map_value(computed, from_low=0, from_high=mapping_max, to_low=0, to_high=0.1)


def default_rul_prediction_fn(current_timestep: int) -> int | None:
    return None
