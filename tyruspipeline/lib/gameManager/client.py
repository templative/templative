import manager
import uuid
import os
from datetime import datetime

from ..svgmanipulation import artProcessor   

def produceGame(gameRootDirectoryPath, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = manager.loadGame(gameRootDirectoryPath)
    identifier = uuid.uuid1()
    uniqueGameName = "%s %s" % (game["name"], game["versionName"])
    print("Producing %s ..." % uniqueGameName)

    timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    gameFolderName = ("%s_%s_%s_%s" % (game["name"], game["versionName"], game["version"], timestamp)).replace(" ", "")
    gameFolderPath = "%s/%s" % (outputDirectory, gameFolderName)
    print(gameFolderPath)
    os.mkdir(gameFolderPath)

    company = manager.loadCompany(gameRootDirectoryPath)
    companyFilepath = "%s/company.json" % (gameFolderPath)
    manager.dumpInstructions(companyFilepath, company)

    gameFilepath = "%s/game.json" % (gameFolderPath)
    manager.dumpInstructions(gameFilepath, game)

    components = manager.loadGameComponents(gameRootDirectoryPath)
    for component in components["components"]:

        componentName = component["name"].replace(" ", "")
        componentDirectory = "%s/%s" % (gameFolderPath, componentName)
        os.mkdir(componentDirectory)

        componentInstructionFilepath = "%s/%s.json" % (componentDirectory, componentName)
        manager.dumpInstructions(componentInstructionFilepath, component)

        produceGameComponent(gameRootDirectoryPath, game, component, componentDirectory)

    return gameFolderPath

def produceGameComponent(gameRootDirectoryPath, game, component, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    componentName = component["name"]
    
    componentGamedata = manager.loadComponentGamedata(gameRootDirectoryPath, component["gamedataFilename"])
    if not componentGamedata or componentGamedata == {}:
        print("Skipping %s component due to missing game data." % componentName)
        return

    componentArtMetadata = manager.loadArtMetadata(gameRootDirectoryPath, component["artMetadataFilename"])
    if not componentArtMetadata or componentArtMetadata == {}:
        print("Skipping %s component due to missing front art metadata." % componentName)
        return

    componentBackArtMetadata = manager.loadArtMetadata(gameRootDirectoryPath, component["backArtMetadataFilename"])
    if not componentBackArtMetadata or componentBackArtMetadata == {}:
        print("Skipping %s component due to missing back art metadata." % componentName)
        return

    print("Creating art assets for %s component." % (component["name"]))
    artProcessor.createArtFilesForComponent(game, component, componentArtMetadata, componentBackArtMetadata,  componentGamedata, outputDirectory)
        