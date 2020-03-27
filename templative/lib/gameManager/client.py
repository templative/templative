import os
import json
from templative.lib.svgscissors import operations as processor
from templative.lib.gameManager import fileLoader
from templative.lib.gameManager import gameWriter

from md2pdf.core import md2pdf

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

    componentArtdata = fileLoader.loadArtdata(gameRootDirectoryPath, gameCompose, componentCompose["artdataFilename"])
    if not componentArtdata or componentArtdata == {}:
        print("Skipping %s component due to missing front art metadata." % componentName)
        return

    componentBackArtdata = fileLoader.loadArtdata(gameRootDirectoryPath, gameCompose, componentCompose["backArtdataFilename"])
    if not componentBackArtdata or componentBackArtdata == {}:
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

    processor.createArtFilesForComponent(game, gameCompose, componentCompose, componentArtdata, componentBackArtdata, componentGamedata, piecesGamedata, componentDirectory)

def produceRulebook(rules, gameFolderPath):
    outputFilepath = os.path.join(gameFolderPath, "rules.pdf")
    
    # pdf_file_path: output PDF file path
    # md_content: input markdown raw string content
    # md_file_path: input markdown file path
    # css_file_path: input styles path (CSS)
    # base_url: absolute base path for markdown linked content (as images)
    md2pdf(outputFilepath, md_content=rules)