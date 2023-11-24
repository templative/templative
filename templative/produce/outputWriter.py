import os
import json
from aiofile import AIOFile

async def dumpInstructions(filepath, data):
    if not filepath:
        raise Exception("Instructions filepath cannot be None")

    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',', ': '))

async def createGameFolder(gameRootDirectoryPath, outputDirectory, name):
    gameFolderPath = os.path.join(gameRootDirectoryPath, outputDirectory, name)
    os.mkdir(gameFolderPath)
    return gameFolderPath

async def updateLastOutputFolder(gameRootDirectoryPath, outputDirectory, gameFolderPath):
    lastFilepath = os.path.join(gameRootDirectoryPath, outputDirectory, ".last")
    async with AIOFile(lastFilepath, "w") as lastFile:
        await lastFile.write(gameFolderPath)

async def createComponentFolder(name, outputDirectory):
    componentDirectory = os.path.join(outputDirectory, name)
    os.mkdir(componentDirectory)
    return componentDirectory

async def copyStudioFromGameFolderToOutput(studio, gameFolderPath):
    studioFilepath = os.path.join(gameFolderPath, "studio.json")
    await dumpInstructions(studioFilepath, studio)

async def copyGameFromGameFolderToOutput(game, gameFolderPath):
    studioFilepath = os.path.join(gameFolderPath, "game.json")
    await dumpInstructions(studioFilepath, game)

