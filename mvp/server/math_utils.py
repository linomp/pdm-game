import math


def linear_growth_with_reset(initial_value, period, time):
    growth_rate = 1
    effective_time = time % period
    current_value = initial_value + growth_rate * effective_time
    current_value %= (initial_value + period)
    return current_value


def exponential_decay(current_timestep: int, initial_value: int, decay_speed: float) -> float:
    return initial_value - math.exp(current_timestep * decay_speed)
