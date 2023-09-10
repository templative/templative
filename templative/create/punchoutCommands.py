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
async def customsmall(name):
    """Create a Small Custom Punchout"""
    await componentCreator.createCustomComponent(name, "PunchoutCustomSmall")

@punchout.group()
async def chit():
    """Create a new Chit"""
    pass

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def ringLarge(name):
    """Create a Large Ring"""
    await componentCreator.createCustomComponent(name, "LargeRingChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def ringMedium(name):
    """Create a Medium Ring"""
    await componentCreator.createCustomComponent(name, "MediumRingChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def ringSmall(name):
    """Create a Small Ring"""
    await componentCreator.createCustomComponent(name, "SmallRingChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def squareLarge(name):
    """Create a Large Square"""
    await componentCreator.createCustomComponent(name, "LargeSquareChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def squareMedium(name):
    """Create a Medium Square"""
    await componentCreator.createCustomComponent(name, "MediumSquareChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def squareSmall(name):
    """Create a Small Square"""
    await componentCreator.createCustomComponent(name, "SmallSquareChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def circleLarge(name):
    """Create a Large Circle"""
    await componentCreator.createCustomComponent(name, "LargeCircleChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def circleMedium(name):
    """Create a Medium Circle"""
    await componentCreator.createCustomComponent(name, "MediumCircleChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def circleSmall(name):
    """Create a Small Circle"""
    await componentCreator.createCustomComponent(name, "SmallCircleChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def hexLarge(name):
    """Create a Large Hex"""
    await componentCreator.createCustomComponent(name, "LargeHexTile")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def hexMedium(name):
    """Create a Medium Hex"""
    await componentCreator.createCustomComponent(name, "MediumHexTile")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def hexSmall(name):
    """Create a Small Hex"""
    await componentCreator.createCustomComponent(name, "SmallHexTile")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def hexMini(name):
    """Create a Mini Hex"""
    await componentCreator.createCustomComponent(name, "MiniHexTile")

@punchout.group()
async def shard():
    """Create a new Shard"""
    pass

@shard.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def hex(name):
    """Create a Hex Shard"""
    await componentCreator.createCustomComponent(name, "HexShard")

@shard.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def circle(name):
    """Create a Circle Shard"""
    await componentCreator.createCustomComponent(name, "CircleShard")

@shard.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def square(name):
    """Create a Square Shard"""
    await componentCreator.createCustomComponent(name, "SquareShard")