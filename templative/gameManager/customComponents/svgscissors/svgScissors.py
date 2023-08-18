import os, subprocess, time
from xml.etree import ElementTree
from aiofile import AIOFile
import svgmanip
from templative.componentInfo import COMPONENT_INFO
import git

from templative.gameManager.models.produceProperties import ProduceProperties
from templative.gameManager.models.gamedata import StudioData, GameData, ComponentData, ComponentBackData, PieceData
from templative.gameManager.models.composition import ComponentComposition
from templative.gameManager.models.artdata import ComponentArtdata

async def createArtFileOfPiece(compositions:ComponentComposition, artdata:any, gamedata:PieceData|ComponentBackData, componentBackOutputDirectory:str, produceProperties:ProduceProperties) -> None:
    
    templateFilesDirectory = compositions.gameCompose["artTemplatesDirectory"]
    artFilename = "%s.svg" % (artdata["templateFilename"])
    artFilepath = os.path.join(templateFilesDirectory, artFilename)
    artFile = svgmanip.Element(artFilepath)

    await addOverlays(artFile, artdata["overlays"], compositions, gamedata, produceProperties.isSimple, produceProperties.isPublish)
    pieceName = gamedata.pieceData["name"] if isinstance(gamedata, PieceData) else gamedata.componentBackDataBlob["name"]

    artFileOutputName = ("%s%s-%s" % (compositions.componentCompose["name"], gamedata.pieceUniqueBackHash, pieceName))
    artFileOutputFilepath = await createArtfile(artFile, artFileOutputName, componentBackOutputDirectory)

    await textReplaceInFile(artFileOutputFilepath, artdata["textReplacements"], gamedata, produceProperties.isSimple, produceProperties.isPublish)
    await updateStylesInFile(artFileOutputFilepath, artdata["styleUpdates"], gamedata)
    
    if not compositions.componentCompose["type"] in COMPONENT_INFO:
        raise Exception("No image size for %s", compositions.componentCompose["type"]) 
    component = COMPONENT_INFO[compositions.componentCompose["type"]]

    imageSizePixels = component["DimensionsPixels"]
    await assignSize(artFileOutputFilepath, imageSizePixels)
    await addNewlines(artFileOutputFilepath)
    await exportSvgToImage(artFileOutputFilepath, imageSizePixels, artFileOutputName, componentBackOutputDirectory)
    print("Produced %s." % (pieceName))

async def addNewlines(artFileOutputFilepath):
    contents = ""
    async with AIOFile(artFileOutputFilepath, 'r') as f:
        contents = await f.read()
    fixedContents = contents.replace("NEWLINE", "\n")
    if fixedContents == contents:
        return
    async with AIOFile(artFileOutputFilepath, 'w') as f:
        f.write(fixedContents)

async def assignSize(artFileOutputFilepath, imageSizePixels):
    
    parser = ElementTree.XMLParser(encoding="utf-8")
    elementTree = ElementTree.parse(artFileOutputFilepath, parser=parser)
    root = elementTree.getroot()
    root.set("width", "%spx" % imageSizePixels[0])
    root.set("height", "%spx" % imageSizePixels[1])
    root.set("viewbox", "0 0 %s %s" % (imageSizePixels[0], imageSizePixels[1]))
    async with AIOFile(artFileOutputFilepath,'wb') as f:
        await f.write(ElementTree.tostring(root))
    
async def createArtfile(artFile, artFileOutputName, outputDirectory):
    artFileOutputFileName = "%s.svg" % (artFileOutputName)
    artFileOutputFilepath = os.path.join(outputDirectory, artFileOutputFileName)
    artFile.dump(artFileOutputFilepath)
    return artFileOutputFilepath

async def addOverlays(artFile, overlays, compositions:ComponentComposition, pieceGamedata:PieceData, isSimplifiedGraphic, isPublish):
    if artFile == None:
        print("artFile cannot be None.")
        return

    if overlays == None:
        print("overlays cannot be None.")
        return

    overlayFilesDirectory = compositions.gameCompose["artInsertsDirectory"]

    for overlay in overlays:
        isComplex = overlay["isComplex"] if "isComplex" in overlay else False
        if isComplex and isSimplifiedGraphic:
            continue

        isDebug = overlay["isDebugInfo"] if "isDebugInfo" in overlay else False
        if isDebug and isPublish:
            continue

        overlayName = await getScopedValue(overlay, pieceGamedata)
        if overlayName != None and overlayName != "":
            overlayFilename = "%s.svg" % (overlayName)
            overlayFilepath = os.path.join(overlayFilesDirectory, overlayFilename)
            graphicsInsert = svgmanip.Element(overlayFilepath)
            artFile.placeat(graphicsInsert, 0.0, 0.0)

async def textReplaceInFile(filepath, textReplacements, gamedata:PieceData|ComponentBackData, isSimplifiedGraphic, isPublish):
    if filepath == None:
        print("filepath cannot be None.")
        return

    if textReplacements == None:
        print("textReplacements cannot be None.")
        return

    contents = ""
    async with AIOFile(filepath, 'r') as f:
        contents = await f.read()
        for textReplacement in textReplacements:
            key = "{%s}" % textReplacement["key"]
            value = await getScopedValue(textReplacement, gamedata)
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

async def updateStylesInFile(filepath, styleUpdates, pieceGamedata: PieceData):
    if filepath == None:
        print("filepath cannot be None.")
        return

    if styleUpdates == None:
        print("styleUpdates cannot be None.")
        return    

    try:
        parsedTree = ElementTree.parse(filepath)
        tree = parsedTree.getroot()

        for styleUpdate in styleUpdates:
            findById = styleUpdate["id"]
            elementToUpdate = tree.find(".//*[@id='%s']" % findById)
            if (elementToUpdate != None):
                value = await getScopedValue(styleUpdate, pieceGamedata)
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

    if replaceStyleWith[len(replaceStyleWith)-1] == ";":
        replaceStyleWith = replaceStyleWith[:len(replaceStyleWith)-1]
    element.set(attribute, replaceStyleWith)

async def getScopedValue(scopedValue, pieceGameData: PieceData|ComponentBackData):
    if scopedValue == None:
        print("scopedValue cannot be None.")
        return

    scope = scopedValue["scope"]
    source = scopedValue["source"]

    scopeData = None
    if scope == "studio":
        scopeData = pieceGameData.studioDataBlob

    if scope == "game":
        scopeData = pieceGameData.gameDataBlob

    if scope == "component":
        scopeData = pieceGameData.componentDataBlob

    if scope == "piece":
        scopeData = pieceGameData.pieceData if isinstance(pieceGameData, PieceData) else pieceGameData.componentBackDataBlob 

    if scope == "global":
        return source
    
    if scope == "utility":
        utilityFunctions = {
            "git-sha": getCurrentGitSha
        }
        if not source in utilityFunctions:
            print("Missing function %s not found in %s scope." % (source, scope))
            return source
        return utilityFunctions[source]()

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
        "--export-width=%s" % imageSizePixels[0], 
        "--export-height=%s" % imageSizePixels[1],
        "--export-background-opacity=0" ]
    
    runCommands(createPngCommands)

    jpgFilepath = os.path.join(absoluteOutputDirectory, "%s.jpg" % (name))
    convertCommands = [ 
        "magick convert", 
        '"%s"' % pngFilepath, 
        '"%s"' % jpgFilepath ]
    runCommands(convertCommands)

    os.remove(pngFilepath)

def getCurrentGitSha():
    repo = git.Repo(search_parent_directories=True)
    return repo.head.object.hexsha