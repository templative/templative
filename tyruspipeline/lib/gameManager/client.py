import os
import json
import csv
from ..svgscissors import operations as processor

def loadGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "game.json")) as game:
        return json.load(game)

def loadCompany(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "company.json")) as company:
        return json.load(company)

def loadGameCompose(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "game-compose.json")) as gameCompose:
        return json.load(gameCompose)

def loadGameComponents(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "components.json")) as componentFile:
        return json.load(componentFile)

def loadPiecesGamedata(gameRootDirectoryPath, gameCompose, gamedataFilename):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    if not gamedataFilename:
        return {}

    piecesGamedataDirectory = gameCompose["piecesGamedataDirectory"]
    gamedataFilenameWithExtension = "%s.csv" % (gamedataFilename)
    filepath = os.path.join(gameRootDirectoryPath, piecesGamedataDirectory, gamedataFilenameWithExtension)
    with open(filepath) as gamedataFile:
        reader = csv.DictReader(gamedataFile, delimiter=',', quotechar='"')

        gamedata = []
        for row in reader:
            gamedata.append(row)
        return gamedata

def loadArtMetadata(gameRootDirectoryPath, gameCompose, artMetadataFilename):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    if not artMetadataFilename:
        return {}

    artMetadataDirectory = gameCompose["artMetadataDirectory"]
    artMetadataFilenameWithExtension = "%s.json" % (artMetadataFilename)
    filepath = os.path.join(gameRootDirectoryPath, artMetadataDirectory, artMetadataFilenameWithExtension)
    with open(filepath) as metadataFile:
        return json.load(metadataFile)

def dumpInstructions(filepath, data):
    if not filepath:
        raise Exception("Instructions filepath cannot be None")
    
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)

def createGameFolder(name, outputDirectory):    
    gameFolderPath = os.path.join(outputDirectory, name)
    os.mkdir(gameFolderPath)
    return gameFolderPath

def copyCompanyFromGameFolderToOutput(gameRootDirectoryPath, gameFolderPath):
    company = loadCompany(gameRootDirectoryPath)
    companyFilepath = os.path.join(gameFolderPath, "company.json")
    dumpInstructions(companyFilepath, company)

def copyGameFromGameFolderToOutput(game, gameFolderPath):
    companyFilepath = os.path.join(gameFolderPath, "game.json")
    dumpInstructions(companyFilepath, game)

def produceGameComponent(gameRootDirectoryPath, game, gameCompose, component, outputDirectory):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    componentDisplayName = component["displayName"]

    piecesGamedata = loadPiecesGamedata(gameRootDirectoryPath, gameCompose, component["gamedataFilename"])
    if not piecesGamedata or piecesGamedata == {}:
        print("Skipping %s component due to missing game data." % componentDisplayName)
        return

    componentArtMetadata = loadArtMetadata(gameRootDirectoryPath, gameCompose, component["artMetadataFilename"])
    if not componentArtMetadata or componentArtMetadata == {}:
        print("Skipping %s component due to missing front art metadata." % componentDisplayName)
        return

    componentBackArtMetadata = loadArtMetadata(gameRootDirectoryPath, gameCompose, component["backArtMetadataFilename"])
    if not componentBackArtMetadata or componentBackArtMetadata == {}:
        print("Skipping %s component due to missing back art metadata." % componentDisplayName)
        return

    print("Creating art assets for %s component." % (componentDisplayName))

    componentName = component["name"]
    componentDirectory = os.path.join(outputDirectory, componentName)
    os.mkdir(componentDirectory)

    componentInstructionFilepath = os.path.join(componentDirectory, "component.json")

    fileInstructionSets = processor.getInstructionSetsForFiles(game, component, piecesGamedata, componentDirectory)
    backInstructionSet = processor.getBackInstructionSet(component, componentDirectory)
    componentInstructions = {
        "name": componentName, 
        "type": component["type"],
        "quantity": component["quantity"],
        "fileInstructions": fileInstructionSets,
        "backInstructions": backInstructionSet
    }
    dumpInstructions(componentInstructionFilepath, componentInstructions)

    processor.createArtFilesForComponent(game, gameCompose, component, componentArtMetadata, componentBackArtMetadata,  piecesGamedata, componentDirectory)