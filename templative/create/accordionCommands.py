import asyncclick as click
from templative.create import componentCreator

@click.group()
async def accordion():
    """Create a new Accordion"""
    pass

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def folioPoker(name):
    """Poker Folio"""
    await componentCreator.createCustomComponent(name, "PokerFolio")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def folioMint(name):
    """Mint Tin Folio"""
    await componentCreator.createCustomComponent(name, "MintTinFolio")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def mint4(name):
    """Mint Tin Accordion 4 Panels"""
    await componentCreator.createCustomComponent(name, "MintTinAccordion4")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def mint6(name):
    """Mint Tin Accordion 6 Panels"""
    await componentCreator.createCustomComponent(name, "MintTinAccordion6")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def mint8(name):
    """Mint Tin Accordion 8 Panels"""
    await componentCreator.createCustomComponent(name, "MintTinAccordion8")