import asyncclick as click
from templative import gameManager, gameUploader

@click.group()
async def cli():
    """Templative CLI"""
    pass

@cli.command()
async def produce():
    """Produce the game in the current directory"""
    await gameManager.produceGame(".")

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
async def init():
    """Deprecated - Create the default game project here"""
    print("Init is not implemented.")