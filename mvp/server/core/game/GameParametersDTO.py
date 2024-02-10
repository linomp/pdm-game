from pydantic import BaseModel

from mvp.server.core.constants import *


class GameParametersDTO(BaseModel):
    initial_cash: float = INITIAL_CASH
    revenue_per_day: float = REVENUE_PER_DAY
    maintenance_cost: float = MAINTENANCE_COST
    sensor_cost: float = SENSOR_COST
    prediction_model_cost: float = PREDICTION_MODEL_COST
    game_tick_interval: float = GAME_TICK_INTERVAL
