import os
import asyncio
from . import defineLoader, componentTemplateCreator, outputWriter, rulesMarkdownProcessor, svgscissors
from datetime import datetime

async def convertRulesMdToHtml(gameRootDirectoryPath):
    rules = await defineLoader.loadRules(gameRootDirectoryPath)
    await rulesMarkdownProcessor.convertRulesMdToHtml(rules, gameRootDirectoryPath)

async def convertRulesMdToSpans(gameRootDirectoryPath):
    rules = await defineLoader.loadRules(gameRootDirectoryPath)
    await rulesMarkdownProcessor.convertRulesMdToSpans(rules, gameRootDirectoryPath)

async def createComponent(name, type):
    gameRootDirectoryPath = "."
    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)
    componentComposeData = await defineLoader.loadComponentCompose(gameRootDirectoryPath)
    await componentTemplateCreator.addToComponentCompose(name, type, gameRootDirectoryPath, componentComposeData)
    await componentTemplateCreator.createPiecesCsv(gameCompose["piecesGamedataDirectory"], name)
    await componentTemplateCreator.createComponentJson(gameCompose["componentGamedataDirectory"], name)
    await componentTemplateCreator.createArtData(gameCompose["artdataDirectory"], name)
    await componentTemplateCreator.createComponentArtFiles(gameCompose["artTemplatesDirectory"], name, type)

async def createStockComponent(name, stockPartId):
    gameRootDirectoryPath = "."
    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)
    componentComposeData = await defineLoader.loadComponentCompose(gameRootDirectoryPath)
    await componentTemplateCreator.addStockComponentToComponentCompose(name, stockPartId, gameRootDirectoryPath, componentComposeData)
    await componentTemplateCreator.createComponentJson(gameCompose["componentGamedataDirectory"], name)

async def listComponents(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = await defineLoader.loadGame(gameRootDirectoryPath)
    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)
    studioCompose = await defineLoader.loadStudio(gameRootDirectoryPath)
    componentCompose = await defineLoader.loadComponentCompose(gameRootDirectoryPath)

    print("%s by %s" % (game["displayName"], studioCompose["displayName"]))
    await printGameComponentQuantities(gameRootDirectoryPath, gameCompose, componentCompose)

async def calculateComponentsDepth(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = await defineLoader.loadGame(gameRootDirectoryPath)
    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)
    studioCompose = await defineLoader.loadStudio(gameRootDirectoryPath)
    componentCompose = await defineLoader.loadComponentCompose(gameRootDirectoryPath)

    print("%s by %s" % (game["displayName"], studioCompose["displayName"]))
    await printGameComponentDepth(gameRootDirectoryPath, gameCompose, componentCompose)

componentDepthPerPieceMillimeters = {
    "MintTinFolio": 1,
    "MintTinAccordion8": 2,
    "MintTinAccordion6": 2,
    "MintTinAccordion4": 1,
    "MintTinDeck": 0.3,
    "MicroDeck": 0.15,
    "MiniDeck": 0.3,
}

async def printGameComponentDepth(gameRootDirectoryPath, gameCompose, componentCompose):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    depthMillimeters = 0
    for component in componentCompose:
        
        if component["disabled"] == "True":
            print("Skipping disabled %s component." % (component["name"]))
            continue
        
        if component["type"].startswith("STOCK"):
            print("Skipping stock %s component." % (component["name"]))
            continue
        
        piecesGamedata = await defineLoader.loadPiecesGamedata(gameRootDirectoryPath, gameCompose, component["piecesGamedataFilename"])
        if not piecesGamedata or piecesGamedata == {}:
            print("Skipping %s component due to missing pieces gamedata." % component["name"])
            continue
        if not component["type"] in componentDepthPerPieceMillimeters:
            print("Skipping %s component as we don't have a millimeter measurement for it." % component["name"])
            continue
        depthOfPiece = componentDepthPerPieceMillimeters[component["type"]]
        for piece in piecesGamedata:
            depthMillimeters += int(piece["quantity"]) * depthOfPiece      
    print("%smm" % round(depthMillimeters, 2))

async def printGameComponentQuantities(gameRootDirectoryPath, gameCompose, componentCompose):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    componentQuantities ={"Document": [{ "name":"Rules", "componentQuantity": 1, "pieceQuantity": 1}]}
    for component in componentCompose:
        if component["disabled"] == "True":
            print("Skipping disabled %s component." % (component["name"]))
            continue
        
        if component["type"].startswith("STOCK"):
            await addStockComponentQuantities(componentQuantities, component)
            continue
        
        piecesGamedata = await defineLoader.loadPiecesGamedata(gameRootDirectoryPath, gameCompose, component["piecesGamedataFilename"])
        if not piecesGamedata or piecesGamedata == {}:
            print("Skipping %s component due to missing pieces gamedata." % component["name"])
            continue
        await addComponentQuantities(componentQuantities, component, piecesGamedata)
        
    message = ""
    for componentType in componentQuantities:
        componentExplanations = ""
        componentQuantity = 0
        for explanation in componentQuantities[componentType]:
            quantity = explanation["componentQuantity"] * explanation["pieceQuantity"]
            componentQuantity += quantity
            componentExplanations = "%s\n    %sx %s" % (componentExplanations, quantity, explanation["name"])
        message = "%s\n%sx %s Pieces: %s" % (message, componentQuantity, componentType, componentExplanations)
        
    print(message)


async def addStockComponentQuantities(componentQuantities, component):
    if not component["type"] in componentQuantities:
        componentQuantities[component["type"]] = []

    componentQuantities[component["type"]].append({
        "name": component["name"], "componentQuantity": component["quantity"], "pieceQuantity": 1
    })

async def addComponentQuantities(componentQuantities, component, piecesGamedata):
    if not component["type"] in componentQuantities:
        componentQuantities[component["type"]] = []

    quantity = 0
    for piece in piecesGamedata:
        quantity += int(piece["quantity"])
    
    componentQuantities[component["type"]].append({
        "name":component["name"], "componentQuantity": component["quantity"], "pieceQuantity": quantity
    })

async def produceGame(gameRootDirectoryPath, componentFilter, isSimple):
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

    studioCompose = await defineLoader.loadStudio(gameRootDirectoryPath)
    tasks.append(asyncio.create_task(outputWriter.copyStudioFromGameFolderToOutput(studioCompose, gameFolderPath)))

    componentCompose = await defineLoader.loadComponentCompose(gameRootDirectoryPath)

    for component in componentCompose:
        isProducingOneComponent = componentFilter != None
        isMatchingComponentFilter = isProducingOneComponent and component["name"] == componentFilter
        if not isMatchingComponentFilter and component["disabled"]:
            print("Skipping disabled %s component." % (component["name"]))
            continue

        if isProducingOneComponent and not isMatchingComponentFilter:
            continue

        tasks.append(asyncio.create_task(produceGameComponent(gameRootDirectoryPath, game, studioCompose, gameCompose, component, gameFolderPath, isSimple)))

    rules = await defineLoader.loadRules(gameRootDirectoryPath)
    tasks.append(asyncio.create_task(rulesMarkdownProcessor.produceRulebook(rules, gameFolderPath)))

    for task in tasks:
        await task

    print("Done producing %s" % gameFolderPath)

    return gameFolderPath

async def produceGameComponent(gameRootDirectoryPath, game, studioCompose, gameCompose, componentCompose, outputDirectory, isSimple):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    componentType = componentCompose["type"]
    componentTypeTokens = componentType.split("_")
    isStockComponent = componentTypeTokens[0].upper() == "STOCK" 
    
    if isStockComponent:
        await produceStockComponent(componentCompose, outputDirectory)
        return
    
    await produceCustomComponent(gameRootDirectoryPath, game, studioCompose, gameCompose, componentCompose, outputDirectory, isSimple)
        
async def produceStockComponent(componentCompose, outputDirectory):
    componentName = componentCompose["name"]

    print("Outputing stock parts for %s component." % (componentName))

    componentDirectory = await outputWriter.createComponentFolder(componentName, outputDirectory)

    stockPartInstructions = {
        "name": componentCompose["name"],
        "quantity": componentCompose["quantity"],
        "type": componentCompose["type"],
    }

    componentInstructionFilepath = os.path.join(componentDirectory, "component.json")
    await outputWriter.dumpInstructions(componentInstructionFilepath, stockPartInstructions)

async def produceCustomComponent(gameRootDirectoryPath, game, studioCompose, gameCompose, componentCompose, outputDirectory, isSimple):
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

    await svgscissors.createArtFilesForComponent(game, studioCompose, gameCompose, componentCompose, componentArtdata, componentBackArtdata, componentGamedata, piecesGamedata, componentDirectory, isSimple)

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
