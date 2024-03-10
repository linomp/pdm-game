from pydantic import BaseModel

from mvp.server.core.constants import *


class GameParametersDTO(BaseModel):
    initial_cash: float
    revenue_per_day: float
    maintenance_cost: float
    sensor_cost: float
    prediction_model_cost: float
    game_tick_interval: float
    warning_levels: dict[str, float]

    def __init__(self):
        super().__init__(
            initial_cash=INITIAL_CASH,
            revenue_per_day=REVENUE_PER_DAY,
            maintenance_cost=MAINTENANCE_COST,
            sensor_cost=SENSOR_COST,
            prediction_model_cost=PREDICTION_MODEL_COST,
            game_tick_interval=GAME_TICK_INTERVAL,
            warning_levels={
                "oil_age": OIL_AGE_MAPPING_MAX * 0.05,
                "mechanical_wear": MECHANICAL_WEAR_MAPPING_MAX * 0.001,
                "temperature": TEMPERATURE_MAPPING_MAX * 0.75
            }
        )
