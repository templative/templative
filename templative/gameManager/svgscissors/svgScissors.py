import os
from xml.etree import ElementTree
from aiofile import AIOFile
import svgmanip
from ..componentStats import componentImageSizePixels

async def createArtFileOfPiece(game, studioCompose,  gameCompose, componentCompose, componentGamedata, pieceGamedata, artMetaData, outputDirectory, isSimple, isPublish):
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

    await addOverlays(artFile, artMetaData["overlays"], studioCompose, game, gameCompose, componentGamedata, pieceGamedata, isSimple, isPublish)

    artFileOutputName = ("%s-%s" % (componentCompose["name"], pieceGamedata["name"]))
    artFileOutputFilepath = await createArtfile(artFile, artFileOutputName, outputDirectory)

    await textReplaceInFile(artFileOutputFilepath, artMetaData["textReplacements"], studioCompose, game, componentGamedata, pieceGamedata, isSimple, isPublish)
    await updateStylesInFile(artFileOutputFilepath, artMetaData["styleUpdates"], studioCompose, game, componentGamedata, pieceGamedata)
    
    if not componentCompose["type"] in componentImageSizePixels:
        raise Exception("No image size for %s", componentCompose["type"]) 
    imageSizePixels = componentImageSizePixels[componentCompose["type"]]
    await assignSize(artFileOutputFilepath, imageSizePixels)
    await addNewlines(artFileOutputFilepath)
    await exportSvgToImage(artFileOutputFilepath, imageSizePixels, artFileOutputName, outputDirectory)
    print("Produced %s." % (pieceGamedata["name"]))

async def addNewlines(artFileOutputFilepath):
    file = open(artFileOutputFilepath, "r")
    contents = file.read()
    file.close()
    fixedContents = contents.replace("NEWLINE", "\n")
    if fixedContents == contents:
        return
    file = open(artFileOutputFilepath, "w")
    file.write(fixedContents)
    file.close()

async def assignSize(artFileOutputFilepath, imageSizePixels):
    
    parser = ElementTree.XMLParser(encoding="utf-8")
    elementTree = ElementTree.parse(artFileOutputFilepath, parser=parser)
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

async def addOverlays(artFile, overlays, studio, game, gameCompose, componentGamedata, pieceGamedata, isSimplifiedGraphic, isPublish):
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
        isComplex = overlay["isComplex"] if "isComplex" in overlay else False
        if isComplex and isSimplifiedGraphic:
            continue

        isDebug = overlay["isDebugInfo"] if "isDebugInfo" in overlay else False
        if isDebug and isPublish:
            continue

        overlayName = await getScopedValue(overlay, studio, game, componentGamedata, pieceGamedata)
        if overlayName != None and overlayName != "":
            overlayFilename = "%s.svg" % (overlayName)
            overlayFilepath = os.path.join(overlayFilesDirectory, overlayFilename)
            graphicsInsert = svgmanip.Element(overlayFilepath)
            artFile.placeat(graphicsInsert, 0.0, 0.0)

async def textReplaceInFile(filepath, textReplacements, studio, game, componentGamedata, pieceGamedata, isSimplifiedGraphic, isPublish):
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

            isComplex = textReplacement["isComplex"] if "isComplex" in textReplacement else False
            if isComplex and isSimplifiedGraphic:
                value = ""

            isDebug = textReplacement["isDebugInfo"] if "isDebugInfo" in textReplacement else False
            if isDebug and isPublish:
                value = ""

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
    # print(message)
    # subprocess.run(commands)
    os.system(message)

async def exportSvgToImage(filepath, imageSizePixels, name, outputDirectory):
    absoluteSvgFilepath = os.path.abspath(filepath)
    absoluteOutputDirectory = os.path.abspath(outputDirectory)
    pngFilepath = os.path.join(absoluteOutputDirectory, "%s.png" % (name))
    createPngCommands = [
        "inkscape", 
        absoluteSvgFilepath,
        '--export-filename=%s' % pngFilepath, 
        "--export-width=%s" % imageSizePixels["width"], 
        "--export-height=%s" % imageSizePixels["height"],
        "--export-background-opacity=0" ]
    
    runCommands(createPngCommands)

    jpgFilepath = os.path.join(absoluteOutputDirectory, "%s.jpg" % (name))
    convertCommands = [ "convert", pngFilepath, jpgFilepath ]
    runCommands(convertCommands)

    os.remove(pngFilepath)
    