import asyncclick as click
from templative import gameManager

@click.group()
async def punchout():
    """Create a new Punchout"""
    pass

@punchout.group()
async def chit():
    """Create a new Chit"""
    pass

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def ringLarge(name):
    """Create a Large Ring"""
    await gameManager.createComponent(name, "LargeRingChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def ringMedium(name):
    """Create a Medium Ring"""
    await gameManager.createComponent(name, "MediumRingChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def ringSmall(name):
    """Create a Small Ring"""
    await gameManager.createComponent(name, "SmallRingChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def squareLarge(name):
    """Create a Large Square"""
    await gameManager.createComponent(name, "LargeSquareChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def squareMedium(name):
    """Create a Medium Square"""
    await gameManager.createComponent(name, "MediumSquareChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def squareSmall(name):
    """Create a Small Square"""
    await gameManager.createComponent(name, "SmallSquareChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def circleLarge(name):
    """Create a Large Circle"""
    await gameManager.createComponent(name, "LargeCircleChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def circleMedium(name):
    """Create a Medium Circle"""
    await gameManager.createComponent(name, "MediumCircleChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def circleSmall(name):
    """Create a Small Circle"""
    await gameManager.createComponent(name, "SmallCircleChit")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def hexLarge(name):
    """Create a Large Hex"""
    await gameManager.createComponent(name, "LargeHexTile")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def hexMedium(name):
    """Create a Medium Hex"""
    await gameManager.createComponent(name, "MediumHexTile")

@chit.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def hexSmall(name):
    """Create a Small Hex"""
    await gameManager.createComponent(name, "SmallHexTile")

@punchout.group()
async def shard():
    """Create a new Shard"""
    pass

@shard.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def hex(name):
    """Create a Hex Shard"""
    await gameManager.createComponent(name, "HexShard")

@shard.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def circle(name):
    """Create a Circle Shard"""
    await gameManager.createComponent(name, "CircleShard")

@shard.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def square(name):
    """Create a Square Shard"""
    await gameManager.createComponent(name, "SquareShard")