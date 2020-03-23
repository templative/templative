import os
import json
from os.path import isfile, join
import sys

gameCrafterBaseUrl = "https://www.thegamecrafter.com"

from templative.lib.gameCrafterClient import operations as gamecrafter
from templative.lib.gameCrafterUpload import instructionsLoader

def uploadGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    session = gamecrafter.login()

    game = instructionsLoader.loadGameInstructions(gameRootDirectoryPath)
    company = instructionsLoader.loadCompanyInstructions(gameRootDirectoryPath)

    print("Uploading %s for %s." % (game["displayName"], company["displayName"]))

    cloudGame = gamecrafter.createGame(session, game["name"], company["gameCrafterDesignerId"])
    cloudGameFolder = gamecrafter.createFolderAtRoot(session, game["name"])

    uploadComponents(session, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"])

    gameUrl = "%s%s%s"%(gameCrafterBaseUrl, "/publish/editor/", cloudGame["id"])
    print("Uploads finished for %s, visit %s" % (cloudGame["name"], gameUrl))
    return gameUrl

def uploadComponents(session, outputDirectory, cloudGame, cloudGameFolderId):
    if not outputDirectory:
        raise Exception("outputDirectory cannot be None")

    for directoryPath in next(os.walk(outputDirectory))[1]:
        componentDirectoryPath = "%s/%s" % (outputDirectory, directoryPath)
        uploadComponent(session, componentDirectoryPath, cloudGame, cloudGameFolderId)

def uploadComponent(session, componentDirectoryPath, cloudGame, cloudGameFolderId):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    componentFile = instructionsLoader.loadComponentInstructions(componentDirectoryPath)
    componentType = componentFile["type"]
    componentName = componentFile["name"]
    componentDisplayName = componentFile["name"]
    quantity = componentFile["quantity"]
    fileInstructions = componentFile["fileInstructions"]
    backInstructions = componentFile["backInstructions"]

    if componentType != "pokerDeck":
        print("Skipping %s. The %s component type is not currently supported." % (componentDisplayName, componentType))
        return

    print("Uploading %s %s %s(s)" % (quantity, componentDisplayName, componentType))

    cloudComponentFolder = gamecrafter.createFolderAtParent(session, componentName, cloudGameFolderId)
    backImageId = uploadBack(session, backInstructions, cloudComponentFolder["id"])
    cloudPokerDeck = gamecrafter.createPokerDeck(session, componentName, quantity, cloudGame["id"], backImageId)

    for instructions in fileInstructions:
        uploadPokerCardPiece(session, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])

def uploadBack(session, instructions, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    print("Uploading Back %s" % (filepath))

    cloudFile = gamecrafter.uploadFile(session, filepath, cloudComponentFolderId)
    return cloudFile["id"]

def uploadPokerCardPiece(session, instructions, deckId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    print("Uploading %s" % (filepath))

    cloudFile = gamecrafter.uploadFile(session, filepath, cloudComponentFolderId)
    pokerCard = gamecrafter.createPokerCard(session, name, deckId, quantity, cloudFile["id"])
