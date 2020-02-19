from element import Element
import svgutils.transform as sg
import xml.etree.ElementTree as ET

def createArtFilesForComponent(component, artMetaData, componentGamedata, outputDirectory):
    if component is None:
        return
    
    if artMetaData is None:
        return

    if componentGamedata is None:
        return

    templateFilesDirectory = "artComponents/templates"
    for componentGamedataRow in componentGamedata:

        artFile = Element("%s/%s.svg" % (templateFilesDirectory, artMetaData["templateFilename"])) 
        
        for overlay in artMetaData["svgOverlaysSource"]:
            overlayName = componentGamedataRow[overlay]
            if overlayName:
                graphicsInsert = Element("%s.svg" % overlayName)
                artFile.placeat(graphicsInsert, 0.0, 0.0)

        artFileOutputName = ("%s-%s" % (component["name"], componentGamedataRow["name"])).replace(" ", "")
        artFileOutputFilePath = "%s/%s.svg" % (outputDirectory, artFileOutputName)

        artFile.dump(artFileOutputFilePath)
        
        for textReplacement in artMetaData["textReplacementSources"]:
            replaceKeyWithValueInFile(artFileOutputFilePath, "{power}", "3")
        
        for styleUpdate in artMetaData["styleUpdateSources"]:
            findById = styleUpdate["id"]
            styleValue = componentGamedataRow[styleUpdate["source"]]
            replaceStyleWith = "#%s" % styleValue
            changeStyleById(artFileOutputFilePath, findById, replaceStyleWith)

def processComponent(gamedataRow, artMetaData):
    pass

def replaceKeyWithValueInFile(filePath, key, value):
    with open(filePath, 'r') as f:
        res = f.read().replace(key, value)

    with open(filePath,'w') as f:
        f.write(res)

def changeStyleById(filePath, id, style):
    tree = ET.parse(filePath)
    tree = tree.getroot()
    sh = tree.find(".//*[@id='background']")
    sh.set('style', style)

    with open(filePath,'w') as f:
        f.write(ET.tostring(tree))
