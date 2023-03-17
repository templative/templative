import os
import asyncio

from . import componentCreator
from .. import instructionsLoader, gameCrafterClient

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
    
    if componentFile["quantity"] == 0:
        return
    
    createDeckTask = componentCreator.createDeck
    createTwoSidedSluggedTask = componentCreator.createTwoSidedSlugged
    createTwoSidedBoxTask = componentCreator.createTwoSidedBox
    createTuckBoxTask = componentCreator.createTuckBox
    createTwoSidedTask = componentCreator.createTwoSided
    
    componentTasks = {
        # "CustomColorD4": createDieTask,
        # "CustomColorD6": createDieTask,
        # "CustomColorD8": createDieTask,
        
        "PokerDeck": createDeckTask,
        "MicroDeck": createDeckTask,
        "MiniDeck": createDeckTask,
        "MintTinDeck": createDeckTask,
        "HexDeck": createDeckTask,

        "SmallStoutBox": createTwoSidedBoxTask,
        "MediumStoutBox": createTwoSidedBoxTask,
        "LargeStoutBox": createTwoSidedBoxTask,
        "MintTin": createTwoSidedBoxTask,

        "LargeRing": createTwoSidedSluggedTask,
        "MediumRing": createTwoSidedSluggedTask,
        "SmallRing": createTwoSidedSluggedTask,

        "LargeSquareChit": createTwoSidedSluggedTask,
        "LargeSquareChit": createTwoSidedSluggedTask,

        "PokerTuckBox36": createTuckBoxTask,
        "PokerTuckBox54": createTuckBoxTask,
        "PokerTuckBox72": createTuckBoxTask,
        "PokerTuckBox90": createTuckBoxTask,
        "PokerTuckBox108": createTuckBoxTask,

        "PokerFolio": createTwoSidedTask,
        "MintTinFolio": createTwoSidedTask,
        "MintTinAccordion4": createTwoSidedTask,
        "MintTinAccordion6": createTwoSidedTask,
        "MintTinAccordion8": createTwoSidedTask,
    }

    if not componentType in componentTasks:
        print("Skipping %s. The %s component type is not currently supported." % (componentFile["name"], componentType))
        return
    
    await componentTasks[componentType](gameCrafterSession, componentFile, componentType, cloudGame["id"], cloudGameFolderId)
        
