import asyncclick as click
from templative.create import componentCreator

@click.group()
async def packaging():
    """Create Packaging"""
    pass

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def mint(name):
    """A Mint Tin"""
    await componentCreator.createCustomComponent(name, "MintTin")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def stoutBoxSmall(name):
    """Small Cardboard Box"""
    await componentCreator.createCustomComponent(name, "SmallStoutBox")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def stoutBoxMedium(name):
    """Medium Cardboard Box"""
    await componentCreator.createCustomComponent(name, "MediumStoutBox")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def stoutBoxLarge(name):
    """Large Cardboard Box"""
    await componentCreator.createCustomComponent(name, "LargeStoutBox")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def tuckBoxPoker36Cards(name):
    """Poker Tuckbox 36x Cards"""
    await componentCreator.createCustomComponent(name, "PokerTuckBox36")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def tuckBoxPoker54Cards(name):
    """Poker Tuckbox 54x Cards"""
    await componentCreator.createCustomComponent(name, "PokerTuckBox54")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def tuckBoxPoker72Cards(name):
    """Poker Tuckbox 72x Cards"""
    await componentCreator.createCustomComponent(name, "PokerTuckBox72")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def tuckBoxPoker90Cards(name):
    """Poker Tuckbox 90x Cards"""
    await componentCreator.createCustomComponent(name, "PokerTuckBox90")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def tuckBoxPoker108Cards(name):
    """Poker Tuckbox 108x Cards"""
    await componentCreator.createCustomComponent(name, "PokerTuckBox108")