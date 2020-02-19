import gameLoader
import uuid
import os

from ..svgmanipulation import artProcessor   

def produceGame(gameRootDirectoryPath, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = gameLoader.loadGame(gameRootDirectoryPath)
    identifier = uuid.uuid1()
    uniqueGameName = "%s %s %s %s" % (game["name"], game["versionName"], game["version"], identifier)
    print("Producing %s ..." % uniqueGameName)

    gameFolderName = "%s_%s_%s_%s" % (game["name"], game["versionName"], game["version"], identifier)
    gameFolderPath = "%s/%s" % (outputDirectory, gameFolderName)
    os.mkdir(gameFolderPath)

    components = gameLoader.loadGameComponents(gameRootDirectoryPath)
    for component in components["components"]:
        produceGameComponent(gameRootDirectoryPath, component, gameFolderPath)

def produceGameComponent(gameRootDirectoryPath, component, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    componentName = component["name"]
    
    componentGamedata = gameLoader.loadComponentGamedata(gameRootDirectoryPath, component["gamedataFilename"])
    if not componentGamedata or componentGamedata == {}:
        print("Skipping %s component due to missing game data." % componentName)
        return

    componentArtMetadata = gameLoader.loadArtMetadata(gameRootDirectoryPath, component["artMetadataFilename"])
    if not componentArtMetadata or componentArtMetadata == {}:
        print("Skipping %s component due to missing art metadata." % componentName)
        return

    artProcessor.createArtFilesForComponent(component, componentArtMetadata, componentGamedata, outputDirectory)

    