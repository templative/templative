from element import Element
import svgutils.transform as sg

templates = "/Users/oliverbarnum/apcw-defines/artComponents/templates"
graphicalInserts = "/Users/oliverbarnum/apcw-defines/artComponents/graphicalInserts"

def createDemoCard():
    actionCard = Element("actionCardTemplate.svg") 
    
    graphicsInsert = Element("embassy.svg")
    actionCard.placeat(graphicsInsert, 0.0, 0.0)

    power = actionCard.find_id("power")

    actionCard.dump("output.svg")

def replaceKeyWithValueInFile(filePath, key, value):
    with open(filePath, 'r') as f:
        res = f.read().replace(key, value)

    with open(filePath,'w') as f:
        f.write(res)

def change
