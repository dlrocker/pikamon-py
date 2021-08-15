import logging
import json

from discord.ext import commands

logger = logging.getLogger(__name__)

CATCH_COMMAND = "catch"


async def catch(message):
    logger.debug("Entering catch() with message {}".format(message))
    await message.channel.send('Catching pokemon!')


class Catch(commands.Cog):
    """Catches the spawned Pokemon"""
    def __init__(self, bot):
        """

        Parameters
        ----------
        bot : commands.Bot
        """
        logger.debug("Setting up Catch()")
        self.bot = bot

    @commands.command()
    async def catch(self, ctx, pokemon_name):
        """Attempts to catch the pokemon if one has spawned

        Parameters
        ----------
        ctx : commands.Context
            Context object which contains information about the event
        pokemon_name : string
            Name of the pokemon that the catch is attempted for

        Examples
        -------
        Command from discord: p!ka catch <pokemon_name>
        p!ka - Command prefix
        catch - Command to perform
        <pokemon_name> - Name of pokemon to catch
        """
        logger.debug(f"Performing catch on pokemon \"{pokemon_name}\"...")
        # logger.debug(ctx.message.content.lower().split(" "))
        await ctx.send(f"You're trying to catch \"{pokemon_name}\"!")


def setup(bot):
    """Sets up an instance of the Catch cog for the bot

    Parameters
    ----------
    bot : commands.Bot

    Returns
    -------

    """
    logger.debug("Calling setup() for Catch()")
    bot.add_cog(Catch(bot))
