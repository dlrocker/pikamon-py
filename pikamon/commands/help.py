import logging

from discord import Embed

logger = logging.getLogger(__name__)
# TODO - Move command static fields to contstants
HELP_COMMAND = "help"

async def help_catch(message, detail):
    pass


command_specific_helps = {
    "catch": help_catch
}


async def help(message, detail=None, command=None):
    if command and command in command_specific_helps:
        await command_specific_helps[command](message, detail)
        return

    msg = """```\n
    No Category:
      help Shows this message
    
    Type p!ka help command for more info on a command.
    You can also type p!ka help category for more info on a category.
    \n```"""
    await message.channel.send(embed=Embed(
        description=msg
    ))
