import asyncclick as click
from templative.create import componentCreator

@click.group()
async def mat():
    """Create a new Mat"""
    pass

@mat.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def bifold(name):
    """Bi-Fold"""
    await componentCreator.createCustomComponent(name, "BiFoldMat")

@mat.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def domino(name):
    """Domino"""
    await componentCreator.createCustomComponent(name, "DominoMat")
