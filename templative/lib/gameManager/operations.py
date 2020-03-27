import uuid
import os
from datetime import datetime
# from distutils.dir_util import copy_tree

from templative.lib.gameManager import fileLoader
from templative.lib.gameManager import gameWriter
from templative.lib.gameManager import client

def produceGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = fileLoader.loadGame(gameRootDirectoryPath)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    uniqueGameName = ("%s_%s_%s_%s" % (game["name"], game["version"], game["versionName"], timestamp)).replace(" ", "")
    game["name"] = uniqueGameName

    gameCompose = fileLoader.loadGameCompose(gameRootDirectoryPath)

    gameFolderPath = gameWriter.createGameFolder(game["name"], gameCompose["outputDirectory"])
    print("Producing %s" % gameFolderPath)    

    gameWriter.copyGameFromGameFolderToOutput(game, gameFolderPath)

    company = fileLoader.loadCompany(gameRootDirectoryPath)
    gameWriter.copyCompanyFromGameFolderToOutput(company, gameFolderPath)
    
    componentCompose = fileLoader.loadComponentCompose(gameRootDirectoryPath)
    for component in componentCompose["components"]:
        if component["disabled"]:
            print("Skipping disabled %s component." % (component["name"]))
        else:
            client.produceGameComponent(gameRootDirectoryPath, game, gameCompose, component, gameFolderPath)


    rules = fileLoader.loadRules(gameRootDirectoryPath)
    client.produceRulebook(rules, gameFolderPath)
    print("Done producing %s" % gameFolderPath)

    return gameFolderPath

def createTemplate():
    if(os.path.exists(".game-compose")):
        print("Error: Existing game compose here.")
        return

    fromDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template")
    # copy_tree(fromDirectory, "./")