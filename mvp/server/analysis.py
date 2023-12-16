import math


def exponential_decay(t: int, start: int, decay_speed: float) -> float:
    return start - math.exp(t * decay_speed)


def get_health_percentage(current_step: int) -> int:
    raw_val = round(exponential_decay(current_step, start=100, decay_speed=1e-1))
    return min(100, max(0, raw_val))


def default_rul_prediction_fn(current_step: int) -> int | None:
    return None
