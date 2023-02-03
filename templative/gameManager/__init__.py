from os import path
# from distutils.dir_util import copy_tree

from . import componentProcessor

async def produceGame(gameRootDirectoryPath):
    return await componentProcessor.produceGame(gameRootDirectoryPath)

async def listComponents(gameRootDirectoryPath):
    await componentProcessor.listComponents(gameRootDirectoryPath)

async def createTemplate():
    if(path.exists(".game-compose")):
        print("Error: Existing game compose here.")
        return

    fromDirectory = path.join(path.dirname(path.realpath(__file__)), "template")
    # copy_tree(fromDirectory, "./")