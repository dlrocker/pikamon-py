# Prefix used for the Bot commands
COMMAND_PREFIX = "p!ka "

# SQLite database name
DATABASE_CONFIG_PATH_ENV_VAR = "DATABASE_CONFIG_PATH"
DATABASE_NAME = "pokemon.db"

# Probability that a pokemon is Spawned if there is no pokemon currently in the channel. Should be between 0 and 1
SPAWN_RATE = 1
# Maximum allowed pokemon ID - it is the max ID number the pokemon API supports
MAX_POKEMON_ID = 807


class Cache:
    """Constants class for Time To Live (TTL) Cache"""
    MAX_SIZE = 258
    TTL = 5
