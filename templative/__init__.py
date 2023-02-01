import click
import asyncio
from templative import gameManager, gameUploader
from functools import wraps

def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper

@click.group()
def cli():
    """Templative CLI"""
    pass

@cli.command()
@coro
async def produce():
    """Produce the game in the current directory"""
    await gameManager.produceGame(".")

@cli.command()
@coro
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
async def upload(input):
    """Upload a produced game in a directory"""
    await gameUploader.uploadGame(input)

@cli.command()
async def init():
    """Deprecated - Create the default game project here"""
    print("Init is not implemented.")