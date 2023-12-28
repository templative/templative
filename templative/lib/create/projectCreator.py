from os import path
from distutils.dir_util import copy_tree

async def createProjectInDirectory(directory):
    if(path.exists(path.join(directory, "game-compose.json"))):
        print("This directory already contains a gameExisting game compose here.")
        return 0

    fromDirectory = path.join(path.dirname(path.realpath(__file__)), "template")
    copy_tree(fromDirectory, directory)

    return 1