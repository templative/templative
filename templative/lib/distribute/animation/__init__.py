from os import path
from aiofile import AIOFile

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