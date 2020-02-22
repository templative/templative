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

    timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    gameFolderName = ("%s_%s_%s_%s" % (game["name"], game["version"], game["versionName"], timestamp)).replace(" ", "")
    gameFolderPath = "%s/%s" % (outputDirectory, gameFolderName)
    print(gameFolderPath)
    os.mkdir(gameFolderPath)

    company = client.loadCompany(gameRootDirectoryPath)
    companyFilepath = "%s/company.json" % (gameFolderPath)
    client.dumpInstructions(companyFilepath, company)

    gameFilepath = "%s/game.json" % (gameFolderPath)
    client.dumpInstructions(gameFilepath, game)

    components = client.loadGameComponents(gameRootDirectoryPath)
    for component in components["components"]:

        componentName = component["name"].replace(" ", "")
        componentDirectory = "%s/%s" % (gameFolderPath, componentName)
        os.mkdir(componentDirectory)

        componentInstructionFilepath = "%s/%s.json" % (componentDirectory, componentName)
        client.dumpInstructions(componentInstructionFilepath, component)

        produceGameComponent(gameRootDirectoryPath, game, component, componentDirectory)

    return gameFolderPath

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
    processor.createArtFilesForComponent(game, component, componentArtMetadata, componentBackArtMetadata,  componentGamedata, outputDirectory)
        