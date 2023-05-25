import os
from aiofile import AIOFile
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

async def lookForPlaygroundFile():
    playgroundFileLocation = "./.playground"
    if not os.path.exists(playgroundFileLocation):
        return None
    
    async with AIOFile(playgroundFileLocation, mode="r") as playground:
        return await playground.read()
    
async def writePlaygroundFile(outputPath):
    playgroundFileLocation = os.path.join("./", ".playground")
    async with AIOFile(playgroundFileLocation, mode="w") as playground:
        await playground.write(outputPath)

async def getPlaygroundDirectory(inputedPlaygroundDirectory):
    if inputedPlaygroundDirectory != None:
        return inputedPlaygroundDirectory
    
    return await lookForPlaygroundFile()  

async def convertToTabletopPlayground(gameRootDirectoryPath, inputedPlaygroundDirectory):
    if gameRootDirectoryPath is None:
        gameRootDirectoryPath = await getLastOutputFileDirectory()

    playgroundDirectory = getPlaygroundDirectory(inputedPlaygroundDirectory)
    if playgroundDirectory == None:
        print("Missing --output directory.")
        return
    await writePlaygroundFile(playgroundDirectory)

    return await tabletopPlayground.convertToTabletopPlayground(gameRootDirectoryPath, playgroundDirectory)
