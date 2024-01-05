import os
import asyncclick as click
from templative.lib.distribute.gameCrafter.client import uploadGame
from templative.lib.distribute.gameCrafter.accountManagement import listGames, deletePageOfGames
from templative.lib.distribute.gameCrafter.util.gameCrafterSession import login, logout
from templative.lib.manage.instructionsLoader import getLastOutputFileDirectory

baseUrl = "https://www.thegamecrafter.com"

def getCredentialsFromEnv():
    publicApiKey = os.environ.get('THEGAMECRAFTER_PUBLIC_KEY')
    if not publicApiKey:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PUBLIC_KEY. Value is %s' % publicApiKey)

    userName = os.environ.get('THEGAMECRAFTER_USER')
    if not userName:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_USER. Value is %s' % userName)

    userPassword = os.environ.get('THEGAMECRAFTER_PASSWORD')
    if not userPassword:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PASSWORD. Value is %s' % userPassword)
    return publicApiKey, userName, userPassword

@click.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
@click.option('-p/-d', '--publish/--debug', default=False, required=False, type=bool, help='Whether to treat this as the official release.')
@click.option('-s/-n', '--stock/--nostock', default=True, required=False, type=bool, help='Whether stock parts are included -s or not -n.')
@click.option('-a/-y', '--asynchronous/--synchronous', default=True, required=False, type=bool, help='Whether upload requests happen all at once -a or one after the other -y.')
@click.option('-u/-o', '--proofed/--proof', default=True, required=False, type=bool, help='Whether images are considered proofed already -u or not -o.')
async def upload(input, publish, stock, asynchronous, proofed):
    """Upload a produced game in a directory"""
    publicApiKey, userName, userPassword = getCredentialsFromEnv()
    session = await login(publicApiKey, userName, userPassword)

    if session is None:
        raise Exception("You must provide a Game Crafter session.")

    if input is None:
        input = await getLastOutputFileDirectory()

    await uploadGame(session, input, publish, stock, asynchronous, 1 if proofed else 0)
    await logout(session)

@click.command()
async def list():
    """List uploaded games"""
    publicApiKey, userName, userPassword = getCredentialsFromEnv()
    session = await login(publicApiKey, userName, userPassword)

    if session is None:
        raise Exception("You must provide a Game Crafter session.")

    await listGames(session)
    await logout(session)

@click.command()
async def deletegames():
    """Delete a page of games"""
    publicApiKey, userName, userPassword = getCredentialsFromEnv()
    session = await login(publicApiKey, userName, userPassword)

    if session is None:
        raise Exception("You must provide a Game Crafter session.")

    await deletePageOfGames(session)
    await logout(session)




