import os
import json
from aiofile import AIOFile

async def loadGameInstructions(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")
    
    gameComposeFilepath = os.path.join(gameRootDirectoryPath, "game.json")
    async with AIOFile(gameComposeFilepath) as game:
        return json.loads(await game.read())

async def loadStudioInstructions(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    async with AIOFile(os.path.join(gameRootDirectoryPath, "studio.json")) as studio:
        return json.loads(await studio.read())

async def loadComponentInstructions(componentDirectoryPath):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    async with AIOFile(os.path.join(componentDirectoryPath, "component.json")) as componentFile:
        return json.loads(await componentFile.read())

async def loadGameCompose():
    async with AIOFile("game-compose.json") as gameCompose:
        return json.loads(await gameCompose.read())

async def getLastOutputFileDirectory():
    gameCompose = await loadGameCompose()
    outputDirectory = gameCompose["outputDirectory"]
    lastFileDirectory = os.path.join(outputDirectory, ".last")

    async with AIOFile(lastFileDirectory) as lastFile:
        return await lastFile.read()