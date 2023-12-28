import asyncclick as click
from templative.lib.distribute.gameCrafter.client import uploadGame
from templative.lib.distribute.gameCrafter.accountManagement import listGames, deletePageOfGames
from templative.lib.distribute.gameCrafter.util.gameCrafterSession import login, logout
from templative.lib.manage.instructionsLoader import getLastOutputFileDirectory

baseUrl = "https://www.thegamecrafter.com"

@click.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
@click.option('-p/-d', '--publish/--debug', default=False, required=False, type=bool, help='Whether to treat this as the official release.')
@click.option('-s/-n', '--stock/--nostock', default=True, required=False, type=bool, help='Whether stock parts are included -s or not -n.')
@click.option('-a/-y', '--asynchronous/--synchronous', default=True, required=False, type=bool, help='Whether upload requests happen all at once -a or one after the other -y.')
@click.option('-u/-o', '--proofed/--proof', default=True, required=False, type=bool, help='Whether images are considered proofed already -u or not -o.')
async def upload(input, publish, stock, asynchronous, proofed):
    """Upload a produced game in a directory"""
    session = await login()

    if session is None:
        raise Exception("You must provide a Game Crafter session.")

    if input is None:
        input = await getLastOutputFileDirectory()

    await uploadGame(session, input, publish, stock, asynchronous, 1 if proofed else 0)
    await logout(session)

@click.command()
async def list():
    """List uploaded games"""
    session = await login()

    if session is None:
        raise Exception("You must provide a Game Crafter session.")

    await listGames(session)
    await logout(session)

@click.command()
async def deletegames():
    """Delete a page of games"""
    session = await login()

    if session is None:
        raise Exception("You must provide a Game Crafter session.")

    await deletePageOfGames(session)
    await logout(session)




