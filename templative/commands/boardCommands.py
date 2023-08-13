import asyncclick as click
from templative import gameManager

@click.group()
async def board():
    """Create a new Board"""
    pass

@board.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def domino(name):
    """Domino Board"""
    await gameManager.createComponent(name, "BoardDomino")
