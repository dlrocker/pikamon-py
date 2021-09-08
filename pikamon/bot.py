import os
import json
import logging.config

from discord.ext import commands
from cachetools import TTLCache

from pikamon.constants import COMMAND_PREFIX, Cache
from pikamon.spawner.spawner import spawn

# TODO - Take path to configuration directory as command line parameter
LOGGING_CONFIG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/../configuration/logging.json"
with open(LOGGING_CONFIG_FILE, 'r') as f:
    logging_config = json.load(f)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


class PikamonBot(commands.Bot):
    def __init__(self, command_prefix=COMMAND_PREFIX):
        super().__init__(command_prefix)
        self.command_prefix = command_prefix
        """
        I believe discord API is not using threading (as evident of using async/await). So for now, I am leaving out
        code to get a lock unless I learn otherwise. The reason this is important is because we need to make sure only
        a single thread is modifying the cache at a time. Code to get the lock if necessary:
        
        from threading import Lock
        self.lock = Lock()
        ...
        with self.lock:
            ...do stuff...
        """
        self.cache = TTLCache(maxsize=Cache.MAX_SIZE, ttl=Cache.TTL)

    async def on_message(self, message):
        """Processes messages posted to channels in the Discord server

        If it is a bot command it will be processed by the loaded command extension. If it is not a bot command,
        it will attempt to spawn a pokemon if no pokemon has already been spawned in the channel.

        Parameters
        ----------
        message : discord.Message
            Discord Message context
        """
        logger.debug("Received message from user {}".format(message.author))
        if message.author == self.user:
            logger.debug("Ignoring message from {}".format(self.user))
            return

        logger.debug("Going to do stuff with message \"{}\"".format(message.content))

        if message.content.lower().startswith(self.command_prefix):
            # If this is a command, we need to call the process_commands() function from parent class to deal with it
            logger.debug("Processing command...")
            await self.process_commands(message)
        else:
            # If the message is not a bot command message, we need to do stuff with it ourselves (spawn pokemon if able)
            await spawn(message, self.cache)

    def load_extensions(self) -> None:
        """Load all enabled extensions and commands for this bot."""
        for command_py in os.listdir("commands"):
            if command_py.endswith(".py") and command_py != "__init__.py":
                command = command_py[:-3]  # Remove trailing ".py"
                logger.debug(f"Loading command extension 'commands.{command}'")
                self.load_extension(f"commands.{command}")


def main(token):
    client = PikamonBot(command_prefix=COMMAND_PREFIX)
    client.load_extensions()
    client.run(token)


if __name__ == "__main__":
    oauth_token = os.environ.get("TOKEN")
    main(oauth_token)
