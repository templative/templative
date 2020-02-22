import uuid
import os
from datetime import datetime

import client as client
from ..svgmanipulation import operations as processor

def produceGame(gameRootDirectoryPath, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = client.loadGame(gameRootDirectoryPath)
    identifier = uuid.uuid1()
    uniqueGameName = "%s %s" % (game["name"], game["versionName"])
    print("Producing %s ..." % uniqueGameName)

    gameFolderPath = createGameFolder(game["name"], game["version"], game["versionName"], outputDirectory)
    print(gameFolderPath)

    copyCompanyFromGameFolderToOutput(gameRootDirectoryPath, gameFolderPath)
    copyGameFromGameFolderToOutput(gameRootDirectoryPath, gameFolderPath)
    
    components = client.loadGameComponents(gameRootDirectoryPath)
    for component in components["components"]:
        produceGameComponent(gameRootDirectoryPath, game, component, gameFolderPath)

    return gameFolderPath

def createGameFolder(name, version, versionName, outputDirectory):
    timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    gameFolderName = ("%s_%s_%s_%s" % (name, version, versionName, timestamp)).replace(" ", "")
    gameFolderPath = "%s/%s" % (outputDirectory, gameFolderName)
    os.mkdir(gameFolderPath)
    return gameFolderPath

def copyCompanyFromGameFolderToOutput(gameRootDirectoryPath, gameFolderPath):
    company = client.loadCompany(gameRootDirectoryPath)
    companyFilepath = "%s/company.json" % (gameFolderPath)
    client.dumpInstructions(companyFilepath, company)

def copyGameFromGameFolderToOutput(gameRootDirectoryPath, gameFolderPath):
    gameFilepath = "%s/game.json" % (gameFolderPath)
    client.dumpInstructions(gameFilepath, {"name": uniqueGameName})

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
    componentInstructions = {
        "name": componentName, 
        "type": component["type"]
    }
    client.dumpInstructions(componentInstructionFilepath, componentInstructions)

    processor.createArtFilesForComponent(game, component, componentArtMetadata, componentBackArtMetadata,  componentGamedata, componentDirectory)
        