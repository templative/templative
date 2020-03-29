import os
import json
from os.path import isfile, join
import sys

gameCrafterBaseUrl = "https://www.thegamecrafter.com"

from templative.lib.gameCrafterClient import operations as gamecrafter
from templative.lib.gameCrafterUpload import instructionsLoader
from templative.lib.gameCrafterUpload import componentCreator

def uploadGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    session = gamecrafter.login()

    game = instructionsLoader.loadGameInstructions(gameRootDirectoryPath)
    company = instructionsLoader.loadCompanyInstructions(gameRootDirectoryPath)

    print("Uploading %s for %s." % (game["displayName"], company["displayName"]))

    cloudGame = gamecrafter.createGame(session, game["name"], company["gameCrafterDesignerId"])
    cloudGameFolder = gamecrafter.createFolderAtRoot(session, game["name"])

    createComponents(session, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"])

    componentCreator.createRules(session, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"])

    gameUrl = "%s%s%s"%(gameCrafterBaseUrl, "/publish/editor/", cloudGame["id"])
    print("Uploads finished for %s, visit %s" % (cloudGame["name"], gameUrl))
    return gameUrl

def createComponents(session, outputDirectory, cloudGame, cloudGameFolderId):
    if not outputDirectory:
        raise Exception("outputDirectory cannot be None")

    for directoryPath in next(os.walk(outputDirectory))[1]:
        componentDirectoryPath = "%s/%s" % (outputDirectory, directoryPath)
        createComponent(session, componentDirectoryPath, cloudGame, cloudGameFolderId)

def createComponent(session, componentDirectoryPath, cloudGame, cloudGameFolderId):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    componentFile = instructionsLoader.loadComponentInstructions(componentDirectoryPath)

    componentType = componentFile["type"]
    if componentType == "pokerDeck":
        componentCreator.createPokerDeck(session, componentFile, cloudGame["id"], cloudGameFolderId)
        return
    elif componentType == "smallStoutBox":
        componentCreator.createSmallStoutBox(session, componentFile, cloudGame["id"], cloudGameFolderId)
        return
     
    print("Skipping %s. The %s component type is not currently supported." % (componentFile["displayName"], componentType))   
