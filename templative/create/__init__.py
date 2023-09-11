import asyncclick as click
from os import path
from distutils.dir_util import copy_tree

from .accordionCommands import accordion
from .deckCommands import deck
from .boardCommands import board
from .dieCommands import die
from .packagingCommands import packaging
from .punchoutCommands import punchout
from .stockpartCommands import stock

@click.group()
async def create():
    """Component Creation Commands"""
    pass

@click.command()
async def init():
    """Create the default game project here"""
    if(path.exists("./game-compose.json")):
        print("This directory already contains a gameExisting game compose here.")
        return

    fromDirectory = path.join(path.dirname(path.realpath(__file__)), "template")
    copy_tree(fromDirectory, "./")

create.add_command(accordion)
create.add_command(deck)
create.add_command(board)
create.add_command(die)
create.add_command(packaging)
create.add_command(punchout)
create.add_command(stock)

