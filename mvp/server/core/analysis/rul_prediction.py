import random


def default_rul_prediction_fn(current_timestep: int) -> int | None:
    return random.randint(1, 1000)
