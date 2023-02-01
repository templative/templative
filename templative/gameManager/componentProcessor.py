import os
import asyncio
from . import defineLoader, outputWriter, rulesMarkdownProcessor, svgscissors
from datetime import datetime

async def produceGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = await defineLoader.loadGame(gameRootDirectoryPath)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    uniqueGameName = ("%s_%s_%s_%s" % (game["name"], game["version"], game["versionName"], timestamp)).replace(" ", "")
    game["name"] = uniqueGameName

    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)

    gameFolderPath = await outputWriter.createGameFolder(game["name"], gameCompose["outputDirectory"])
    await outputWriter.updateLastOutputFolder(gameCompose["outputDirectory"], gameFolderPath)
    print("Producing %s" % gameFolderPath)

    tasks = []
    tasks.append(asyncio.create_task(outputWriter.copyGameFromGameFolderToOutput(game, gameFolderPath)))

    company = await defineLoader.loadCompany(gameRootDirectoryPath)
    tasks.append(asyncio.create_task(outputWriter.copyCompanyFromGameFolderToOutput(company, gameFolderPath)))

    componentCompose = await defineLoader.loadComponentCompose(gameRootDirectoryPath)

    for component in componentCompose["components"]:
        if component["disabled"]:
            print("Skipping disabled %s component." % (component["name"]))
            continue
        tasks.append(asyncio.create_task(produceGameComponent(gameRootDirectoryPath, game, gameCompose, component, gameFolderPath)))

    rules = await defineLoader.loadRules(gameRootDirectoryPath)
    tasks.append(asyncio.create_task(rulesMarkdownProcessor.produceRulebook(rules, gameFolderPath)))

    for task in tasks:
        await task

    print("Done producing %s" % gameFolderPath)

    return gameFolderPath

async def produceGameComponent(gameRootDirectoryPath, game, gameCompose, componentCompose, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    componentName = componentCompose["name"]

    componentGamedata = await defineLoader.loadComponentGamedata(gameRootDirectoryPath, gameCompose, componentCompose["componentGamedataFilename"])
    if not componentGamedata or componentGamedata == {}:
        print("Skipping %s component due to missing component gamedata." % componentName)
        return

    piecesGamedata = await defineLoader.loadPiecesGamedata(gameRootDirectoryPath, gameCompose, componentCompose["piecesGamedataFilename"])
    if not piecesGamedata or piecesGamedata == {}:
        print("Skipping %s component due to missing pieces gamedata." % componentName)
        return

    componentArtdata = await defineLoader.loadArtdata(gameRootDirectoryPath, gameCompose, componentCompose["artdataFilename"])
    if not componentArtdata or componentArtdata == {}:
        print("Skipping %s component due to missing front art metadata." % componentName)
        return

    componentBackArtdata = await defineLoader.loadArtdata(gameRootDirectoryPath, gameCompose, componentCompose["backArtdataFilename"])
    if not componentBackArtdata or componentBackArtdata == {}:
        print("Skipping %s component due to missing back art metadata." % componentName)
        return

    print("Creating art assets for %s component." % (componentName))

    componentDirectory = await outputWriter.createComponentFolder(componentName, outputDirectory)

    componentInstructionFilepath = os.path.join(componentDirectory, "component.json")

    frontInstructionSets = await getInstructionSetsForFiles(game, componentCompose, piecesGamedata, componentDirectory)
    backInstructionSet = await getBackInstructionSet(componentCompose, componentDirectory)
    componentInstructions = {
        "name": componentName,
        "type": componentCompose["type"],
        "quantity": componentCompose["quantity"],
        "frontInstructions": frontInstructionSets,
        "backInstructions": backInstructionSet
    }
    await outputWriter.dumpInstructions(componentInstructionFilepath, componentInstructions)

    await svgscissors.createArtFilesForComponent(game, gameCompose, componentCompose, componentArtdata, componentBackArtdata, componentGamedata, piecesGamedata, componentDirectory)

async def getInstructionSetsForFiles(game, componentCompose, componentGamedata, componentFilepath):
    if game == None:
        print("game cannot be None.")
        return

    if componentCompose == None:
        print("component cannot be None.")
        return

    if componentGamedata == None:
        print("componentGamedata cannot be None.")
        return

    instructionSets = []
    for pieceGamedata in componentGamedata:
        filename = "%s-%s.jpg" % (componentCompose["name"], pieceGamedata["name"])
        artFilepath = os.path.join(componentFilepath, filename)
        instructionSets.append({"name": pieceGamedata["name"], "filepath": artFilepath, "quantity": pieceGamedata["quantity"]})

    return instructionSets

async def getBackInstructionSet(componentCompose, componentFilepath):
    filename = "%s-back.jpg" % componentCompose["name"]
    backFilepath = os.path.join(componentFilepath, filename)
    return {"name": filename, "filepath": backFilepath}
