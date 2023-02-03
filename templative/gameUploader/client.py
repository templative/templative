import os
import asyncio
from . import instructionsLoader, componentCreator, gameCrafterClient

gameCrafterBaseUrl = "https://www.thegamecrafter.com"

async def uploadGame(gameCrafterSession, gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    game = await instructionsLoader.loadGameInstructions(gameRootDirectoryPath)
    studio = await instructionsLoader.loadStudioInstructions(gameRootDirectoryPath)

    print("Uploading %s for %s." % (game["displayName"], studio["displayName"]))

    cloudGame = await gameCrafterClient.createGame(gameCrafterSession, game["name"], studio["gameCrafterDesignerId"])
    await gameCrafterClient.createActionShot(gameCrafterSession, cloudGame["id"])
    cloudGameFolder = await gameCrafterClient.createFolderAtRoot(gameCrafterSession, game["name"])

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
    if componentType == "PokerDeck":
        await componentCreator.createPokerDeck(gameCrafterSession, componentFile, cloudGame["id"], cloudGameFolderId)
        
    elif componentType == "SmallStoutBox":
        await componentCreator.createSmallStoutBox(gameCrafterSession, componentFile, cloudGame["id"], cloudGameFolderId)
        
    elif componentType == "LargeRing" or componentType == "LargeSquareChit":
        await componentCreator.createTwoSidedSlugged(gameCrafterSession, componentFile, componentType, cloudGame["id"], cloudGameFolderId)
    else:
        print("Skipping %s. The %s component type is not currently supported." % (componentFile["name"], componentType))
        
