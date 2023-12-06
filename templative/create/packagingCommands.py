import asyncclick as click
from templative.create import componentCreator

@click.group()
async def packaging():
    """Create Packaging"""
    pass

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def mint(name, input):
    """A Mint Tin"""
    await componentCreator.createCustomComponent(input, name, "MintTin")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def stoutBoxSmall(name, input):
    """Small Cardboard Box"""
    await componentCreator.createCustomComponent(input, name, "SmallStoutBox")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def stoutBoxMedium(name, input):
    """Medium Cardboard Box"""
    await componentCreator.createCustomComponent(input, name, "MediumStoutBox")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def stoutBoxLarge(name, input):
    """Large Cardboard Box"""
    await componentCreator.createCustomComponent(input, name, "LargeStoutBox")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def tuckBoxPoker36Cards(name, input):
    """Poker Tuckbox 36x Cards"""
    await componentCreator.createCustomComponent(input, name, "PokerTuckBox36")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def tuckBoxPoker54Cards(name, input):
    """Poker Tuckbox 54x Cards"""
    await componentCreator.createCustomComponent(input, name, "PokerTuckBox54")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def tuckBoxPoker72Cards(name, input):
    """Poker Tuckbox 72x Cards"""
    await componentCreator.createCustomComponent(input, name, "PokerTuckBox72")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def tuckBoxPoker90Cards(name, input):
    """Poker Tuckbox 90x Cards"""
    await componentCreator.createCustomComponent(input, name, "PokerTuckBox90")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def tuckBoxPoker108Cards(name, input):
    """Poker Tuckbox 108x Cards"""
    await componentCreator.createCustomComponent(input, name, "PokerTuckBox108")

@packaging.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def boosterPack(name, input):
    """Poker Booster Pack"""
    await componentCreator.createCustomComponent(input, name, "PokerBooster")