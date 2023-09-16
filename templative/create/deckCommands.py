import asyncclick as click
from templative.create import componentCreator

@click.group()
async def deck():
    """Create a new Decks"""
    pass

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def poker(name):
    """Poker Deck"""
    await componentCreator.createCustomComponent(name, "PokerDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def jumbo(name):
    """Jumbo Deck"""
    await componentCreator.createCustomComponent(name, "JumboDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def business(name):
    """Business Deck"""
    await componentCreator.createCustomComponent(name, "BusinessDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def mint(name):
    """Mint Tin Deck"""
    await componentCreator.createCustomComponent(name, "MintTinDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def hex(name):
    """Hex Deck"""
    await componentCreator.createCustomComponent(name, "HexDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def micro(name):
    """Micro Deck"""
    await componentCreator.createCustomComponent(name, "MicroDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def mini(name):
    """Mini Deck"""
    await componentCreator.createCustomComponent(name, "MiniDeck")