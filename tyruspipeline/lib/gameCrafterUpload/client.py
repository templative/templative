import os
import json
from os.path import isfile, join
import sys
import inflect
p = inflect.engine()

gameCrafterBaseUrl = "https://www.thegamecrafter.com"

from ..gameCrafterClient import operations as gamecrafter

def loadGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "game.json")) as game:
        return json.load(game)

def loadCompany(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "company.json")) as company:
        return json.load(company)

def loadComponentFile(componentDirectoryPath):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    with open(os.path.join(componentDirectoryPath, "component.json")) as componentFile:
        return json.load(componentFile)

def uploadGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    session = gamecrafter.login()

    game = loadGame(gameRootDirectoryPath)
    company = loadCompany(gameRootDirectoryPath)

    print("Uploading %s for %s." % (game["displayName"], company["displayName"]))

    cloudGame = gamecrafter.createGame(session, game["name"], company["gameCrafterDesignerId"])
    cloudGameFolder = gamecrafter.createFolderAtRoot(session, game["name"])

    uploadComponents(session, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"])

    gameUrl = os.path.join(gameCrafterBaseUrl, "/publish/editor/", cloudGame["id"])
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

    componentFile = loadComponentFile(componentDirectoryPath)
    componentType = componentFile["type"]
    componentName = componentFile["name"]
    componentDisplayName = componentFile["name"]
    quantity = componentFile["quantity"]
    fileInstructions = componentFile["fileInstructions"]
    backInstructions = componentFile["backInstructions"]

    if componentType != "pokerDeck":
        print("Skipping %s. The %s component type is not currently supported." % (componentDisplayName, componentType))
        return

    inflectedNumber = p.number_to_words(quantity)
    print("Uploading %s %s %s(s)" % (inflectedNumber, componentDisplayName, componentType))

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
