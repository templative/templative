import os
import json
import csv

from ..svgmanipulation import operations

def loadGame(gameRootDirectoryPath):
    with open("%s/game.json" % gameRootDirectoryPath) as gameFile:
        return json.load(gameFile)

def loadGameComponents(gameRootDirectoryPath):
    with open("%s/components.json" % gameRootDirectoryPath) as gameFile:
        return json.load(gameFile)'

def processGameComponent(gameRootDirectoryPath, component):
    gamedata = getComponentGamedata(gameRootDirectoryPath, component["gamedata"])
    if not gamedata:
        return
    
    artMetadata = getArtMetadata(gameRootDirectoryPath, component["artMetadata"])
    if not artMetadata:
        return

    # For every item in game data process component using art metadata
    # operations.processComponent()

def getComponentGamedata(gameRootDirectoryPath, gamedataFileName):
    return {}

def getArtMetadata(gameRootDirectoryPath, artMetadataFileName):
    return {}
