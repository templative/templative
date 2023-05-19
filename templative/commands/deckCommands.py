import asyncclick as click
from templative import gameManager

@click.group()
async def deck():
    """Create a new Decks"""
    pass

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def poker(name):
    """Poker Deck"""
    await gameManager.createComponent(name, "PokerDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def business(name):
    """Business Deck"""
    await gameManager.createComponent(name, "BusinessDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def mint(name):
    """Mint Tin Deck"""
    await gameManager.createComponent(name, "MintTinDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def hex(name):
    """Hex Deck"""
    await gameManager.createComponent(name, "HexDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def micro(name):
    """Micro Deck"""
    await gameManager.createComponent(name, "MicroDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def mini(name):
    """Mini Deck"""
    await gameManager.createComponent(name, "MiniDeck")