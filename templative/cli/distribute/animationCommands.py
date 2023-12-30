from os import path
from aiofile import AIOFile
import asyncclick as click
from templative.lib.manage.instructionsLoader import getLastOutputFileDirectory
from templative.lib.distribute.animation import packageBuilder, getAnimationDirectory, writeAnimationFile
import json

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

    await packageBuilder.createPackage(input, animationDirectory)
