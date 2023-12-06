import asyncclick as click
from templative.create import componentCreator

@click.group()
async def mat():
    """Create a new Mat"""
    pass

@mat.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def bifold(name, input):
    """Bi-Fold"""
    await componentCreator.createCustomComponent(input, name, "BiFoldMat")

@mat.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def domino(name, input):
    """Domino"""
    await componentCreator.createCustomComponent(input, name, "DominoMat")
