import os
import json

def dumpInstructions(filepath, data):
    if not filepath:
        raise Exception("Instructions filepath cannot be None")
    
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)

def createGameFolder(name, outputDirectory):    
    gameFolderPath = os.path.join(outputDirectory, name)
    os.mkdir(gameFolderPath)
    return gameFolderPath

def createComponentFolder(name, outputDirectory):
    componentDirectory = os.path.join(outputDirectory, name)
    os.mkdir(componentDirectory)
    return componentDirectory

def copyCompanyFromGameFolderToOutput(company, gameFolderPath):
    companyFilepath = os.path.join(gameFolderPath, "company.json")
    dumpInstructions(companyFilepath, company)

def copyGameFromGameFolderToOutput(game, gameFolderPath):
    companyFilepath = os.path.join(gameFolderPath, "game.json")
    dumpInstructions(companyFilepath, game)

