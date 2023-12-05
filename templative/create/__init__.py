import asyncclick as click


from .accordionCommands import accordion
from .deckCommands import deck
from .boardCommands import board
from .dieCommands import die
from .packagingCommands import packaging
from .punchoutCommands import punchout
from .stockpartCommands import stock
from .matCommands import mat
from templative.create import projectCreator

@click.group()
async def create():
    """Component Creation Commands"""
    pass

@click.command()
@click.option("-p", "--path", default="./", help="The name of the new component.")
async def init(path):
    """Create the default game project here"""
    return await projectCreator.createProjectInDirectory(path)


create.add_command(accordion)
create.add_command(deck)
create.add_command(board)
create.add_command(die)
create.add_command(packaging)
create.add_command(punchout)
create.add_command(stock)
create.add_command(mat)

