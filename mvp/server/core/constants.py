# Gameplay
DEFAULT_SESSION_ID = 'test'
GAME_TICK_INTERVAL = 0.03  # 30ms
IDLE_SESSION_TTL_SECONDS = 60 * 30  # 15 minutes
SESSION_CLEANUP_INTERVAL_SECONDS = 60 * 60  # 60 minutes
TIMESTEPS_PER_MOVE = 24  # "hours"
GAME_OVER_MESSAGE_MACHINE_BREAKDOWN = "Machine health has reached 0%"
GAME_OVER_MESSAGE_NO_MONEY = "Player ran out of money"

# Machine Simulation
TEMPERATURE_STARTING_POINT = 20
OIL_AGE_MAPPING_MAX = 365
TEMPERATURE_MAPPING_MAX = 100
MECHANICAL_WEAR_MAPPING_MAX = 1000
OIL_AGE_WARNING_FACTOR = 0.25
TEMPERATURE_WARNING_FACTOR = 0.70
MECHANICAL_WEAR_WARNING_FACTOR = 0.1

# Maintenance effects
HEALTH_RECOVERY_FACTOR_ON_MAINTENANCE = 1.75
MECHANICAL_WEAR_REDUCTION_FACTOR_ON_MAINTENANCE = 100

# Financials
INITIAL_CASH = 0
REVENUE_PER_DAY = 20
MAINTENANCE_COST = 40
SENSOR_COST = 30
PREDICTION_MODEL_COST = 50
