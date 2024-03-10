import math


def linear_growth_with_reset(initial_value: float, period: int, current_timestep: int, growth_rate=1) -> float:
    effective_time = current_timestep % period
    current_value = initial_value + growth_rate * effective_time
    current_value %= (initial_value + period)
    return current_value


def exponential_decay(current_timestep: int, initial_value: float, decay_speed: float) -> float:
    return initial_value / math.exp(current_timestep * decay_speed)


def map_value(value: float, from_low: float, from_high: float, to_low: float, to_high: float) -> float:
    from_range: float = from_high - from_low
    to_range: float = to_high - to_low

    scaled_value: float = (value - from_low) / from_range
    mapped_value: float = to_low + (scaled_value * to_range)

    if mapped_value < to_low:
        return to_low
    elif mapped_value > to_high:
        return to_high
    else:
        return mapped_value
