"""
config.py

Global configuration used throughout the Logistics Optimization System.
Changing values here automatically affects every module.
"""

# ==========================================================
# DATABASE
# ==========================================================

DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "db_logistik"
DB_USER = "root"
DB_PASSWORD = ""

DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================================================
# COMPANY CONFIGURATION
# ==========================================================

WAREHOUSE_CITY = "Surabaya"

TRUCK_COUNT = 4

# ==========================================================
# BUSINESS CONSTANTS
# ==========================================================

BASE_REVENUE_PER_KG_KM = 8

DEFAULT_DIMENSION_MULTIPLIER = {
    "S": 1.0,
    "M": 1.2,
    "L": 1.5
}

# ==========================================================
# GENETIC ALGORITHM DEFAULTS
# ==========================================================

DEFAULT_POPULATION_SIZE = 30
DEFAULT_GENERATIONS = 100
DEFAULT_CROSSOVER_RATE = 0.90
DEFAULT_MUTATION_RATE = 0.10
DEFAULT_ELITE_COUNT = 2

# ==========================================================
# SIMULATED ANNEALING DEFAULTS
# ==========================================================

DEFAULT_INITIAL_TEMPERATURE = 1000
DEFAULT_COOLING_RATE = 0.95
DEFAULT_MIN_TEMPERATURE = 1
DEFAULT_MAX_SA_ITERATIONS = 500