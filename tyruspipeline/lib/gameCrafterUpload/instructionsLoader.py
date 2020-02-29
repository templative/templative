import os
import json

def loadGameInstructions(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "game.json")) as game:
        return json.load(game)

def loadCompanyInstructions(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    with open(os.path.join(gameRootDirectoryPath, "company.json")) as company:
        return json.load(company)

def loadComponentInstructions(componentDirectoryPath):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    with open(os.path.join(componentDirectoryPath, "component.json")) as componentFile:
        return json.load(componentFile)