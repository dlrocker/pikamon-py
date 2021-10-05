import logging
import random

import discord
from discord import Embed

from pikamon.pokeapi.api import get_pokemon
from pikamon.commands.register import is_registered
from pikamon.constants import Pokemon, SqliteDB, DiscordMessage

logger = logging.getLogger(__name__)


async def __catch_pokemon(message, cache, sqlite_conn, pokemon_name, author):
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

    Returns
    -------
    bool
        None: Return None if we fail to get the Pokemon for any reason, such as it doesn't exist or API failure
        True: If the user successfully catches the Pokemon
        False: If the user fails to catch the Pokemon. This happens if the specified name doesn't match the actual name
    """
    cursor = sqlite_conn.cursor()

    pokedex_id = cache.get(message.channel)
    logger.debug("Attempting catch on Pokemon ID {}".format(pokedex_id))
    pokemon_data = await get_pokemon(pokedex_id)
    if pokemon_data is None:
        return None

    if pokemon_data.get("name", "").lower() == pokemon_name:
        # Record the Pokemon as being caught
        insert_pokemon = '''INSERT INTO {table} (trainer_id, pokemon_number, pokemon_name, pokemon_level) VALUES (
                    ?, ?, ?, ?);'''.format(table=SqliteDB.POKEMON_TABLE)
        cursor.execute(
            insert_pokemon,
            (author, pokedex_id, pokemon_name, random.randint(Pokemon.MIN_LEVEL, Pokemon.MAX_LEVEL))
        )
        sqlite_conn.commit()

        # Remove Pokemon from cache after successful catch
        cache.pop(message.channel)
        return True
    # Signal that the user failed to catch the Pokemon
    return False


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
    registered = await is_registered(message, registered_trainers, author)
    if not registered:
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
        response = await __catch_pokemon(message, cache, sqlite_conn, pokemon_name, author)
        if response is True:
            await message.channel.send(embed=Embed(
                description=f"Congratulations {message.author.mention}, you caught a \"{pokemon_name}\"!",
                colour=DiscordMessage.COLOR
            ))
        elif response is False:
            await message.channel.send(embed=Embed(
                description=f"{message.author.mention} failed to catch the Pokemon!",
                colour=DiscordMessage.COLOR
            ))
        else:
            await message.channel.send(embed=Embed(
                description=f"Unable to catch the Pokemon at this time!",
                colour=DiscordMessage.COLOR
            ))
    else:
        await message.channel.send("The pokemon ran away!")
