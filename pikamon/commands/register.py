import logging
from datetime import datetime

import discord
from discord import Embed

from pikamon.constants import SqliteDB, DiscordMessage

logger = logging.getLogger(__name__)


def get_registered_trainers(sqlite_conn):
    """Gets a set of all trainers that have been previously registered with the bot from our SQLite database

    Parameters
    ----------
    sqlite_conn : sqlite3.Connection
        SQLite Connection Object

    Returns
    -------
    set
        Python Set() containing all previously registered trainers
    """
    cursor = sqlite_conn.cursor()
    cursor.execute('''SELECT user_id from {}'''.format(SqliteDB.USER_TABLE))
    result = cursor.fetchall()
    return {record[0] for record in result}


async def register_trainer(message, registered_trainers, sqlite_conn):
    """Logic to register a new trainer

    It is important to note that the registered_trainers set() will be mutated as part of this operation.

    Parameters
    ----------
    message : discord.Message
        Discord message object which executed the pokemon bot catch command
    registered_trainers : set
        Python Set() containing all previously registered trainers. Note: This set will be mutated when adding
        new trainers.
    sqlite_conn : sqlite3.Connection
        SQLite Connection Object
    """
    cursor = sqlite_conn.cursor()

    # use str(...) so that we get the username along with their unique username ID. Example: someuser#1234
    author = str(message.author)
    cursor.execute('''SELECT user_id from {} where user_id = "{}"'''.format(SqliteDB.USER_TABLE, author))
    result = cursor.fetchall()
    if len(result) == 0:
        # Since the user is not already in the table, add them as a registered user
        current_time = datetime.utcnow().strftime('%Y%m%d')
        insert_user = '''INSERT INTO {table} (user_id, create_date, last_action_date) VALUES (?, ?, ?);'''.format(
            table=SqliteDB.USER_TABLE)
        logger.debug("Executing the create user command: \"{}\"".format(insert_user))
        values = (author, int(current_time), int(current_time))
        cursor.execute(
            insert_user,
            values
        )
        sqlite_conn.commit()
        registered_trainers.add(author)
        await message.channel.send(embed=Embed(
            description=f"Congratulations {message.author.mention}, you are now a registered trainer! "
                        + "Go catch them all!",
            colour=DiscordMessage.COLOR
        ))
    else:
        await message.channel.send(embed=Embed(
            description=f"{message.author.mention} you are already a registered trainer!",
            colour=DiscordMessage.COLOR
        ))
