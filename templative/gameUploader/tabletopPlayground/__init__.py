from os import path, mkdir, walk
from json import dump, load
from shutil import copyfile
from templative.gameUploader import instructionsLoader
from . import templateMaker
from PIL import Image
from hashlib import md5
import math

async def convertToTabletopPlayground(producedDirectoryPath, playgroundPackagesDirectory):

    game = await instructionsLoader.loadGameInstructions(producedDirectoryPath)
    studio = await instructionsLoader.loadStudioInstructions(producedDirectoryPath)

    print("Convert %s into a Tabletop Playground package for %s." % (game["displayName"], studio["displayName"]))

    packageDirectoryPath = await createPackageDirectories(game["name"], playgroundPackagesDirectory)
    manifestFilepath = await createManifest(game["name"], packageDirectoryPath)
    await copyComponentsToPackage(producedDirectoryPath, packageDirectoryPath)

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
    for directoryPath in next(walk(producedDirectoryPath))[1]:
        componentDirectoryPath = "%s/%s" % (producedDirectoryPath, directoryPath)
        await copyComponentToPackage(componentDirectoryPath, packageDirectoryPath)

async def copyComponentToPackage(componentDirectoryPath, packageDirectoryPath):
    componentInstructions = None
    componentInstructionsFilepath = path.join(componentDirectoryPath, "component.json")
    with open(componentInstructionsFilepath, "r") as componentInstructionsFile:
        componentInstructions = load(componentInstructionsFile)
    
    if componentInstructions["type"] != "PokerDeck":
        return
    
    totalCount, cardColumnCount, cardRowCount = await copyImages(componentInstructions, path.join(packageDirectoryPath, "Textures"))
    componentGuid = md5(componentInstructions["name"].encode()).hexdigest()
    await createTemplateFile(path.join(packageDirectoryPath, "Templates"), componentGuid, componentInstructions["name"], totalCount, cardColumnCount, cardRowCount)
    
async def createCompositeImageInTextures(componentName, frontInstructions, textureDirectoryFilepath):

    totalCount = 0
    for instruction in frontInstructions:
        totalCount += int(instruction["quantity"])

    columns = math.floor(math.sqrt(totalCount))
    rows = columns
    while columns * rows < totalCount:
        rows += 1

    tiledImage = Image.new('RGB',(825*columns, 1125*rows))
    
    xIndex = 0
    yIndex = 0
    for instruction in frontInstructions:
        image = Image.open(instruction["filepath"])
        for _ in range(int(instruction["quantity"])):
            tiledImage.paste(image,(xIndex*825,yIndex*1125))
            xIndex += 1
            if xIndex == columns:
                xIndex = 0
                yIndex +=1

    frontImageName = "%s-front.jpeg" % componentName
    frontImageFilepath = path.join(textureDirectoryFilepath, frontImageName)
    tiledImage.save(frontImageFilepath,"JPEG")
    return totalCount, columns, rows

async def copyBackImageToTextures(componentName, backInstructions, textureDirectoryFilepath):
    backImageName = "%s-back.jpg" % componentName
    backImageFilepath = path.join(textureDirectoryFilepath, backImageName)
    copyfile(backInstructions["filepath"], backImageFilepath)

async def copyImages(componentInstructions, textureDirectoryFilepath):
    totalCardQuantity = await createCompositeImageInTextures(componentInstructions["name"], componentInstructions["frontInstructions"], textureDirectoryFilepath)
    await copyBackImageToTextures(componentInstructions["name"], componentInstructions["backInstructions"], textureDirectoryFilepath)
    return totalCardQuantity

async def createTemplateFile(templateDirectoryPath, guid, name, totalCount, cardColumnCount, cardRowCount):
    frontTextureName = "%s-front.jpeg" % name
    backTextureName = "%s-back.jpg" % name
    cardTemplateData = templateMaker.createCardTemplate(guid, name, frontTextureName, totalCount, cardColumnCount, cardRowCount, backTextureName)
    templateFilepath = path.join(templateDirectoryPath, "%s.json" % guid)
    with open(templateFilepath, "w") as templateFile:
        dump(cardTemplateData, templateFile, indent=2)
    return templateFilepath

async def createManifest(gameName, packageDirectoryPath):
    manifestData = {
        "Name": gameName,
        "Version": "1",
        "GUID": md5(gameName.encode()).hexdigest()
    }
    manifestFilepath = path.join(packageDirectoryPath, "manifest.json")
    with open(manifestFilepath, "w") as manifestFile:
        dump(manifestData, manifestFile, indent=2)
    return manifestFilepath