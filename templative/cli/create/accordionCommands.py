import asyncclick as click
from templative.lib.create import componentCreator

@click.group()
async def accordion():
    """Create a new Accordion"""
    pass

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def folioPoker(name, input):
    """Poker Folio"""
    await componentCreator.createCustomComponent(input, name, "PokerFolio")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def folioMint(name, input):
    """Mint Tin Folio"""
    await componentCreator.createCustomComponent(input, name, "MintTinFolio")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def mint4(name, input):
    """Mint Tin Accordion 4 Panels"""
    await componentCreator.createCustomComponent(input, name, "MintTinAccordion4")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def mint6(name, input):
    """Mint Tin Accordion 6 Panels"""
    await componentCreator.createCustomComponent(input, name, "MintTinAccordion6")

@accordion.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def mint8(name, input):
    """Mint Tin Accordion 8 Panels"""
    await componentCreator.createCustomComponent(input, name, "MintTinAccordion8")