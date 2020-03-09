import os
import json
from ..svgscissors import operations as processor
import fileLoader
import gameWriter

def produceGameComponent(gameRootDirectoryPath, game, gameCompose, componentCompose, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    componentName = componentCompose["name"]

    componentGamedata = fileLoader.loadComponentGamedata(gameRootDirectoryPath, gameCompose, componentCompose["componentGamedataFilename"])
    if not componentGamedata or componentGamedata == {}:
        print("Skipping %s component due to missing component gamedata." % componentName)
        return

    piecesGamedata = fileLoader.loadPiecesGamedata(gameRootDirectoryPath, gameCompose, componentCompose["piecesGamedataFilename"])
    if not piecesGamedata or piecesGamedata == {}:
        print("Skipping %s component due to missing pieces gamedata." % componentName)
        return

    componentArtMetadata = fileLoader.loadArtMetadata(gameRootDirectoryPath, gameCompose, componentCompose["artMetadataFilename"])
    if not componentArtMetadata or componentArtMetadata == {}:
        print("Skipping %s component due to missing front art metadata." % componentName)
        return

    componentBackArtMetadata = fileLoader.loadArtMetadata(gameRootDirectoryPath, gameCompose, componentCompose["backArtMetadataFilename"])
    if not componentBackArtMetadata or componentBackArtMetadata == {}:
        print("Skipping %s component due to missing back art metadata." % componentName)
        return

    print("Creating art assets for %s component." % (componentName))

    componentDirectory = gameWriter.createComponentFolder(componentName, outputDirectory)

    componentInstructionFilepath = os.path.join(componentDirectory, "component.json")

    fileInstructionSets = processor.getInstructionSetsForFiles(game, componentCompose, piecesGamedata, componentDirectory)
    backInstructionSet = processor.getBackInstructionSet(componentCompose, componentDirectory)
    componentInstructions = {
        "name": componentName, 
        "type": componentCompose["type"],
        "quantity": componentCompose["quantity"],
        "fileInstructions": fileInstructionSets,
        "backInstructions": backInstructionSet
    }
    gameWriter.dumpInstructions(componentInstructionFilepath, componentInstructions)

    processor.createArtFilesForComponent(game, gameCompose, componentCompose, componentArtMetadata, componentBackArtMetadata, componentGamedata, piecesGamedata, componentDirectory)