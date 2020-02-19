from element import Element
import svgutils.transform as sg
import xml.etree.ElementTree as ET

templates = "/Users/oliverbarnum/apcw-defines/artComponents/templates"
graphicalInserts = "/Users/oliverbarnum/apcw-defines/artComponents/graphicalInserts"

def createDemoCard():
    actionCard = Element("actionCardTemplate.svg") 
    
    graphicsInsert = Element("embassy.svg")
    actionCard.placeat(graphicsInsert, 0.0, 0.0)

    actionCard.dump("output.svg")
    replaceKeyWithValueInFile("output.svg", "{power}", "3")
    replaceKeyWithValueInFile("output.svg", "{title}", "Embassy")
    replaceKeyWithValueInFile("output.svg", "{quantity}", "5")
    replaceKeyWithValueInFile("output.svg", "{version}", "5.0.0")
    replaceKeyWithValueInFile("output.svg", "{active}", "")
    replaceKeyWithValueInFile("output.svg", "{activeDescription}", "")
    replaceKeyWithValueInFile("output.svg", "{passive}", "Passive")
    replaceKeyWithValueInFile("output.svg", "{passiveDescription}", "Diplomats here are worth two power.")
    changeStyleById("output.svg", "background", "fill:#70a7da")

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
