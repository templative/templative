import asyncclick as click
from .client import uploadGame
from .util.gameCrafterSession import login, logout
from templative.gameManager.instructionsLoader import getLastOutputFileDirectory

baseUrl = "https://www.thegamecrafter.com"

@click.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
@click.option('-p/-d', '--publish/--debug', default=False, required=False, type=bool, help='Whether to treat this as the official release.')
async def upload(input, publish):
    """Upload a produced game in a directory"""
    session = await login()

    if session is None:
        raise Exception("You must provide a Game Crafter session.")

    if input is None:
        input = await getLastOutputFileDirectory()

    await uploadGame(session, input, publish)
    await logout(session)




