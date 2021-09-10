import os
import json
import logging.config

from discord.ext import commands
from cachetools import TTLCache

from pikamon.constants import COMMAND_PREFIX, Cache, DATABASE_CONFIG_PATH_ENV_VAR
from pikamon.spawner.spawner import spawn
from pikamon.commands.catch import CATCH_COMMAND, catch
from pikamon.database.connect import setup_database

# TODO - Take path to configuration directory as command line parameter
LOGGING_CONFIG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/../configuration/logging.json"
with open(LOGGING_CONFIG_FILE, 'r') as f:
    logging_config = json.load(f)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


table_sql_path = os.environ.get(DATABASE_CONFIG_PATH_ENV_VAR)
sqlite_conn = setup_database(table_sql_path=table_sql_path)
cache = TTLCache(maxsize=Cache.MAX_SIZE, ttl=Cache.TTL)
bot = commands.Bot(command_prefix=COMMAND_PREFIX)
registered_commands = {
    CATCH_COMMAND: catch
}


@bot.event
async def on_message(message):
    """Processes messages posted to channels in the Discord server

    If it is a bot command it will be processed by the loaded command extension. If it is not a bot command,
    it will attempt to spawn a pokemon if no pokemon has already been spawned in the channel.

    Parameters
    ----------
    message : discord.Message
        Discord Message context
    """
    logger.debug("Received message from user {}".format(message.author))
    if message.author == bot.user:
        # Ignore messages from the Pokemon bot
        return

    message_content = message.content.lower()
    if message_content.startswith(COMMAND_PREFIX):
        # If this is a command, we need to call the process_commands() function from parent class to deal with it
        logger.debug(f"Processing command: {message_content}")
        command_statement = message_content.split(" ")
        if len(command_statement) >= 2 and command_statement[1] in registered_commands:
            command = registered_commands.get(command_statement[1])
            await command(message, cache, sqlite_conn)
        else:
            await message.channel.send("Unknown command \"{}\"".format(message_content))
    else:
        # If the message is not a bot command message, we need to do stuff with it ourselves (spawn pokemon if able)
        await spawn(message, cache)


oauth_token = os.environ.get("TOKEN")
bot.run(oauth_token)
