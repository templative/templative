import gameLoader
import uuid
import os
from datetime import datetime

from ..svgmanipulation import artProcessor   

def produceGame(gameRootDirectoryPath, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = gameLoader.loadGame(gameRootDirectoryPath)
    identifier = uuid.uuid1()
    uniqueGameName = "%s %s" % (game["name"], game["versionName"])
    print("Producing %s ..." % uniqueGameName)

    timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    gameFolderName = ("%s_%s_%s_%s" % (game["name"], game["versionName"], game["version"], timestamp)).replace(" ", "")
    gameFolderPath = "%s/%s" % (outputDirectory, gameFolderName)
    print(gameFolderPath)
    os.mkdir(gameFolderPath)

    components = gameLoader.loadGameComponents(gameRootDirectoryPath)
    for component in components["components"]:
        produceGameComponent(gameRootDirectoryPath, game, component, gameFolderPath)

    return gameFolderPath

def produceGameComponent(gameRootDirectoryPath, game, component, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    componentName = component["name"]
    
    componentGamedata = gameLoader.loadComponentGamedata(gameRootDirectoryPath, component["gamedataFilename"])
    if not componentGamedata or componentGamedata == {}:
        print("Skipping %s component due to missing game data." % componentName)
        return

    componentArtMetadata = gameLoader.loadArtMetadata(gameRootDirectoryPath, component["artMetadataFilename"])
    if not componentArtMetadata or componentArtMetadata == {}:
        print("Skipping %s component due to missing front art metadata." % componentName)
        return

    componentBackArtMetadata = gameLoader.loadArtMetadata(gameRootDirectoryPath, component["backArtMetadataFilename"])
    if not componentBackArtMetadata or componentBackArtMetadata == {}:
        print("Skipping %s component due to missing back art metadata." % componentName)
        return

    artProcessor.createArtFilesForComponent(game, component, componentArtMetadata, componentBackArtMetadata,  componentGamedata, outputDirectory)

    