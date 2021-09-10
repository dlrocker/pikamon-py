# Prefix used for the Bot commands
COMMAND_PREFIX = "p!ka "


class SqliteDB:
    """SQLite database tables"""
    # Database environment variable that specifies the table configuration path on the system
    DATABASE_CONFIG_PATH_ENV_VAR = "DATABASE_CONFIG_PATH"

    DATABASE_NAME = "pokemon.db"    # SQLite database name
    USER_TABLE = "users"            # User table
    POKEMON_TABLE = "pokemon"       # Pokemon table


class Pokemon:
    # Probability that a pokemon is Spawned if there is no pokemon currently in the channel. Should be between 0 and 1
    SPAWN_RATE = 1

    # Maximum allowed pokemon ID that the pokemon API supports
    MAX_ID = 807

    # Minimum/Maximum pokemon level
    MIN_LEVEL = 1
    MAX_LEVEL = 100


class Cache:
    """Constants class for Time To Live (TTL) Cache"""
    MAX_SIZE = 258  # Max number of channels supported
    TTL = 20        # Max lifetime of channel in cache - in seconds


class DiscordMessage:
    """Properties related to sending messages to Discord"""
    COLOR = 0x008080    # Message color when the bot posts to discord channels
