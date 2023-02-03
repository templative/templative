import os
from xml.etree import ElementTree
from aiofile import AIOFile
import svgmanip
import subprocess

componentImageSizePixels = {
    "PokerDeck": { "width": 825, "height":1125 },
    "LargeRing": { "width": 450, "height":450 },
    "MediumRing": { "width": 375, "height": 375 },
    "LargeSquareChit": { "width": 375, "height": 375 },
    "SmallStoutBox": { "width": 3600, "height": 3000 },
}

async def createArtFileOfPiece(game, studioCompose,  gameCompose, componentCompose, componentGamedata, pieceGamedata, artMetaData, outputDirectory):
    if game == None:
        print("game cannot be None.")
        return

    if studioCompose == None:
        print("studioCompose cannot be None.")
        return

    if componentCompose == None:
        print("componentCompose cannot be None.")
        return

    if artMetaData == None:
        print("artMetaData cannot be None.")
        return

    if componentGamedata == None:
        print("componentGamedata cannot be None.")
        return

    if pieceGamedata == None:
        print("pieceGamedata cannot be None.")
        return

    if outputDirectory == None:
        print("outputDirectory cannot be None.")
        return

    templateFilesDirectory = gameCompose["artTemplatesDirectory"]
    artFilename = "%s.svg" % (artMetaData["templateFilename"])
    artFile = svgmanip.Element(os.path.join(templateFilesDirectory, artFilename))

    await addOverlays(artFile, artMetaData["overlays"], studioCompose, game, gameCompose, componentGamedata, pieceGamedata)

    artFileOutputName = ("%s-%s" % (componentCompose["name"], pieceGamedata["name"]))
    artFileOutputFilepath = await createArtfile(artFile, artFileOutputName, outputDirectory)

    await textReplaceInFile(artFileOutputFilepath, artMetaData["textReplacements"], studioCompose, game, componentGamedata, pieceGamedata)
    await updateStylesInFile(artFileOutputFilepath, artMetaData["styleUpdates"], studioCompose, game, componentGamedata, pieceGamedata)
    
    if not componentCompose["type"] in componentImageSizePixels:
        raise Exception("No image size for %s", componentCompose["type"]) 
    imageSizePixels = componentImageSizePixels[componentCompose["type"]]
    await assignSize(artFileOutputFilepath, imageSizePixels)
    await exportSvgToImage(artFileOutputFilepath, imageSizePixels, artFileOutputName, outputDirectory)
    print("Produced %s." % (pieceGamedata["name"]))


async def assignSize(artFileOutputFilepath, imageSizePixels):
    elementTree = ElementTree.parse(artFileOutputFilepath)
    root = elementTree.getroot()
    root.set("width", "%spx" % imageSizePixels["width"])
    root.set("height", "%spx" % imageSizePixels["height"])
    root.set("viewbox", "0 0 %s %s" % (imageSizePixels["width"], imageSizePixels["height"]))
    async with AIOFile(artFileOutputFilepath,'wb') as f:
        await f.write(ElementTree.tostring(root))
    
async def createArtfile(artFile, artFileOutputName, outputDirectory):
    artFileOutputFileName = "%s.svg" % (artFileOutputName)
    artFileOutputFilepath = os.path.join(outputDirectory, artFileOutputFileName)
    artFile.dump(artFileOutputFilepath)
    return artFileOutputFilepath

async def addOverlays(artFile, overlays, studio, game, gameCompose, componentGamedata, pieceGamedata):
    if artFile == None:
        print("artFile cannot be None.")
        return

    if overlays == None:
        print("overlays cannot be None.")
        return

    if studio == None:
        print("studio cannot be None.")
        return

    if game == None:
        print("game cannot be None.")
        return

    if componentGamedata == None:
        print("componentGamedata cannot be None.")
        return

    if pieceGamedata == None:
        print("pieceGamedata cannot be None.")
        return

    overlayFilesDirectory = gameCompose["artInsertsDirectory"]

    for overlay in overlays:
        overlayName = await getScopedValue(overlay, studio, game, componentGamedata, pieceGamedata)
        if overlayName != None and overlayName != "":
            overlayFilename = "%s.svg" % (overlayName)
            overlayFilepath = os.path.join(overlayFilesDirectory, overlayFilename)
            graphicsInsert = svgmanip.Element(overlayFilepath)
            artFile.placeat(graphicsInsert, 0.0, 0.0)

async def textReplaceInFile(filepath, textReplacements, studio, game, componentGamedata, pieceGamedata):
    if filepath == None:
        print("filepath cannot be None.")
        return

    if textReplacements == None:
        print("textReplacements cannot be None.")
        return

    if studio == None:
        print("studio cannot be None.")
        return

    if game == None:
        print("game cannot be None.")
        return

    if componentGamedata == None:
        print("componentGamedata cannot be None.")
        return

    if pieceGamedata == None:
        print("pieceGamedata cannot be None.")
        return

    contents = ""
    async with AIOFile(filepath, 'r') as f:
        contents = await f.read()
        for textReplacement in textReplacements:
            key = "{%s}" % textReplacement["key"]
            value = await getScopedValue(textReplacement, studio, game, componentGamedata, pieceGamedata)
            value = await processValueFilters(value, textReplacement)
            contents = contents.replace(key, str(value))

    async with AIOFile(filepath,'w') as f:
        await f.write(contents)

async def processValueFilters(value, textReplacement):
    if "filters" in textReplacement:
        for filter in textReplacement["filters"]:
            if filter == "toUpper":
                value = value.upper()
    return value

async def updateStylesInFile(filepath, styleUpdates, studio, game, componentGamedata, pieceGamedata):
    if filepath == None:
        print("filepath cannot be None.")
        return

    if styleUpdates == None:
        print("styleUpdates cannot be None.")
        return

    if studio == None:
        print("studio cannot be None.")
        return

    if game == None:
        print("game cannot be None.")
        return

    if componentGamedata == None:
        print("componentGamedata cannot be None.")
        return

    if pieceGamedata == None:
        print("pieceGamedata cannot be None.")
        return

    try:
        parsedTree = ElementTree.parse(filepath)
        tree = parsedTree.getroot()

        for styleUpdate in styleUpdates:
            findById = styleUpdate["id"]
            elementToUpdate = tree.find(".//*[@id='%s']" % findById)
            if (elementToUpdate != None):
                value = await getScopedValue(styleUpdate, studio, game, componentGamedata, pieceGamedata)
                await replaceStyleAttributeForElement(elementToUpdate, "style", styleUpdate["cssValue"], value)
            else:
                print("Could not find element with id [%s]." % (findById))

        async with AIOFile(filepath,'wb') as f:
            await f.write(ElementTree.tostring(tree))
    except ElementTree.ParseError as pe:
        print("Production failed!", pe, filepath)

async def replaceStyleAttributeForElement(element, attribute, key, value):
    attributeValue = element.get(attribute, "")

    replaceStyleWith = ""
    found = False

    cssKeyValuePairs = attributeValue.split(';')
    for cssKeyValuePair in cssKeyValuePairs:
        keyAndPair = cssKeyValuePair.split(':')
        if (keyAndPair[0] == key):
            replaceStyleWith += "%s:%s;" % (key, value)
            found = True
        else:
            replaceStyleWith += cssKeyValuePair + ';'

    if (not found):
        newCss = "%s:%s;" % (key, value)
        replaceStyleWith += newCss

    replaceStyleWith = "%s:%s" % (key, value)
    element.set(attribute, replaceStyleWith)

async def getScopedValue(scopedValue, studio, game, componentGamedata, pieceGamedata):
    if scopedValue == None:
        print("scopedValue cannot be None.")
        return
    
    if studio == None:
        print("studio cannot be None.")
        return
    
    if game == None:
        print("game cannot be None.")
        return

    if componentGamedata == None:
        print("componentGamedata cannot be None.")
        return

    if pieceGamedata == None:
        print("pieceGamedata cannot be None.")
        return

    scope = scopedValue["scope"]
    source = scopedValue["source"]

    scopeData = None
    if scope == "game":
        scopeData = game

    if scope == "component":
        scopeData = componentGamedata

    if scope == "piece":
        scopeData = pieceGamedata

    if scope == "studio":
        scopeData = studio

    if scope == "global":
        return source

    if not source in scopeData:
        print("Missing key %s not found in %s scope." % (source, scope))
        return source

    return scopeData[source]

def runCommands(commands):
    message = ""
    for command in commands:
        message = message + command + " "
    
    subprocess.run(commands, shell=True)

async def exportSvgToImage(filepath, imageSizePixels, name, outputDirectory):
    

    pngFilepath = os.path.abspath(os.path.join(outputDirectory, "%s.png" % (name))) 
    runCommands([
        "inkscape", filepath, "--export-filename=" + pngFilepath, "--export-width=%s" % imageSizePixels["width"], "--export-height=%s" % imageSizePixels["height"],"--export-background-opacity=0" ])

    jpgFilepath = os.path.abspath(os.path.join(outputDirectory, "%s.jpg" % (name))) 
    runCommands(["convert", pngFilepath, jpgFilepath ])
    