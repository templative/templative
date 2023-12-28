import asyncclick as click

from .accordionCommands import accordion
from .deckCommands import deck
from .boardCommands import board
from .dieCommands import die
from .packagingCommands import packaging
from .punchoutCommands import punchout
from .stockpartCommands import stock
from .matCommands import mat
from templative.lib.create import projectCreator

@click.group()
async def create():
    """Component Creation Commands"""
    pass

@click.command()
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def init(input):
    """Create the default game project here"""
    return await projectCreator.createProjectInDirectory(input)


create.add_command(accordion)
create.add_command(deck)
create.add_command(board)
create.add_command(die)
create.add_command(packaging)
create.add_command(punchout)
create.add_command(stock)
create.add_command(mat)

