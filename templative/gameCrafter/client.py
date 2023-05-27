import asyncio
from templative.gameManager import instructionsLoader
from .advertisementCreator import createActionShot, createAdvertisementImages
from .componentCreator import createComponents, createRules
from .fileFolderManager import createGame, createFolderAtRoot

gameCrafterBaseUrl = "https://www.thegamecrafter.com"

async def uploadGame(gameCrafterSession, gameRootDirectoryPath, isPublish):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    game = await instructionsLoader.loadGameInstructions(gameRootDirectoryPath)
    studio = await instructionsLoader.loadStudioInstructions(gameRootDirectoryPath)

    print("Uploading %s for %s." % (game["displayName"], studio["displayName"]))

    cloudGame = await createGame(gameCrafterSession, game, studio["gameCrafterDesignerId"], isPublish)
    await createActionShot(gameCrafterSession, cloudGame["id"])
    cloudGameFolder = await createFolderAtRoot(gameCrafterSession, game["name"])

    tasks = []
    tasks.append(asyncio.create_task(createComponents(gameCrafterSession, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"], isPublish)))
    tasks.append(asyncio.create_task(createRules(gameCrafterSession, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"])))
    # tasks.append(asyncio.create_task(createAdvertisementImages(gameCrafterSession)))
    for task in tasks:
        await task

    gameUrl = "%s%s%s"%(gameCrafterBaseUrl, "/make/games/", cloudGame["id"])
    print("Uploads finished for %s, visit %s" % (cloudGame["name"], gameUrl))
    return gameUrl



