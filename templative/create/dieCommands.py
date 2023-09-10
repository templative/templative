import asyncclick as click
from templative.create import componentCreator

@click.group()
async def die():
    """Create a new Die"""
    pass

@die.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def d4(name):
    """Create an Acrylic D4"""
    await componentCreator.createCustomComponent(name, "D4Plastic")

@die.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def d6(name):
    """Create an Acrylic D6"""
    await componentCreator.createCustomComponent(name, "D6Plastic")

@die.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def d8(name):
    """Create an Acrylic D8"""
    await componentCreator.createCustomComponent(name, "D8Plastic")