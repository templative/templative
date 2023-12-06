import asyncclick as click
from templative.create import componentCreator

@click.group()
async def punchout():
    """Create a new Punchout"""
    pass

@punchout.group()
async def custom():
    """Create a new Custom Punchout"""
    pass

@custom.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def customsmall(name, input):
    """Create a Small Custom Punchout"""
    await componentCreator.createCustomComponent(input, name, "PunchoutCustomSmall")

@punchout.group()
async def chit():
    """Create a new Chit"""
    pass

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def ringLarge(name, input):
    """Create a Large Ring"""
    await componentCreator.createCustomComponent(input, name, "LargeRingChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def ringMedium(name, input):
    """Create a Medium Ring"""
    await componentCreator.createCustomComponent(input, name, "MediumRingChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def ringSmall(name, input):
    """Create a Small Ring"""
    await componentCreator.createCustomComponent(input, name, "SmallRingChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def squareLarge(name, input):
    """Create a Large Square"""
    await componentCreator.createCustomComponent(input, name, "LargeSquareChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def squareMedium(name, input):
    """Create a Medium Square"""
    await componentCreator.createCustomComponent(input, name, "MediumSquareChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def squareSmall(name, input):
    """Create a Small Square"""
    await componentCreator.createCustomComponent(input, name, "SmallSquareChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def circleLarge(name, input):
    """Create a Large Circle"""
    await componentCreator.createCustomComponent(input, name, "LargeCircleChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def circleMedium(name, input):
    """Create a Medium Circle"""
    await componentCreator.createCustomComponent(input, name, "MediumCircleChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def circleSmall(name, input):
    """Create a Small Circle"""
    await componentCreator.createCustomComponent(input, name, "SmallCircleChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def hexLarge(name, input):
    """Create a Large Hex"""
    await componentCreator.createCustomComponent(input, name, "LargeHexTile")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def hexMedium(name, input):
    """Create a Medium Hex"""
    await componentCreator.createCustomComponent(input, name, "MediumHexTile")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def hexSmall(name, input):
    """Create a Small Hex"""
    await componentCreator.createCustomComponent(input, name, "SmallHexTile")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def hexMini(name, input):
    """Create a Mini Hex"""
    await componentCreator.createCustomComponent(input, name, "MiniHexTile")

@punchout.group()
async def shard():
    """Create a new Shard"""
    pass

@shard.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def hex(name, input):
    """Create a Hex Shard"""
    await componentCreator.createCustomComponent(input, name, "HexShard")

@shard.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def circle(name, input):
    """Create a Circle Shard"""
    await componentCreator.createCustomComponent(input, name, "CircleShard")

@shard.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def square(name, input):
    """Create a Square Shard"""
    await componentCreator.createCustomComponent(input, name, "SquareShard")