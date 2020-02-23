import os
import json
from os.path import isfile, join
import sys

gameCrafterBaseUrl = "https://www.thegamecrafter.com"

from ..gameCrafterClient import operations as gamecrafter

def loadGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open("%s/game.json" % gameRootDirectoryPath) as game:
        return json.load(game)

def loadCompany(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open("%s/company.json" % gameRootDirectoryPath) as company:
        return json.load(company)

def loadComponentFile(componentDirectoryPath):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    with open("%s/component.json" % componentDirectoryPath) as componentFile:
        return json.load(componentFile)

def uploadGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    session = gamecrafter.login()

    game = loadGame(gameRootDirectoryPath)
    company = loadCompany(gameRootDirectoryPath)

    print("Uploading %s for %s." % (game["name"], company["name"]))

    cloudGame = gamecrafter.createGame(session, game["name"], company["gameCrafterDesignerId"])
    cloudGameFolder = gamecrafter.createFolderAtRoot(session, game["name"])

    uploadComponents(session, gameRootDirectoryPath, cloudGame, cloudGameFolder["id"])

    gameUrl = "%s/publish/editor/%s" % (gameCrafterBaseUrl, cloudGame["id"])
    print("Uploads finished for %s, visit %s" %(cloudGame["name"], gameUrl))
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
    fileInstructions = componentFile["fileInstructions"]

    cloudComponentFolder = gamecrafter.createFolderAtParent(session, componentName, cloudGameFolderId)
    cloudPokerDeck = gamecrafter.createPokerDeck(session, componentName, cloudGame["id"], None)

    if componentType != "pokerDeck":
        print("Skipping %s. The %s component type is not currently supported." % (componentName, componentType))
        return
    
    print("Uploading %s %s" % (componentType, componentName))
    
    for instructions in fileInstructions:
        uploadPiece(session, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])

def uploadPiece(session, instructions, deckId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    print("Uploading %s" % (filepath))

    cloudFile = gamecrafter.uploadFile(session, filepath, cloudComponentFolderId)
    pokerCard = gamecrafter.createPokerCard(session, name, deckId, quantity, cloudFile["id"])
