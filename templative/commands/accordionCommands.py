import asyncclick as click
from templative import gameManager

@click.group()
async def accordion():
    """Create a new Accordion"""
    pass

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def folioPoker(name):
    """Poker Folio"""
    await gameManager.createComponent(name, "PokerFolio")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def folioMint(name):
    """Mint Tin Folio"""
    await gameManager.createComponent(name, "MintTinFolio")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def accordionMint4(name):
    """Mint Tin Accordion 4 Panels"""
    await gameManager.createComponent(name, "MintTinAccordion4")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def accordionMint6(name):
    """Mint Tin Accordion 6 Panels"""
    await gameManager.createComponent(name, "MintTinAccordion6")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def accordionMint8(name):
    """Mint Tin Accordion 8 Panels"""
    await gameManager.createComponent(name, "MintTinAccordion8")