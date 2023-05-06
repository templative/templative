import os
import asyncio

from . import componentCreator
from .. import instructionsLoader, gameCrafterClient

gameCrafterBaseUrl = "https://www.thegamecrafter.com"

async def uploadGame(gameCrafterSession, gameRootDirectoryPath, isPublish):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    game = await instructionsLoader.loadGameInstructions(gameRootDirectoryPath)
    studio = await instructionsLoader.loadStudioInstructions(gameRootDirectoryPath)

    print("Uploading %s for %s." % (game["displayName"], studio["displayName"]))

    cloudGame = await gameCrafterClient.createGame(gameCrafterSession, game, studio["gameCrafterDesignerId"], isPublish)
    await gameCrafterClient.createActionShot(gameCrafterSession, cloudGame["id"])
    cloudGameFolder = await gameCrafterClient.createFolderAtRoot(gameCrafterSession, game["name"])

    tasks = []
    tasks.append(asyncio.create_task(createComponents(gameCrafterSession, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"], isPublish)))
    tasks.append(asyncio.create_task(componentCreator.createRules(gameCrafterSession, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"])))
    for task in tasks:
        await task

    gameUrl = "%s%s%s"%(gameCrafterBaseUrl, "/make/games/", cloudGame["id"])
    print("Uploads finished for %s, visit %s" % (cloudGame["name"], gameUrl))
    return gameUrl

async def createComponents(gameCrafterSession, outputDirectory, cloudGame, cloudGameFolderId, isPublish):
    if not outputDirectory:
        raise Exception("outputDirectory cannot be None")

    tasks = []
    for directoryPath in next(os.walk(outputDirectory))[1]:
        componentDirectoryPath = "%s/%s" % (outputDirectory, directoryPath)
        tasks.append(asyncio.create_task(createComponent(gameCrafterSession, componentDirectoryPath, cloudGame, cloudGameFolderId, isPublish)))

    for task in tasks:
        await task

async def createComponent(gameCrafterSession, componentDirectoryPath, cloudGame, cloudGameFolderId, isPublish):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    componentFile = await instructionsLoader.loadComponentInstructions(componentDirectoryPath)

    isDebugInfo = False if not "isDebugInfo" in componentFile else componentFile["isDebugInfo"]
    if isDebugInfo and isPublish:
        print("!!! Skipping %s. It is debug only and we are publishing." % (componentFile["name"]))
        return

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
        "MediumSquareChit": createTwoSidedSluggedTask,
        "SmallSquareChit": createTwoSidedSluggedTask,

        "LargeHexTile": createTwoSidedSluggedTask,
        "MediumHexTile": createTwoSidedSluggedTask,
        "SmallHexTile": createTwoSidedSluggedTask,

        "LargeCircleChit": createTwoSidedSluggedTask,
        "MediumCircleChit": createTwoSidedSluggedTask,
        "SmallCircleChit": createTwoSidedSluggedTask,


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

    missingDirectComponentMatch = not componentType in componentTasks

    componentTypeTokens = componentType.split("_")
    isStockComponent = componentTypeTokens[0].upper() == "STOCK" 

    if missingDirectComponentMatch and not isStockComponent:
        print("!!! Skipping %s. The %s component type is not currently supported." % (componentFile["name"], componentType))
        return
    
    if isStockComponent:
        await componentCreator.createStockPart(gameCrafterSession, componentFile, cloudGame["id"])
        return
    
    await componentTasks[componentType](gameCrafterSession, componentFile, componentType, cloudGame["id"], cloudGameFolderId)
        
