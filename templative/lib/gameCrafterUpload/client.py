import os
from os.path import isfile, join
import json
import sys
import asyncio
from .. import gamecrafterclient as gamecrafter
from . import instructionsLoader, componentCreator

gameCrafterBaseUrl = "https://www.thegamecrafter.com"

async def uploadGame(gameCrafterSession, gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    game = await instructionsLoader.loadGameInstructions(gameRootDirectoryPath)
    company = await instructionsLoader.loadCompanyInstructions(gameRootDirectoryPath)

    print("Uploading %s for %s." % (game["displayName"], company["displayName"]))

    cloudGame = await gamecrafter.createGame(gameCrafterSession, game["name"], company["gameCrafterDesignerId"])
    cloudGameFolder = await gamecrafter.createFolderAtRoot(gameCrafterSession, game["name"])

    tasks = []
    tasks.append(asyncio.create_task(createComponents(gameCrafterSession, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"])))
    tasks.append(asyncio.create_task(componentCreator.createRules(gameCrafterSession, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"])))
    for task in tasks:
        await task

    gameUrl = "%s%s%s"%(gameCrafterBaseUrl, "/make/games/", cloudGame["id"])
    print("Uploads finished for %s, visit %s" % (cloudGame["name"], gameUrl))
    return gameUrl

async def createComponents(gameCrafterSession, outputDirectory, cloudGame, cloudGameFolderId):
    if not outputDirectory:
        raise Exception("outputDirectory cannot be None")

    tasks = []
    for directoryPath in next(os.walk(outputDirectory))[1]:
        componentDirectoryPath = "%s/%s" % (outputDirectory, directoryPath)
        tasks.append(asyncio.create_task(createComponent(gameCrafterSession, componentDirectoryPath, cloudGame, cloudGameFolderId)))

    for task in tasks:
        await task

async def createComponent(gameCrafterSession, componentDirectoryPath, cloudGame, cloudGameFolderId):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    componentFile = await instructionsLoader.loadComponentInstructions(componentDirectoryPath)

    componentType = componentFile["type"]
    if componentType == "pokerDeck":
        await componentCreator.createPokerDeck(gameCrafterSession, componentFile, cloudGame["id"], cloudGameFolderId)
        return
    elif componentType == "smallStoutBox":
        await componentCreator.createSmallStoutBox(gameCrafterSession, componentFile, cloudGame["id"], cloudGameFolderId)
        return

    print("Skipping %s. The %s component type is not currently supported." % (componentFile["displayName"], componentType))
