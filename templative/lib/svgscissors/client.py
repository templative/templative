import os
import asyncio
import svgutils.transform as sg
import xml.etree.ElementTree as ET
from wand.image import Image
from aiofile import AIOFile
import wand.exceptions
from .element import Element

async def createArtfile(artFile, artFileOutputName, outputDirectory):

    artFileOutputFileName = "%s.svg" % (artFileOutputName)
    artFileOutputFilepath = os.path.join(outputDirectory, artFileOutputFileName)
    artFile.dump(artFileOutputFilepath)
    return artFileOutputFilepath

async def addOverlays(artFile, overlays, game, gameCompose, componentGamedata, pieceGamedata):
    if artFile == None:
        print("artFile cannot be None.")
        return

    if overlays == None:
        print("overlays cannot be None.")
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
        overlayName = await getScopedValue(overlay, game, componentGamedata, pieceGamedata)
        if overlayName != None and overlayName != "":
            overlayFilename = "%s.svg" % (overlayName)
            overlayFilepath = os.path.join(overlayFilesDirectory, overlayFilename)
            graphicsInsert = Element(overlayFilepath)
            artFile.placeat(graphicsInsert, 0.0, 0.0)

async def textReplaceInFile(filepath, textReplacements, game, componentGamedata, pieceGamedata):
    if filepath == None:
        print("filepath cannot be None.")
        return

    if textReplacements == None:
        print("textReplacements cannot be None.")
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
            value = await getScopedValue(textReplacement, game, componentGamedata, pieceGamedata)
            value = await processValueFilters(value, textReplacement)
            contents = contents.replace(key, value)

    async with AIOFile(filepath,'w') as f:
        await f.write(contents)

async def processValueFilters(value, textReplacement):
    if "filters" in textReplacement:
        for filter in textReplacement["filters"]:
            if filter == "toUpper":
                value = value.upper()
    return value

async def updateStylesInFile(filepath, styleUpdates, game, componentGamedata, pieceGamedata):
    if filepath == None:
        print("filepath cannot be None.")
        return

    if styleUpdates == None:
        print("styleUpdates cannot be None.")
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
        parsedTree = ET.parse(filepath)
        tree = parsedTree.getroot()

        for styleUpdate in styleUpdates:
            findById = styleUpdate["id"]
            elementToUpdate = tree.find(".//*[@id='%s']" % findById)
            if (elementToUpdate != None):
                value = await getScopedValue(styleUpdate, game, componentGamedata, pieceGamedata)
                await replaceStyleAttributeForElement(elementToUpdate, "style", styleUpdate["cssValue"], value)
            else:
                print("Could not find element with id [%s]." % (findById))

        async with AIOFile(filepath,'wb') as f:
            await f.write(ET.tostring(tree))
    except ET.ParseError as pe:
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

async def getScopedValue(scopedValue, game, componentGamedata, pieceGamedata):
    if scopedValue == None:
        print("scopedValue cannot be None.")
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

    if scope == "game":
        return game[source]

    if scope == "component":
        return componentGamedata[source]

    if scope == "piece":
        return pieceGamedata[source]

    return source


async def exportSvgToJpg(filepath, name, outputDirectory):
    outputFilename = "%s.jpg" % (name)
    outputFilepath = os.path.join(outputDirectory, outputFilename)
    try:
        svgImage = Image(filename=filepath)    
        svgImage.save(filename=outputFilepath)
        svgImage.close()
    except wand.exceptions.WandRuntimeError as error:
        print(error, filepath, name)