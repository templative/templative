from .instructionsLoader import getLastOutputFileDirectory
from . import client, gameCrafterClient

async def uploadGame(gameRootDirectoryPath):
    session = await gameCrafterClient.login()

    if session is None:
        raise Exception("You must provide a Game Crafter session.")

    if gameRootDirectoryPath is None:
        gameRootDirectoryPath = await getLastOutputFileDirectory()

    result = await client.uploadGame(session, gameRootDirectoryPath)
    await gameCrafterClient.logout(session)
    return result

