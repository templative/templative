import os
import json
import csv

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

def loadGameCompose(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "game-compose.json")) as gameCompose:
        return json.load(gameCompose)

def loadGameComponents(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "components.json")) as componentFile:
        return json.load(componentFile)

def loadComponentGamedata(gameRootDirectoryPath, gameCompose, gamedataFilename):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    if not gamedataFilename:
        return {}

    componentDataDirectory = gameCompose["componentDataDirectory"]
    gamedataFilenameWithExtension = "%s.csv" % (gamedataFilename)
    filepath = os.path.join(gameRootDirectoryPath, componentDataDirectory, gamedataFilenameWithExtension)
    with open(filepath) as gamedataFile:
        reader = csv.DictReader(gamedataFile, delimiter=',', quotechar='"')

        gamedata = []
        for row in reader:
            gamedata.append(row)
        return gamedata

def loadArtMetadata(gameRootDirectoryPath, gameCompose, artMetadataFilename):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    if not artMetadataFilename:
        return {}

    artMetadataDirectory = gameCompose["artMetadataDirectory"]
    artMetadataFilenameWithExtension = "%s.json" % (artMetadataFilename)
    filepath = os.path.join(gameRootDirectoryPath, artMetadataDirectory, artMetadataFilenameWithExtension)
    with open(filepath) as metadataFile:
        return json.load(metadataFile)

def dumpInstructions(filepath, data):
    if not filepath:
        raise Exception("Instructions filepath cannot be None")
    
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)
