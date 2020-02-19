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
            graphicsInsert = Element("%s.svg" % componentGamedataRow[overlay])
            artFile.placeat(graphicsInsert, 0.0, 0.0)

        artFileOutputNamen = "%s-%s" % (component["name"], componentGamedataRow["name"])
        artFileOutputFilename = "%s.svg" % artFileOutputFilename

        artFile.dump(artFileOutputFilename)
        
        for textReplacement in artMetaData["textReplacementSources"]:
            replaceKeyWithValueInFile(artFileOutputFilename, "{power}", "3")
        
        for styleUpdate in artMetaData["styleUpdateSources"]:
            findById = styleUpdate["id"]
            styleValue = componentGamedataRow[styleUpdate["source"]]
            replaceStyleWith = "#%s" % styleValue
            changeStyleById(artFileOutputFilename, findById, replaceStyleWith)

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
