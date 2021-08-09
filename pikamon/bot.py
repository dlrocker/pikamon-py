import os
import sys
import json
import logging
import logging.config

import discord

from pikamon.constants import COMMAND_PREFIX
from pikamon.commands.catch import catch, CATCH_COMMAND

# TODO - Take path to configuration directory as command line parameter
LOGGING_CONFIG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/../configuration/logging.json"
with open(LOGGING_CONFIG_FILE, 'r') as f:
    logging_config = json.load(f)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


class PikamonBot(discord.Client):
    def __init__(self):
        super().__init__()

        self.commands = {
            CATCH_COMMAND: catch
        }

    async def help(self, message):
        await message.channel.send("""
        Welcome to the Pikamon Bot!
            
        Here are the list of valid Commands:
        {}
        
        Enjoy!
        """.format(
            "\n".join(["- {}".format(c) for c in self.commands.keys()])
        ))

    async def on_message(self, message):
        logger.debug("Received message from user {}".format(message.author, self.user))
        if message.author == self.user:
            return

        msg_content_list = message.content.lower().split(" ")
        if msg_content_list[0] != COMMAND_PREFIX:
            return

        if len(msg_content_list) <= 2:
            logger.debug("Invalid command: {}".format(message.content))
            await self.help(message)
            return

        command = self.commands.get(msg_content_list[1])
        if command is not None:
            await catch(message)

    # async def on_disconnect(self):
    #     logger.info("Disconnecting bot")


def main(token):
    client = PikamonBot()
    client.run(token)


if __name__ == "__main__":
    oauth_token = sys.argv[1]
    main(oauth_token)
