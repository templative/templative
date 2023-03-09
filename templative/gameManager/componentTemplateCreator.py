from json import dump
from os import path
from shutil import copyfile

async def addToComponentCompose(name, type, gameRootDirectoryPath, componentComposeData):    
    for component in componentComposeData:
        if component["name"] != name:
            continue
        componentComposeData.remove(component)
        break

    componentComposeData.append({
        "name": name,
        "type": type,
        "quantity": 1,
        "piecesGamedataFilename": name,
        "componentGamedataFilename": name,
        "artdataFilename": "%sFront" % name,
        "backArtdataFilename": "%sBack" % name,
        "disabled": False
    })
    with open(path.join(gameRootDirectoryPath, 'component-compose.json'), 'w') as componentComposeFile:
        dump(componentComposeData, componentComposeFile, indent=4)

async def createPiecesCsv(piecesDirectoryPath, name):
    piecesCsvData = """name,displayName,quantity\n%s,%s,1""" % (name, name)
    with open(path.join(piecesDirectoryPath, '%s.csv' % name), 'w') as piecesCsvFile:
        piecesCsvFile.write(piecesCsvData)

async def createComponentJson(componentDirectoryPath, name):
    componentJsonData = {
        "displayName": name,
        "pieceDisplayName": name
    }   
    with open(path.join(componentDirectoryPath, '%s.json' % name), 'w') as componentJsonFile:
        dump(componentJsonData, componentJsonFile, indent=4)

async def createArtData(artDataDirectoryPath, name):
    
    with open(path.join(artDataDirectoryPath, '%sFront.json' % name), 'w') as artDataJsonFile:
        dump({
        "name": name,
        "templateFilename": "%sFront" % name,
        "textReplacements": [
        ],
        "styleUpdates":[
        ],
        "overlays": [
        ]
    }, artDataJsonFile, indent=4)
    with open(path.join(artDataDirectoryPath, '%sBack.json' % name), 'w') as artDataJsonFile:
        dump({
        "name": name,
        "templateFilename": "%sBack" % name,
        "textReplacements": [
        ],
        "styleUpdates":[
        ],
        "overlays": [
        ]
    }, artDataJsonFile, indent=4)

async def createComponentArtFiles(artTemplatesDirectoryPath, name, type):
    componentDirectoryPath = path.join(path.dirname(path.realpath(__file__)), "componentTemplates")
    componentTemplateFilepath = path.join(componentDirectoryPath, "%s.svg" % type)
    frontName = path.join(artTemplatesDirectoryPath, "%sFront.svg" % name)
    copyfile(componentTemplateFilepath, frontName)
    backName = path.join(artTemplatesDirectoryPath, "%sBack.svg" % name)
    copyfile(componentTemplateFilepath, backName)
