import os
import asyncio
from . import defineLoader, componentTemplateCreator, outputWriter, rulesMarkdownProcessor
from datetime import datetime
from templative.componentInfo import COMPONENT_INFO

from . import customComponents

from .models.produceProperties import ProduceProperties
from .models.gamedata import GameData
from .models.composition import ComponentComposition

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

async def printGameComponentDepth(gameRootDirectoryPath, gameCompose, componentCompose):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    depthMillimeters = 0
    for component in componentCompose:
        if str(component["disabled"]) == "True":
            print("Skipping disabled %s component." % (component["name"]))
            continue
        
        if component["type"].startswith("STOCK"):
            print("Skipping stock %s component." % (component["name"]))
            continue
        
        piecesGamedata = await defineLoader.loadPiecesGamedata(gameRootDirectoryPath, gameCompose, component["piecesGamedataFilename"])
        if not piecesGamedata or piecesGamedata == {}:
            print("Skipping %s component due to missing pieces gamedata." % component["name"])
            continue
        
        if not component["type"] in component["type"]:
            print("Missing component info for %s." % component["name"])
            continue

        component = COMPONENT_INFO[component["type"]]
        if not "GameCrafterPackagingDepthMillimeters" in component:
            print("Skipping %s component as we don't have a millimeter measurement for it." % component["name"])
            continue

        depthOfPiece = component["GameCrafterPackagingDepthMillimeters"]
        for piece in piecesGamedata:
            depthMillimeters += int(piece["quantity"]) * depthOfPiece      
    print("%smm" % round(depthMillimeters, 2))

async def printGameComponentQuantities(gameRootDirectoryPath, gameCompose, componentCompose):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    componentQuantities ={"Document": [{ "name":"Rules", "componentQuantity": 1, "pieceQuantity": 1}]}
    for component in componentCompose:
        if str(component["disabled"]) == "True":
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

async def produceGame(gameRootDirectoryPath, componentFilter, isSimple, isPublish):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    gameDataBlob = await defineLoader.loadGame(gameRootDirectoryPath)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    uniqueGameName = ("%s_%s_%s_%s" % (gameDataBlob["name"], gameDataBlob["version"], gameDataBlob["versionName"], timestamp)).replace(" ", "")
    gameDataBlob["name"] = uniqueGameName

    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)

    outputDirectoryPath = await outputWriter.createGameFolder(gameDataBlob["name"], gameCompose["outputDirectory"])
    await outputWriter.updateLastOutputFolder(gameCompose["outputDirectory"], outputDirectoryPath)
    print("Producing %s" % outputDirectoryPath)

    tasks = []
    tasks.append(asyncio.create_task(outputWriter.copyGameFromGameFolderToOutput(gameDataBlob, outputDirectoryPath)))

    studioDataBlob = await defineLoader.loadStudio(gameRootDirectoryPath)
    tasks.append(asyncio.create_task(outputWriter.copyStudioFromGameFolderToOutput(studioDataBlob, outputDirectoryPath)))

    componentsCompose = await defineLoader.loadComponentCompose(gameRootDirectoryPath)

    gameData = GameData(studioDataBlob, gameDataBlob)
    produceProperties = ProduceProperties(gameRootDirectoryPath, outputDirectoryPath, isPublish, isSimple)

    for componentCompose in componentsCompose:
        isProducingOneComponent = componentFilter != None
        isMatchingComponentFilter = isProducingOneComponent and componentCompose["name"] == componentFilter
        if not isMatchingComponentFilter and componentCompose["disabled"]:
            if not isProducingOneComponent:
                print("Skipping disabled %s component." % (componentCompose["name"]))
            continue
        
        isDebugInfo = False if not "isDebugInfo" in componentCompose else componentCompose["isDebugInfo"]
        if isDebugInfo and isPublish:
            print("Skipping debug only %s component as we are publishing." % (componentCompose["name"]))
            continue

        if isProducingOneComponent and not isMatchingComponentFilter:
            continue

        componentComposition = ComponentComposition(gameCompose, componentCompose)

        tasks.append(asyncio.create_task(produceGameComponent(produceProperties, gameData, componentComposition)))

    rules = await defineLoader.loadRules(gameRootDirectoryPath)
    tasks.append(asyncio.create_task(rulesMarkdownProcessor.produceRulebook(rules, outputDirectoryPath)))

    for task in tasks:
        await task

    print("Done producing %s" % outputDirectoryPath)

    return outputDirectoryPath

async def produceGameComponent(produceProperties: ProduceProperties, gamedata:GameData, componentComposition:ComponentComposition) -> None:

    componentType = componentComposition.componentCompose["type"]
    componentTypeTokens = componentType.split("_")
    isStockComponent = componentTypeTokens[0].upper() == "STOCK" 
    
    if isStockComponent:
        await produceStockComponent(componentComposition.componentCompose, produceProperties.outputDirectoryPath)
        return
    
    await customComponents.produceCustomComponent(produceProperties, gamedata, componentComposition)
        
async def produceStockComponent(componentCompose, outputDirectory):
    componentName = componentCompose["name"]

    print("Outputing stock parts for %s component." % (componentName))

    componentDirectory = await outputWriter.createComponentFolder(componentName, outputDirectory)

    stockPartInstructions = {
        "name": componentCompose["name"],
        "quantity": componentCompose["quantity"],
        "type": componentCompose["type"]
    }

    componentInstructionFilepath = os.path.join(componentDirectory, "component.json")
    await outputWriter.dumpInstructions(componentInstructionFilepath, stockPartInstructions)

