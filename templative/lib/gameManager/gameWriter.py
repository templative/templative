import os
import json
from aiofile import AIOFile

async def dumpInstructions(filepath, data):
    if not filepath:
        raise Exception("Instructions filepath cannot be None")

    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',', ': '))

async def createGameFolder(name, outputDirectory):
    gameFolderPath = os.path.join(outputDirectory, name)
    os.mkdir(gameFolderPath)
    return gameFolderPath

async def updateLastOutputFolder(outputDirectory, gameFolderPath):
    lastFilepath = os.path.join(outputDirectory, ".last")
    async with AIOFile(lastFilepath, "w") as lastFile:
        await lastFile.write(gameFolderPath)

async def createComponentFolder(name, outputDirectory):
    componentDirectory = os.path.join(outputDirectory, name)
    os.mkdir(componentDirectory)
    return componentDirectory

async def copyCompanyFromGameFolderToOutput(company, gameFolderPath):
    companyFilepath = os.path.join(gameFolderPath, "company.json")
    await dumpInstructions(companyFilepath, company)

async def copyGameFromGameFolderToOutput(game, gameFolderPath):
    companyFilepath = os.path.join(gameFolderPath, "game.json")
    await dumpInstructions(companyFilepath, game)

