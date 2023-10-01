import os
import asyncio

from . import outputWriter, rulesMarkdownProcessor
from templative.manage import defineLoader
from datetime import datetime

from templative.produce import customComponents

from templative.manage.models.produceProperties import ProduceProperties
from templative.manage.models.gamedata import GameData
from templative.manage.models.composition import ComponentComposition

async def produceGame(gameRootDirectoryPath, componentFilter, isSimple, isPublish, targetLanguage):
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
    produceProperties = ProduceProperties(gameRootDirectoryPath, outputDirectoryPath, isPublish, isSimple, targetLanguage)

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