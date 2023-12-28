from os import path, mkdir, walk
from json import dump, load
from shutil import copyfile
from templative.lib.manage import instructionsLoader
from . import templateMaker
from templative.lib.distribute.playground.playgroundTemplates import stockModel
from .gameStateMaker import createGameStateVts
from PIL import Image
from hashlib import md5
import math
from aiofile import AIOFile
import asyncclick as click
from templative.lib.componentInfo import COMPONENT_INFO
from templative.lib.stockComponentInfo import STOCK_COMPONENT_INFO

async def lookForPlaygroundFile():
    playgroundFileLocation = "./.playground"
    if not path.exists(playgroundFileLocation):
        return None
    
    async with AIOFile(playgroundFileLocation, mode="r") as playground:
        return await playground.read()
    
async def writePlaygroundFile(outputPath):
    playgroundFileLocation = path.join("./", ".playground")
    async with AIOFile(playgroundFileLocation, mode="w") as playground:
        await playground.write(outputPath)

async def getPlaygroundDirectory(inputedPlaygroundDirectory):
    if inputedPlaygroundDirectory != None:
        return inputedPlaygroundDirectory
    
    return await lookForPlaygroundFile()  

async def convertToTabletopPlayground(producedDirectoryPath, playgroundPackagesDirectory):

    game = await instructionsLoader.loadGameInstructions(producedDirectoryPath)
    studio = await instructionsLoader.loadStudioInstructions(producedDirectoryPath)

    print("Convert %s into a Tabletop Playground package for %s." % (game["displayName"], studio["displayName"]))

    packageDirectoryPath = await createPackageDirectories(game["name"], playgroundPackagesDirectory)
    packageGuid = await createManifest(game["name"], packageDirectoryPath)
    templates = await copyComponentsToPackage(producedDirectoryPath, packageDirectoryPath)

    print("!!! Using default player count 2.")
    defaultPlayerCount = 2
    gameStateJson = await createGameStateVts(game["name"], packageGuid, templates, defaultPlayerCount, packageDirectoryPath)

async def createPackageDirectories(gameName, packagesDirectoryPath):
    packageDirectoryPath = path.join(packagesDirectoryPath, gameName)
    if not path.exists(packageDirectoryPath):
        mkdir(packageDirectoryPath)

    subDirectoryNames = [
        "Fonts", "Models", "Scripts", "Sounds", "States", "Templates", "Textures", "Thumbnails"
    ]

    for subDirectoryName in subDirectoryNames:
        subDirectoryPath = path.join(packageDirectoryPath, subDirectoryName)
        if path.exists(subDirectoryPath):
            continue
        mkdir(subDirectoryPath)

    return packageDirectoryPath

async def copyComponentsToPackage(producedDirectoryPath, packageDirectoryPath):
    templates = []
    for directoryPath in next(walk(producedDirectoryPath))[1]:
        componentDirectoryPath = "%s/%s" % (producedDirectoryPath, directoryPath)
        templateJson = await copyComponentToPackage(componentDirectoryPath, packageDirectoryPath)
        if templateJson == None:
            continue
        templates.append(templateJson)
    return templates

async def copyComponentToPackage(componentDirectoryPath, packageDirectoryPath):
    componentInstructions = None
    componentInstructionsFilepath = path.join(componentDirectoryPath, "component.json")
    with open(componentInstructionsFilepath, "r") as componentInstructionsFile:
        componentInstructions = load(componentInstructionsFile)
    
    supportedInstructionTypes = {
        "DECK": createDeck,
        "BOARD": createBoard
    }

    componentTypeTokens = componentInstructions["type"].split("_")
    isStockComponent = componentTypeTokens[0].upper() == "STOCK" 
    if isStockComponent:
        if not componentTypeTokens[1] in STOCK_COMPONENT_INFO:
            print("Missing stock info for %s." % componentTypeTokens[1])
            return None
        stockComponentInfo = STOCK_COMPONENT_INFO[componentTypeTokens[1]]
        if not "PlaygroundModelFile" in stockComponentInfo:
            print("Skipping %s as it doesn't have a PlaygroundModelFile." % componentTypeTokens[1])
            return None
        return await createStock(packageDirectoryPath, componentInstructions, stockComponentInfo)

    if not componentInstructions["type"] in COMPONENT_INFO:
        print("Missing component info for %s." % componentInstructions["type"])
        return None
    component = COMPONENT_INFO[componentInstructions["type"]]

    if not "PlaygroundCreationTask" in component:
        print("Skipping %s that has no PlaygroundCreationTask." % componentInstructions["type"])
        return None
    playgroundTask = component["PlaygroundCreationTask"]

    if not playgroundTask in supportedInstructionTypes:
        print("Skipping unsupported %s." % playgroundTask)
        return None
    instruction = supportedInstructionTypes[playgroundTask]

    return await instruction(packageDirectoryPath, componentInstructions)
    
async def createBoard(packageDirectoryPath, componentInstructions):
    textureDirectory = path.join(packageDirectoryPath, "Textures")
    await copyFrontImageToTextures(componentInstructions["name"], componentInstructions["frontInstructions"][0], textureDirectory)
    await copyBackImageToTextures(componentInstructions["name"], componentInstructions["backInstructions"], textureDirectory)

    componentGuid = md5(componentInstructions["name"].encode()).hexdigest()
    templateDirectory = path.join(packageDirectoryPath, "Templates")
    return await createBoardTemplateFile(templateDirectory, componentGuid, componentInstructions["name"], componentInstructions["type"])

async def createDeck(packageDirectoryPath, componentInstructions):
    textureDirectory = path.join(packageDirectoryPath, "Textures")

    totalCount, cardColumnCount, cardRowCount = await createCompositeImageInTextures(componentInstructions["name"], componentInstructions["type"], componentInstructions["frontInstructions"], textureDirectory)
    await copyBackImageToTextures(componentInstructions["name"], componentInstructions["backInstructions"], textureDirectory)
    componentGuid = md5(componentInstructions["name"].encode()).hexdigest()
    templateDirectory = path.join(packageDirectoryPath, "Templates")
    return await createCardTemplateFile(templateDirectory, componentGuid, componentInstructions["name"], componentInstructions["type"], totalCount, cardColumnCount, cardRowCount)

async def createStock(packageDirectoryPath, componentInstructions, stockPartInfo):
    guid = md5(componentInstructions["name"].encode()).hexdigest()

    normalMap = stockPartInfo["PlaygroundNormalMap"] if "PlaygroundNormalMap" in stockPartInfo else ""
    extraMap = stockPartInfo["PlaygroundExtraMap"] if "PlaygroundExtraMap" in stockPartInfo else ""
    stockTemplateData = stockModel.createStockModel(componentInstructions["name"], guid, stockPartInfo["PlaygroundModelFile"], stockPartInfo["PlaygroundColor"], normalMap, extraMap)

    if "PlaygroundDieFaces" in stockPartInfo:
        stockTemplateData["Faces"] = stockPartInfo["PlaygroundDieFaces"]

    templateDirectory = path.join(packageDirectoryPath, "Templates")
    templateFilepath = path.join(templateDirectory, "%s.json" % guid)

    with open(templateFilepath, "w") as templateFile:
        dump(stockTemplateData, templateFile, indent=2)
    
    return stockTemplateData

async def createCompositeImageInTextures(componentName, componentType, frontInstructions, textureDirectoryFilepath):

    totalCount = 0
    for instruction in frontInstructions:
        totalCount += int(instruction["quantity"])

    columns = math.floor(math.sqrt(totalCount))
    rows = columns
    while columns * rows < totalCount:
        rows += 1

    if not componentType in COMPONENT_INFO:
        print("Missing component info for %s." % componentType)
        return None
    component = COMPONENT_INFO[componentType]

    if not "DimensionsPixels" in component:
        print("Skipping %s that has no DimensionsPixels." % componentType)
        return None
    pixelDimensions = COMPONENT_INFO[componentType]["DimensionsPixels"]

    tiledImage = Image.new('RGB',(pixelDimensions[0]*columns, pixelDimensions[1]*rows))
    
    xIndex = 0
    yIndex = 0
    for instruction in frontInstructions:
        image = Image.open(instruction["filepath"])
        for _ in range(int(instruction["quantity"])):
            tiledImage.paste(image,(xIndex*pixelDimensions[0],yIndex*pixelDimensions[1]))
            xIndex += 1
            if xIndex == columns:
                xIndex = 0
                yIndex +=1

    frontImageName = "%s-front.jpeg" % componentName
    frontImageFilepath = path.join(textureDirectoryFilepath, frontImageName)
    tiledImage.save(frontImageFilepath,"JPEG")
    return totalCount, columns, rows

async def copyFrontImageToTextures(componentName, frontInstructions, textureDirectoryFilepath):
    frontImageName = "%s-front.jpeg" % componentName
    frontImageFilepath = path.join(textureDirectoryFilepath, frontImageName)
    copyfile(frontInstructions["filepath"], frontImageFilepath)

async def copyBackImageToTextures(componentName, backInstructions, textureDirectoryFilepath):
    backImageName = "%s-back.jpeg" % componentName
    backImageFilepath = path.join(textureDirectoryFilepath, backImageName)
    copyfile(backInstructions["filepath"], backImageFilepath)

async def createBoardTemplateFile(templateDirectoryPath, guid, name, componentType):
    frontTextureName = "%s-front.jpeg" % name
    backTextureName = "%s-back.jpeg" % name
    cardTemplateData = templateMaker.createBoardTemplate(guid, name, componentType, frontTextureName, backTextureName)
    templateFilepath = path.join(templateDirectoryPath, "%s.json" % guid)
    with open(templateFilepath, "w") as templateFile:
        dump(cardTemplateData, templateFile, indent=2)
    return cardTemplateData

async def createCardTemplateFile(templateDirectoryPath, guid, name, componentType, totalCount, cardColumnCount, cardRowCount):
    frontTextureName = "%s-front.jpeg" % name
    backTextureName = "%s-back.jpeg" % name
    cardTemplateData = templateMaker.createCardTemplate(guid, name, componentType, frontTextureName, totalCount, cardColumnCount, cardRowCount, backTextureName)
    templateFilepath = path.join(templateDirectoryPath, "%s.json" % guid)
    with open(templateFilepath, "w") as templateFile:
        dump(cardTemplateData, templateFile, indent=2)
    return cardTemplateData

async def createManifest(gameName, packageDirectoryPath):
    packageGuid = md5(gameName.encode()).hexdigest()
    manifestData = {
        "Name": gameName,
        "Version": "1",
        "GUID": packageGuid
    }
    manifestFilepath = path.join(packageDirectoryPath, "manifest.json")
    with open(manifestFilepath, "w") as manifestFile:
        dump(manifestData, manifestFile, indent=2)
    return packageGuid