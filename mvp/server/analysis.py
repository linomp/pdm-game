import math

from mvp.server.constants import TIMESTEPS_PER_MOVE


def get_health_percentage(current_timestep: int, initial_value=100) -> int:
    health_decay_speed = compute_decay_speed(current_timestep)
    raw_val = round(exponential_decay(current_timestep, initial_value=initial_value, decay_speed=health_decay_speed))
    return min(100, max(0, raw_val))


def exponential_decay(t: int, initial_value: int, decay_speed: float) -> float:
    return initial_value - math.exp(t * decay_speed)


def compute_decay_speed(t: int) -> float:
    # Made-up calculation involving operational parameters:  temperature, oil age, mechanical wear
    # - temperature grows linearly over the 8 hours of a shift (resets every 8 hours)
    # - oil age grows monotonically, directly proportional to temperature and resets only after every maintenance routine
    # - mechanical wear grows monotonically, directly proportional to oil age, for now it never resets (such that at some point, the machine will definitely break and game over)

    parameter_values = get_parameter_values(t)

    # TODO: calibrate these weights
    computed = parameter_values["temperature"] * 0.01 + parameter_values["oil_age"] * 0.01 + parameter_values[
        "mechanical_wear"] * 0.01

    # decay speed will always bet between 0.1 and 0.2
    return min(computed / 3, 0.3)


def get_parameter_values(current_timestep: int) -> dict[str, float]:
    return {
        "temperature": get_machine_temperature(current_timestep),
        "oil_age": get_oil_age(current_timestep),
        "mechanical_wear": get_mechanical_wear(current_timestep)
    }


def get_machine_temperature(t: int) -> float:
    return max(0, t - 1) % TIMESTEPS_PER_MOVE


def get_oil_age(t: int) -> float:
    return 0.


def get_mechanical_wear(t: int) -> float:
    return 0.


def default_rul_prediction_fn(current_timestep: int) -> int | None:
    return None
