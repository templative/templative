import asyncio

from templative.lib.gameCrafterUpload.instructionsLoader import getLastOutputFileDirectory
import templative.lib.gameCrafterUpload.client as client

async def uploadGame(gameRootDirectoryPath):
    
    if gameRootDirectoryPath is None:
        gameRootDirectoryPath = await getLastOutputFileDirectory()    

    return await client.uploadGame(gameRootDirectoryPath)

