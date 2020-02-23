import uuid
import os
from datetime import datetime

import client as client
from ..svgmanipulation import operations as processor

def produceGame(gameRootDirectoryPath, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = client.loadGame(gameRootDirectoryPath)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    uniqueGameName = ("%s_%s_%s_%s" % (game["name"], game["version"], game["versionName"], timestamp)).replace(" ", "")
    game["name"] = uniqueGameName

    gameFolderPath = createGameFolder(game["name"], outputDirectory)
    print("Producing %s" % gameFolderPath)

    copyCompanyFromGameFolderToOutput(gameRootDirectoryPath, gameFolderPath)
    copyGameFromGameFolderToOutput(game, gameFolderPath)
    
    components = client.loadGameComponents(gameRootDirectoryPath)
    for component in components["components"]:
        produceGameComponent(gameRootDirectoryPath, game, component, gameFolderPath)

    return gameFolderPath

def createGameFolder(name, outputDirectory):    
    gameFolderPath = "%s/%s" % (outputDirectory, name)
    os.mkdir(gameFolderPath)
    return gameFolderPath

def copyCompanyFromGameFolderToOutput(gameRootDirectoryPath, gameFolderPath):
    company = client.loadCompany(gameRootDirectoryPath)
    companyFilepath = "%s/company.json" % (gameFolderPath)
    client.dumpInstructions(companyFilepath, company)

def copyGameFromGameFolderToOutput(game, gameFolderPath):
    gameFilepath = "%s/game.json" % (gameFolderPath)
    client.dumpInstructions(gameFilepath, game)

def produceGameComponent(gameRootDirectoryPath, game, component, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    componentName = component["name"]
    
    componentGamedata = client.loadComponentGamedata(gameRootDirectoryPath, component["gamedataFilename"])
    if not componentGamedata or componentGamedata == {}:
        print("Skipping %s component due to missing game data." % componentName)
        return

    componentArtMetadata = client.loadArtMetadata(gameRootDirectoryPath, component["artMetadataFilename"])
    if not componentArtMetadata or componentArtMetadata == {}:
        print("Skipping %s component due to missing front art metadata." % componentName)
        return

    componentBackArtMetadata = client.loadArtMetadata(gameRootDirectoryPath, component["backArtMetadataFilename"])
    if not componentBackArtMetadata or componentBackArtMetadata == {}:
        print("Skipping %s component due to missing back art metadata." % componentName)
        return

    print("Creating art assets for %s component." % (component["name"]))

    componentName = component["name"].replace(" ", "")
    componentDirectory = "%s/%s" % (outputDirectory, componentName)
    os.mkdir(componentDirectory)

    componentInstructionFilepath = "%s/component.json" % (componentDirectory)

    fileInstructionSets = processor.getInstructionSetsForFiles(game, component, componentGamedata, componentDirectory)

    componentInstructions = {
        "name": componentName, 
        "type": component["type"],
        "fileInstructions": fileInstructionSets
    }
    client.dumpInstructions(componentInstructionFilepath, componentInstructions)

    processor.createArtFilesForComponent(game, component, componentArtMetadata, componentBackArtMetadata,  componentGamedata, componentDirectory)
        