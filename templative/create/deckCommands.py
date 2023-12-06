import asyncclick as click
from templative.create import componentCreator

@click.group()
async def deck():
    """Create a new Decks"""
    pass

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def poker(name, input):
    """Poker Deck"""
    await componentCreator.createCustomComponent(input, name, "PokerDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def jumbo(name, input):
    """Jumbo Deck"""
    await componentCreator.createCustomComponent(input, name, "JumboDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def business(name, input):
    """Business Deck"""
    await componentCreator.createCustomComponent(input, name, "BusinessDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def mint(name, input):
    """Mint Tin Deck"""
    await componentCreator.createCustomComponent(input, name, "MintTinDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def hex(name, input):
    """Hex Deck"""
    await componentCreator.createCustomComponent(input, name, "HexDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def micro(name, input):
    """Micro Deck"""
    await componentCreator.createCustomComponent(input, name, "MicroDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def mini(name, input):
    """Mini Deck"""
    await componentCreator.createCustomComponent(input, name, "MiniDeck")