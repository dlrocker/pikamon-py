import os
import sys
import json
import logging
import logging.config

import discord

LOGGING_CONFIG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/../configuration/logging.json"
with open(LOGGING_CONFIG_FILE, 'r') as f:
    logging_config = json.load(f)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


def main(token):
    client = discord.Client()

    @client.event
    async def on_ready():
        logger.info('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        logger.debug("Received message from user {}".format(message.author, client.user))

        # client.user is the bot. Ignore messages from the bot.
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    client.run(token)


if __name__ == "__main__":
    oauth_token = sys.argv[1]
    main(oauth_token)
