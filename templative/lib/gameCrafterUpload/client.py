import os
import json
from os.path import isfile, join
import sys
import threading
from multiprocessing import Process

gameCrafterBaseUrl = "https://www.thegamecrafter.com"

from templative.lib.gameCrafterClient import operations as gamecrafter
from templative.lib.gameCrafterUpload import instructionsLoader
from templative.lib.gameCrafterUpload import componentCreator

async def uploadGame(client, gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    session = await gamecrafter.login(client)

    game = await instructionsLoader.loadGameInstructions(gameRootDirectoryPath)
    company = await instructionsLoader.loadCompanyInstructions(gameRootDirectoryPath)

    print("Uploading %s for %s." % (game["displayName"], company["displayName"]))

    cloudGame = await gamecrafter.createGame(client, session, game["name"], company["gameCrafterDesignerId"])
    cloudGameFolder = await gamecrafter.createFolderAtRoot(client, session, game["name"])

    await createComponents(client,session, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"])
    await componentCreator.createRules(client, session, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"])

    gameUrl = "%s%s%s"%(gameCrafterBaseUrl, "/publish/editor/", cloudGame["id"])
    print("Uploads finished for %s, visit %s" % (cloudGame["name"], gameUrl))
    return gameUrl

async def createComponents(client,session, outputDirectory, cloudGame, cloudGameFolderId):
    if not outputDirectory:
        raise Exception("outputDirectory cannot be None")

    threads = []
    for directoryPath in next(os.walk(outputDirectory))[1]:
        componentDirectoryPath = "%s/%s" % (outputDirectory, directoryPath)
        threads.append(Proccess(await createComponent(client, session, componentDirectoryPath, cloudGame, cloudGameFolderId)))
    
    for thread in threads:
        thread.start()
        thread.join()
        
    print("Done with threads")

async def createComponent(client, session, componentDirectoryPath, cloudGame, cloudGameFolderId):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    componentFile = await instructionsLoader.loadComponentInstructions(componentDirectoryPath)

    componentType = componentFile["type"]
    if componentType == "pokerDeck":
        await componentCreator.createPokerDeck(client, session, componentFile, cloudGame["id"], cloudGameFolderId)
        return
    elif componentType == "smallStoutBox":
        await componentCreator.createSmallStoutBox(client, session, componentFile, cloudGame["id"], cloudGameFolderId)
        return
     
    print("Skipping %s. The %s component type is not currently supported." % (componentFile["displayName"], componentType))   
