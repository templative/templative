import asyncclick as click
from templative import gameManager

@click.group()
async def deck():
    """Create a new Decks"""
    pass

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def pokerDeck(name):
    """Poker Deck"""
    await gameManager.createComponent(name, "PokerDeck")

@deck.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def mintTinDeck(name):
    """Mint Tin Deck"""
    await gameManager.createComponent(name, "MintTinDeck")