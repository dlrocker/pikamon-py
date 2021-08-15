import random
import logging

from pikamon.constants import SPAWN_RATE, MAX_POKEMON_ID
from pikamon.spawner.poke_api import get_pokemon_info, get_pokemon_img

logger = logging.getLogger(__name__)


async def spawn(message, cache):
    """Spawns a pokemon based on probability if a pokemon has not already been spawned for the channel with the
    current message being processed

    Parameters
    ----------
    message : discord.Message
        Discord Message context
    """
    channel_name = message.channel
    logger.debug("Attempting to spawn pokemon on channel \"{}\"".format(channel_name))

    # Clear all channel caches so that if a pokemon has expired, it is no longer available
    # TODO - Print message when pokemon for channel expires. May need to extend TTLCache and edit the following:
    # - https://github.com/tkem/cachetools/blob/master/src/cachetools/ttl.py#L158
    cache.expire()

    if channel_name in cache:
        logger.info("A pokemon has already been spawned for channel \"{}\"".format(channel_name))
    else:
        if random.random() <= SPAWN_RATE:
            logger.info("Spawning new Pokemon!")
            # TODO - Replace this with some kind of pokemon object that contains the information about the pokemon that was sent to the channel  # noqa: E501
            pokemon_id = random.randint(0, MAX_POKEMON_ID)
            pokemon = get_pokemon_info(pokemon_id=pokemon_id)
            cache[channel_name] = pokemon_id
            await message.channel.send("Spawned pokemon!\n{}".format(pokemon["name"]))
        else:
            logger.info("Pokemon will not be spawned this time")
