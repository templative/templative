import asyncclick as click
from .accordionCommands import accordion
from .deckCommands import deck
from .dieCommands import die
from .packagingCommands import packaging
from .punchoutCommands import punchout
from .stockpartCommands import stock

@click.group()
async def create():
    """Create components from templates"""
    pass

create.add_command(accordion)
create.add_command(deck)
create.add_command(die)
create.add_command(packaging)
create.add_command(punchout)
create.add_command(stock)



