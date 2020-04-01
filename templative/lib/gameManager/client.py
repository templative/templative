import os
import asyncio
import json
from templative.lib.svgscissors import operations as processor
from templative.lib.gameManager import fileLoader
from templative.lib.gameManager import gameWriter

from templative.lib.gameManager.md2pdf import md2pdf

async def produceGameComponent(gameRootDirectoryPath, game, gameCompose, componentCompose, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    componentName = componentCompose["name"]

    componentGamedata = await fileLoader.loadComponentGamedata(gameRootDirectoryPath, gameCompose, componentCompose["componentGamedataFilename"])
    if not componentGamedata or componentGamedata == {}:
        print("Skipping %s component due to missing component gamedata." % componentName)
        return

    piecesGamedata = await fileLoader.loadPiecesGamedata(gameRootDirectoryPath, gameCompose, componentCompose["piecesGamedataFilename"])
    if not piecesGamedata or piecesGamedata == {}:
        print("Skipping %s component due to missing pieces gamedata." % componentName)
        return

    componentArtdata = await fileLoader.loadArtdata(gameRootDirectoryPath, gameCompose, componentCompose["artdataFilename"])
    if not componentArtdata or componentArtdata == {}:
        print("Skipping %s component due to missing front art metadata." % componentName)
        return

    componentBackArtdata = await fileLoader.loadArtdata(gameRootDirectoryPath, gameCompose, componentCompose["backArtdataFilename"])
    if not componentBackArtdata or componentBackArtdata == {}:
        print("Skipping %s component due to missing back art metadata." % componentName)
        return

    print("Creating art assets for %s component." % (componentName))

    componentDirectory = await gameWriter.createComponentFolder(componentName, outputDirectory)

    componentInstructionFilepath = os.path.join(componentDirectory, "component.json")

    frontInstructionSets = await processor.getInstructionSetsForFiles(game, componentCompose, piecesGamedata, componentDirectory)
    backInstructionSet = await processor.getBackInstructionSet(componentCompose, componentDirectory)
    componentInstructions = {
        "name": componentName, 
        "type": componentCompose["type"],
        "quantity": componentCompose["quantity"],
        "frontInstructions": frontInstructionSets,
        "backInstructions": backInstructionSet
    }
    await gameWriter.dumpInstructions(componentInstructionFilepath, componentInstructions)

    await processor.createArtFilesForComponent(game, gameCompose, componentCompose, componentArtdata, componentBackArtdata, componentGamedata, piecesGamedata, componentDirectory)

async def produceRulebook(rules, gameFolderPath):
    outputFilepath = os.path.join(gameFolderPath, "rules.pdf")
    cssFilepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pdfStyles.css")
    md2pdf(outputFilepath, md_content=rules, css_file_path=cssFilepath)