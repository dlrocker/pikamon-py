import logging

logger = logging.getLogger(__name__)

CATCH_COMMAND = "catch"


async def catch(message):
    logger.debug("Entering catch() with message {}".format(message))
    await message.channel.send('Catching pokemon!')
