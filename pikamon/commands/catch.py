import logging
from datetime import datetime
import random

import discord
from discord import Embed

from pikamon.constants import USER_TABLE, POKEMON_TABLE, MIN_POKEMON_LEVEL, MAX_POKEMON_LEVEL

logger = logging.getLogger(__name__)


def __catch_pokemon(message, cache, sqlite_conn, pokemon_name, author):
    """Internal logic to actually perform the "catch" command on the specified pokemon

    Parameters
    ----------
    message : discord.Message
        Discord message object which executed the pokemon bot catch command
    cache : cachetools.TTLCache
        A TTL LRU cache to store channels which contain spawned pokemon
    sqlite_conn : sqlite3.Connection
        SQLite Connection Object
    pokemon_name : str
        Name of the pokemon being caught
    author : str
        Name of the Discord user attempting to catch the Pokemon
    """
    cursor = sqlite_conn.cursor()

    # TODO - Change so that we call out to the Pokemon API to verify the user specified the correct pokemon name
    #  As of right now, assume the user specified the correct pokemon
    if True:
        pokemon_id = cache.pop(message.channel)
        insert_pokemon = '''INSERT INTO {table} (trainer_id, pokemon_number, pokemon_name, pokemon_level) VALUES (
                    ?, ?, ?, ?);'''.format(table=POKEMON_TABLE)
        cursor.execute(
            insert_pokemon,
            (author, pokemon_id, pokemon_name, random.randint(MIN_POKEMON_LEVEL, MAX_POKEMON_LEVEL))
        )

        # TODO - Remove when no longer debugging. We don't want to print the whole pokemon database everytime...
        if logger.isEnabledFor(logging.DEBUG):
            cursor.execute('''SELECT * from pokemon;'''.format(author))
            result = cursor.fetchall()
            logger.debug(result)
            sqlite_conn.commit()


async def catch_pokemon(message, cache, registered_trainers, sqlite_conn):
    """Perform the catch command on a pokemon specified by the user.

    Parameters
    ----------
    message : discord.Message
        Discord message object which executed the pokemon bot catch command
    cache : cachetools.TTLCache
        A TTL LRU cache to store channels which contain spawned pokemon
    registered_trainers : set of str
        Cache of registered trainers
    sqlite_conn : sqlite3.Connection
        SQLite Connection Object

    Examples
    -------
    Command from discord: p!ka catch <pokemon_name>
    p!ka - Command prefix
    catch - Command to perform
    <pokemon_name> - Name of pokemon to catch
    """
    cache.expire()  # Remove any expired entries from the cache

    # use str(...) so that we get the username along with their unique username ID. Example: someuser#1234
    author = str(message.author)
    if author not in registered_trainers:
        await message.channel.send(embed=Embed(
            description=f"Whoops! {message.author.mention} you are not a registered trainer! Please "
            + "register before catching pokemon!",
            colour=0x008080
        ))
        return

    message_content = message.content.lower().split(" ")
    if len(message_content) != 3:
        await message.channel.send("Invalid catch command!")
        # TODO - Remove this if we can overwrite the on_error bot functionality to automatically send a
        #  message to the channel where the error occurred.
        raise discord.DiscordException("Invalid catch command")

    pokemon_name = message_content[2]
    logger.debug(f"Performing catch on user specified pokemon \"{pokemon_name}\"...")
    if message.channel in cache:
        __catch_pokemon(message, cache, sqlite_conn, pokemon_name, author)
        await message.channel.send(embed=Embed(
            description=f"Congratulations {message.author.mention}, you caught a \"{pokemon_name}\"!",
            colour=0x008080
        ))
    else:
        await message.channel.send("The pokemon ran away!")
