import asyncio
import aiohttp
from templative.lib.gameCrafterUpload.instructionsLoader import getLastOutputFileDirectory
import templative.lib.gameCrafterUpload.client as client

async def uploadGame(gameRootDirectoryPath):
    
    if gameRootDirectoryPath is None:
        gameRootDirectoryPath = await getLastOutputFileDirectory()    

    async with aiohttp.ClientSession() as clientSession:
        return await client.uploadGame(clientSession, gameRootDirectoryPath)

