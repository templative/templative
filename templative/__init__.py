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

@cli.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
async def upload(input):
    """Upload a produced game in a directory"""
    await gameUploader.uploadGame(input)

@cli.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
async def playground(input):
    """Convert a produced game into a tabletop playground game"""
    await gameUploader.convertToTabletopPlayground(input)

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