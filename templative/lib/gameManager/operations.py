import threading
import multiprocessing
import uuid
import os
import asyncio
from datetime import datetime
# from distutils.dir_util import copy_tree

from templative.lib.gameManager import fileLoader
from templative.lib.gameManager import gameWriter
from templative.lib.gameManager import client

async def produceGame(gameRootDirectoryPath, componentName):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    isExclusivelyComponent = componentName != None
    game = await fileLoader.loadGame(gameRootDirectoryPath)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    uniqueGameName = ("%s_%s_%s_%s" % (game["name"], game["version"], game["versionName"], timestamp)).replace(" ", "")
    game["name"] = uniqueGameName

    gameCompose = await fileLoader.loadGameCompose(gameRootDirectoryPath)

    gameFolderPath = await gameWriter.createGameFolder(game["name"], gameCompose["outputDirectory"])
    print("Producing %s" % gameFolderPath)    

    await gameWriter.copyGameFromGameFolderToOutput(game, gameFolderPath)

    company = await fileLoader.loadCompany(gameRootDirectoryPath)
    await gameWriter.copyCompanyFromGameFolderToOutput(company, gameFolderPath)
    
    componentCompose = await fileLoader.loadComponentCompose(gameRootDirectoryPath)
    threads = []
    for component in componentCompose["components"]:
        if not isExclusivelyComponent and component["disabled"]:
            print("Skipping disabled %s component." % (component["name"]))
        elif isExclusivelyComponent and component["name"] != componentName:
            print("Skipping %s component." % (component["name"]))
        else:
            threads.append(multiprocessing.Process(await client.produceGameComponent(gameRootDirectoryPath, game, gameCompose, component, gameFolderPath)))

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

    rules = await fileLoader.loadRules(gameRootDirectoryPath)
    await client.produceRulebook(rules, gameFolderPath)
    print("Done producing %s" % gameFolderPath)

    return gameFolderPath

async def createTemplate():
    if(os.path.exists(".game-compose")):
        print("Error: Existing game compose here.")
        return

    fromDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template")
    # copy_tree(fromDirectory, "./")