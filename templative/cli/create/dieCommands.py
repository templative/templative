import asyncclick as click
from templative.lib.create import componentCreator

@click.group()
async def die():
    """Create a new Die"""
    pass

@die.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def d4(name, input):
    """Create an Acrylic D4"""
    await componentCreator.createCustomComponent(input, name, "D4Plastic")

@die.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def d6(name, input):
    """Create an Acrylic D6"""
    await componentCreator.createCustomComponent(input, name, "D6Plastic")

@die.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def d8(name, input):
    """Create an Acrylic D8"""
    await componentCreator.createCustomComponent(input, name, "D8Plastic")