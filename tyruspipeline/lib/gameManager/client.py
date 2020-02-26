import os
import json
import csv

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

def loadGameCompose(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open("%s/game-compose.json" % gameRootDirectoryPath) as gameCompose:
        return json.load(gameCompose)

def loadGameComponents(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open("%s/components.json" % gameRootDirectoryPath) as componentFile:
        return json.load(componentFile)

def loadComponentGamedata(gameRootDirectoryPath, gameCompose, gamedataFilename):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    if not gamedataFilename:
        return {}

    componentDataDirectory = gameCompose["componentDataDirectory"]

    filepath = '%s/%s/%s.csv' % (gameRootDirectoryPath, componentDataDirectory, gamedataFilename)
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

    filepath = '%s/%s/%s.json' % (gameRootDirectoryPath, artMetadataDirectory, artMetadataFilename)
    with open(filepath) as metadataFile:
        return json.load(metadataFile)

def dumpInstructions(filepath, data):
    if not filepath:
        raise Exception("Instructions filepath cannot be None")
    
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)
