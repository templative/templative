import asyncclick as click
from templative import gameManager

@click.group()
async def die():
    """Create a new Die"""
    pass

@die.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def d4(name):
    """D4"""
    await gameManager.createComponent(name, "CustomColorD4")

@die.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def d6(name):
    """D6"""
    await gameManager.createComponent(name, "CustomColorD6")

@die.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def d8(name):
    """D8"""
    await gameManager.createComponent(name, "CustomColorD8")