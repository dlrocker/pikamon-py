import logging

from discord import Embed

from pikamon.commands.register import is_registered
from pikamon.constants import SqliteDB, DiscordMessage

logger = logging.getLogger(__name__)


def __format_list(pokemon_list):
    """Formats the list of a Trainers Pokemon so that it displays nicely in Discord

    Parameters
    ----------
    pokemon_list : list of str
        List of Pokemon table records/tuples from SQLite for the trainer

    Returns
    -------
    str
        Formatted String message of Pokemon caught by the trainer
    """
    # TODO - Format this a bit nicer, ideally with padding so it displays well in Discord.
    formatted_list = "**Your Pokemon:\n**"
    for id, pokemon_name, pokemon_level in pokemon_list:
        formatted_list += f"Name: {pokemon_name} --- Level: {pokemon_level} --- ID: {id}\n"
    return formatted_list


async def list_pokemon(message, registered_trainers, sqlite_conn):
    """Post a list of all Pokemon caught by a trainer to Discord

    Parameters
    ----------
    message : discord.Message
        Discord message object which executed the pokemon bot catch command
    registered_trainers : set of str
        Set of registered Pokemon trainers
    sqlite_conn : sqlite3.Connection
        SQLite Connection Object
    """
    # use str(...) so that we get the username along with their unique username ID. Example: someuser#1234
    author = str(message.author)
    registered = await is_registered(message, registered_trainers, author)
    if not registered:
        return

    cursor = sqlite_conn.cursor()
    list_caught_pokemon = '''SELECT id, pokemon_name, pokemon_level FROM {} where trainer_id = \"{}\"'''\
        .format(SqliteDB.POKEMON_TABLE, author)
    cursor.execute(list_caught_pokemon)
    pokemon_list = cursor.fetchall()

    if len(pokemon_list) > 0:
        await message.channel.send(embed=Embed(
            description=__format_list(pokemon_list),
            colour=DiscordMessage.COLOR
        ))
    else:
        await message.channel.send(embed=Embed(
            description=f"{message.author.mention} you don't have any Pokemon! Get back out there trainer!",
            colour=DiscordMessage.COLOR
        ))
