import uuid
import os
from datetime import datetime

import client as client
from ..svgmanipulation import operations as processor

def produceGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = client.loadGame(gameRootDirectoryPath)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    uniqueGameName = ("%s_%s_%s_%s" % (game["name"], game["version"], game["versionName"], timestamp)).replace(" ", "")
    game["name"] = uniqueGameName

    gameCompose = client.loadGameCompose(gameRootDirectoryPath)

    gameFolderPath = createGameFolder(game["name"], gameCompose["outputDirectory"])
    print("Producing %s" % gameFolderPath)

    copyCompanyFromGameFolderToOutput(gameRootDirectoryPath, gameFolderPath)
    copyGameFromGameFolderToOutput(game, gameFolderPath)
    
    components = client.loadGameComponents(gameRootDirectoryPath)
    for component in components["components"]:
        produceGameComponent(gameRootDirectoryPath, game, gameCompose, component, gameFolderPath)

    print("Done producing %s" % gameFolderPath)

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

def produceGameComponent(gameRootDirectoryPath, game, gameCompose, component, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    componentDisplayName = component["displayName"]

    componentGamedata = client.loadComponentGamedata(gameRootDirectoryPath, gameCompose, component["gamedataFilename"])
    if not componentGamedata or componentGamedata == {}:
        print("Skipping %s component due to missing game data." % componentDisplayName)
        return

    componentArtMetadata = client.loadArtMetadata(gameRootDirectoryPath, gameCompose, component["artMetadataFilename"])
    if not componentArtMetadata or componentArtMetadata == {}:
        print("Skipping %s component due to missing front art metadata." % componentDisplayName)
        return

    componentBackArtMetadata = client.loadArtMetadata(gameRootDirectoryPath, gameCompose, component["backArtMetadataFilename"])
    if not componentBackArtMetadata or componentBackArtMetadata == {}:
        print("Skipping %s component due to missing back art metadata." % componentDisplayName)
        return

    print("Creating art assets for %s component." % (componentDisplayName))

    componentName = component["name"]
    componentDirectory = "%s/%s" % (outputDirectory, componentName)
    os.mkdir(componentDirectory)

    componentInstructionFilepath = "%s/component.json" % (componentDirectory)

    fileInstructionSets = processor.getInstructionSetsForFiles(game, component, componentGamedata, componentDirectory)
    backInstructionSet = processor.getBackInstructionSet(component, componentDirectory)
    componentInstructions = {
        "name": componentName, 
        "type": component["type"],
        "fileInstructions": fileInstructionSets,
        "backInstructions": backInstructionSet
    }
    client.dumpInstructions(componentInstructionFilepath, componentInstructions)

    processor.createArtFilesForComponent(game, gameCompose, component, componentArtMetadata, componentBackArtMetadata,  componentGamedata, componentDirectory)
        