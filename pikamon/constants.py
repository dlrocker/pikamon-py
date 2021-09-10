# Prefix used for the Bot commands
COMMAND_PREFIX = "p!ka"

# SQLite database name
DATABASE_CONFIG_PATH_ENV_VAR = "DATABASE_CONFIG_PATH"
DATABASE_NAME = "pokemon.db"

# SQLite database tables
USER_TABLE = "users"
POKEMON_TABLE = "pokemon"

# Probability that a pokemon is Spawned if there is no pokemon currently in the channel. Should be between 0 and 1
SPAWN_RATE = 1

# Maximum allowed pokemon ID that the pokemon API supports
MAX_POKEMON_ID = 807

# Minimum/Maximum pokemon level
MIN_POKEMON_LEVEL = 1
MAX_POKEMON_LEVEL = 100


class Cache:
    """Constants class for Time To Live (TTL) Cache"""
    MAX_SIZE = 258  # Max number of channels supported
    TTL = 20        # Max lifetime of channel in cache - in seconds
