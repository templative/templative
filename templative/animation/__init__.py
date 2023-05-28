from os import path
from aiofile import AIOFile
import asyncclick as click
from templative.gameManager.instructionsLoader import getLastOutputFileDirectory
from .packageBuilder import createPackage

@click.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
@click.option('-o', '--output', default=None, help='The output directory.')
async def animation(input, output):
    """Create a typescript module for your board game."""
    if input is None:
        input = await getLastOutputFileDirectory()

    animationDirectory = await getAnimationDirectory(output)
    if animationDirectory == None:
        print("Missing --output directory.")
        return
    await writeAnimationFile(animationDirectory)

    await createPackage(input, animationDirectory)

async def lookForAnimationFile():
    animationFileLocation = "./.animation"
    if not path.exists(animationFileLocation):
        return None
    
    async with AIOFile(animationFileLocation, mode="r") as animation:
        return await animation.read()
    
async def writeAnimationFile(outputPath):
    animationFileLocation = path.join("./", ".animation")
    async with AIOFile(animationFileLocation, mode="w") as animation:
        await animation.write(outputPath)

async def getAnimationDirectory(inputedAnimationDirectory):
    if inputedAnimationDirectory != None:
        return inputedAnimationDirectory
    
    return await lookForAnimationFile()  