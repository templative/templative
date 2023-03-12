import asyncclick as click
from templative import gameManager

@click.group()
async def packaging():
    """Create Packaging"""
    pass

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def mint(name):
    """A Mint Tin"""
    await gameManager.createComponent(name, "MintTin")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def stoutBoxSmall(name):
    """Small Cardboard Box"""
    await gameManager.createComponent(name, "SmallStoutBox")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def stoutBoxMedium(name):
    """Medium Cardboard Box"""
    await gameManager.createComponent(name, "MediumStoutBox")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def stoutBoxLarge(name):
    """Large Cardboard Box"""
    await gameManager.createComponent(name, "LargeStoutBox")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def tuckBoxPoker36Cards(name):
    """Poker Tuckbox 36x Cards"""
    await gameManager.createComponent(name, "PokerTuckBox36")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def tuckBoxPoker54Cards(name):
    """Poker Tuckbox 54x Cards"""
    await gameManager.createComponent(name, "PokerTuckBox54")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def tuckBoxPoker72Cards(name):
    """Poker Tuckbox 72x Cards"""
    await gameManager.createComponent(name, "PokerTuckBox72")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def tuckBoxPoker90Cards(name):
    """Poker Tuckbox 90x Cards"""
    await gameManager.createComponent(name, "PokerTuckBox90")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def tuckBoxPoker108Cards(name):
    """Poker Tuckbox 108x Cards"""
    await gameManager.createComponent(name, "PokerTuckBox108")