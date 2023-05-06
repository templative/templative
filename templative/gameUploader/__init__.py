from .gameCrafterClient import client
from .instructionsLoader import getLastOutputFileDirectory
from . import gameCrafterClient, tabletopPlayground

async def uploadGame(gameRootDirectoryPath, isPublish):
    session = await gameCrafterClient.login()

    if session is None:
        raise Exception("You must provide a Game Crafter session.")

    if gameRootDirectoryPath is None:
        gameRootDirectoryPath = await getLastOutputFileDirectory()

    result = await client.uploadGame(session, gameRootDirectoryPath, isPublish)
    await gameCrafterClient.logout(session)
    return result

async def convertToTabletopPlayground(gameRootDirectoryPath, playgroundDirectory):
    if gameRootDirectoryPath is None:
        gameRootDirectoryPath = await getLastOutputFileDirectory()

    return await tabletopPlayground.convertToTabletopPlayground(gameRootDirectoryPath, playgroundDirectory)
