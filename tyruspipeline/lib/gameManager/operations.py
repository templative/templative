import uuid
import os
from datetime import datetime
from distutils.dir_util import copy_tree

import client as client

def produceGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = client.loadGame(gameRootDirectoryPath)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    uniqueGameName = ("%s_%s_%s_%s" % (game["name"], game["version"], game["versionName"], timestamp)).replace(" ", "")
    game["name"] = uniqueGameName

    gameCompose = client.loadGameCompose(gameRootDirectoryPath)

    gameFolderPath = client.createGameFolder(game["name"], gameCompose["outputDirectory"])
    print("Producing %s" % gameFolderPath)

    client.copyCompanyFromGameFolderToOutput(gameRootDirectoryPath, gameFolderPath)
    client.copyGameFromGameFolderToOutput(game, gameFolderPath)
    
    components = client.loadGameComponents(gameRootDirectoryPath)
    for component in components["components"]:
        client.produceGameComponent(gameRootDirectoryPath, game, gameCompose, component, gameFolderPath)

    print("Done producing %s" % gameFolderPath)

    return gameFolderPath

def createTemplate():
    if(os.path.exists(".game-compose")):
        print("Existing game compose here. Exiting.")
        return

    fromDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template")
    copy_tree(fromDirectory, "./")
        