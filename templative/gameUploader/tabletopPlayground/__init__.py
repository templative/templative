from os import path, mkdir, walk
from json import dump, load
from shutil import copyfile
from templative.gameUploader import instructionsLoader
from . import templateMaker
from .gameStateMaker import createGameStateVts
from PIL import Image
from hashlib import md5
import math

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
        "BusinessDeck": createDeck,
        "MicroDeck": createDeck,
        "MiniDeck": createDeck,
        "MintTinDeck": createDeck,
        "PokerDeck": createDeck,
        "SmallSquareChit": createDeck,
        "MediumSquareChit": createDeck,
        "LargeSquareChit": createDeck,
        "MintTinAccordion4": createBoard,
        "MintTinAccordion6": createBoard,
        "MintTinAccordion8": createBoard,
    }

    if not componentInstructions["type"] in supportedInstructionTypes:
        print("Skipping unsupported %s named %s" %(componentInstructions["type"],componentInstructions["name"]))
        return None

    return await supportedInstructionTypes[componentInstructions["type"]](packageDirectoryPath, componentInstructions)
    
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
    
async def createCompositeImageInTextures(componentName, componentType, frontInstructions, textureDirectoryFilepath):

    totalCount = 0
    for instruction in frontInstructions:
        totalCount += int(instruction["quantity"])

    columns = math.floor(math.sqrt(totalCount))
    rows = columns
    while columns * rows < totalCount:
        rows += 1

    componentDimensions = {
        "PokerDeck": (825, 1125),
        "BusinessDeck": (675, 1125),
        "MediumSquareChit": (300,300),
        "MiniDeck": (600, 825),
        "MicroDeck": (450, 600),
        "MintTinDeck": (750, 1125),
        "HexDeck": (1200, 1050),
    }
    dimensions = (825, 1125)
    if componentType in componentDimensions:
        dimensions = componentDimensions[componentType]
    else:
        print("Missing dimensions for %s, using 6,9." % componentType)

    tiledImage = Image.new('RGB',(dimensions[0]*columns, dimensions[1]*rows))
    
    xIndex = 0
    yIndex = 0
    for instruction in frontInstructions:
        image = Image.open(instruction["filepath"])
        for _ in range(int(instruction["quantity"])):
            tiledImage.paste(image,(xIndex*dimensions[0],yIndex*dimensions[1]))
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