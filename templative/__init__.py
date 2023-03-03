import asyncclick as click
from templative import gameManager, gameUploader

@click.group()
async def cli():
    """Templative CLI"""
    pass

@cli.command()
@click.option('--component', default=None, help='The component to produce.')
async def produce(component):
    """Produce the game in the current directory"""
    await gameManager.produceGame(".", component)

@cli.command()
async def components():
    """Get a list of quantities of the game in the current directory"""
    await gameManager.listComponents(".")

@cli.group()
async def create():
    """Create components from templates"""
    pass

@create.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def deckPoker(name):
    """Create a new poker sized deck"""
    if name == None:
        print("Missing --name.")
        return
    
    await gameManager.createComponent(name, "PokerDeck")

@create.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def accordionPoker(name):
    """Create a new poker sized accordion"""
    if name == None:
        print("Missing --name.")
        return
    
    await gameManager.createComponent(name, "PokerFolio")

@create.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def stoutBoxSmall(name):
    """Create a new small cardboard box"""
    if name == None:
        print("Missing --name.")
        return
    
    await gameManager.createComponent(name, "SmallStoutBox")

@create.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def tuckBoxPoker108Cards(name):
    """Create a new poker sized tuckbox fitting 108 cards"""
    if name == None:
        print("Missing --name.")
        return
    
    await gameManager.createComponent(name, "PokerTuckBox108")

@create.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def ringLarge(name):
    """Create a new large ring"""
    if name == None:
        print("Missing --name.")
        return
    
    await gameManager.createComponent(name, "LargeRing")

@create.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def ringMedium(name):
    """Create a new medium ring"""
    if name == None:
        print("Missing --name.")
        return
    
    await gameManager.createComponent(name, "MediumRing")

@create.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
async def chitSquareLarge(name):
    """Create a new medium ring"""
    if name == None:
        print("Missing --name.")
        return
    
    await gameManager.createComponent(name, "LargeSquareChit")

@cli.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
async def upload(input):
    """Upload a produced game in a directory"""
    await gameUploader.uploadGame(input)

@cli.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
@click.option('-o', '--output', default=None, help='The Tabletop Playground packages directory. Such as "~/Library/Application Support/Epic/TabletopPlayground/Packages"')
async def playground(input,output):
    """Convert a produced game into a tabletop playground game"""
    if output == None:
        print("Missing --output directory.")
        return
    await gameUploader.convertToTabletopPlayground(input, output)

@cli.group()
async def rules():
    """Rules commands"""
    pass

@rules.command()
async def toHtml():
    """Convert the rules markdown to html"""
    await gameManager.convertRulesMdToHtml(".")

@rules.command()
async def toTspans():
    """Convert the rules markdown to svg tspans"""
    await gameManager.convertRulesMdToSpans(".")

@cli.command()
async def init():
    """Create the default game project here"""
    await gameManager.createTemplate()