# Gameplay
DEFAULT_SESSION_ID = 'test'
GAME_TICK_INTERVAL = 0.5
IDLE_SESSION_TTL_SECONDS = 60 * 30  # 30 minutes
TIMESTEPS_PER_MOVE = 8  # we conceptualize every player move as a full working day, or "8 hours"
GAME_OVER_MESSAGE_MACHINE_BREAKDOWN = "Machine health has reached 0%"
GAME_OVER_MESSAGE_NO_MONEY = "Player ran out of money"

# Machine Simulation
TEMPERATURE_STARTING_POINT = 20
OIL_AGE_MAPPING_MAX = 365
TEMPERATURE_MAPPING_MAX = 200
MECHANICAL_WEAR_MAPPING_MAX = 100

# Financials
INITIAL_CASH = 0
REVENUE_PER_DAY = 20
MAINTENANCE_COST = 80
SENSOR_COST = 20
PREDICTION_MODEL_COST = 50
