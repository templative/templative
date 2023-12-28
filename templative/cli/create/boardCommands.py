import asyncclick as click
from templative.lib.create import componentCreator

@click.group()
async def board():
    """Create a new Board"""
    pass

@board.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def domino(name, input):
    """Domino Board"""
    await componentCreator.createCustomComponent(input, name, "DominoBoard")
