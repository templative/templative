from os import path
from distutils.dir_util import copy_tree
import asyncclick as click
from .instructionsLoader import getLastOutputFileDirectory
from . import componentProcessor

@click.command()
async def init():
    """Create the default game project here"""
    if(path.exists("./game-compose.json")):
        print("This directory already contains a gameExisting game compose here.")
        return

    fromDirectory = path.join(path.dirname(path.realpath(__file__)), "template")
    copy_tree(fromDirectory, "./")

@click.command()
@click.option('--name', default=None, help='The component to produce.')
@click.option('-s/-c', '--simple/--complex', default=False, required=False, type=bool, help='Whether complex information is shown. Used for videos.')
@click.option('-p/-d', '--publish/--debug', default=False, required=False, type=bool, help='Where debug information is included.')
@click.option('--input', default="./", required=False, help='The directory of the templative project.')
async def produce(name, simple, publish, input):
    """Produce the game in the current directory"""
    return await componentProcessor.produceGame(input, name, simple, publish)

@click.command()
@click.option('--input', default="./", required=False, help='The directory of the templative project.')
async def components(input):
    """Get a list of quantities of the game in the current directory"""
    await componentProcessor.listComponents(input)

@click.command()
@click.option('--input', default="./", required=False, help='The directory of the templative project.')
async def depth(input):
    """Get the depth of all components"""
    await componentProcessor.calculateComponentsDepth(input)

async def createComponent(name, type):
    if name == None:
        print("Missing --name.")
        return
    
    await componentProcessor.createComponent(name, type)

async def createStockComponent(name, stockPartId):
    if name == None:
        print("Missing name.")
        return
    
    if stockPartId == None:
        print("Missing stockPartId.")
        return
    
    await componentProcessor.createStockComponent(name, stockPartId)