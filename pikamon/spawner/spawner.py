import random
import logging

from discord import Embed

from pikamon.constants import Pokemon, DiscordMessage

logger = logging.getLogger(__name__)


async def spawn(message, cache):
    """Spawns a pokemon based on probability if a pokemon has not already been spawned for the channel with the
    current message being processed

    Parameters
    ----------
    message : discord.Message
        Discord Message context
    cache : cachetools.TTLCache
        Cache object which contains channels that have active pokemon spawns
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
        if random.random() <= Pokemon.SPAWN_RATE:
            logger.info("Spawning new Pokemon!")
            pokemon_id = random.randint(0, Pokemon.MAX_ID)
            cache[channel_name] = pokemon_id
            embeded_msg = Embed(
                title="‌‌A wild pokémon has appeared!",
                description="Guess the pokémon аnd type `p!ka catch <pokémon>` to cаtch it!",
                colour=DiscordMessage.COLOR
            )
            embeded_msg.set_image(
                url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png")
            await message.channel.send(embed=embeded_msg)
        else:
            logger.debug("Pokemon will not be spawned this time.")
