import os
import json
import csv

def loadGameCompose(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "game-compose.json")) as gameCompose:
        return json.load(gameCompose)

def loadComponentCompose(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "component-compose.json")) as componentFile:
        return json.load(componentFile)

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

def loadPiecesGamedata(gameRootDirectoryPath, gameCompose, piecesGamedataFilename):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    if not piecesGamedataFilename:
        return {}

    piecesGamedataDirectory = gameCompose["piecesGamedataDirectory"]
    piecesGamedataFilenameWithExtension = "%s.csv" % (piecesGamedataFilename)
    filepath = os.path.join(gameRootDirectoryPath, piecesGamedataDirectory, piecesGamedataFilenameWithExtension)
    with open(filepath) as gamedataFile:
        reader = csv.DictReader(gamedataFile, delimiter=',', quotechar='"')

        gamedata = []
        for row in reader:
            gamedata.append(row)
        return gamedata

def loadComponentGamedata(gameRootDirectoryPath, gameCompose, componentGamedataFilename):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    if not componentGamedataFilename:
        return {}

    componentGamedataDirectory = gameCompose["componentGamedataDirectory"]
    componentGamedataFilenameWithExtension = "%s.json" % (componentGamedataFilename)
    filepath = os.path.join(gameRootDirectoryPath, componentGamedataDirectory, componentGamedataFilenameWithExtension)
    with open(filepath) as componentGamedata:
        return json.load(componentGamedata)

def loadArtdata(gameRootDirectoryPath, gameCompose, artdataFilename):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    if not artdataFilename:
        return {}

    artdataDirectory = gameCompose["artdataDirectory"]
    artdataFilenameWithExtension = "%s.json" % (artdataFilename)
    filepath = os.path.join(gameRootDirectoryPath, artdataDirectory, artdataFilenameWithExtension)
    with open(filepath) as metadataFile:
        return json.load(metadataFile)