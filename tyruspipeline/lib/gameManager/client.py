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

def loadGameComponents(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open("%s/components.json" % gameRootDirectoryPath) as componentFile:
        return json.load(componentFile)

def loadComponentGamedata(gameRootDirectoryPath, gamedataFilename):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    if not gamedataFilename:
        return {}

    filepath = '%s/componentData/%s.csv' % (gameRootDirectoryPath, gamedataFilename)
    with open(filepath) as gamedataFile:
        reader = csv.DictReader(gamedataFile, delimiter=',', quotechar='"')

        gamedata = []
        for row in reader:
            gamedata.append(row)
        return gamedata

def loadArtMetadata(gameRootDirectoryPath, artMetadataFilename):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    if not artMetadataFilename:
        return {}

    filepath = '%s/componentArtMetadata/%s.json' % (gameRootDirectoryPath, artMetadataFilename)
    with open(filepath) as metadataFile:
        return json.load(metadataFile)

def dumpInstructions(filepath, data):
    if not filepath:
        raise Exception("Instructions filepath cannot be None")
    
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)
