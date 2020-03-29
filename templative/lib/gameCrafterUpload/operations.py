
import templative.lib.gameCrafterUpload.client as client
import asyncio
import aiohttp

async def uploadGame(gameRootDirectoryPath):
    
    if gameRootDirectoryPath is None:
        print("gameRootDirectoryPath cannot be None")
        return

    async with aiohttp.ClientSession() as clientSession:
        return await client.uploadGame(clientSession, gameRootDirectoryPath)

