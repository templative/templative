import asyncio

from .instructionsLoader import getLastOutputFileDirectory
from . import client

async def uploadGame(session, gameRootDirectoryPath):

    if session is None:
        raise Exception("You must provide a Game Crafter session.")

    if gameRootDirectoryPath is None:
        gameRootDirectoryPath = await getLastOutputFileDirectory()

    return await client.uploadGame(session, gameRootDirectoryPath)

