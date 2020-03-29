import os
import json
from aiofile import AIOFile

async def loadGameInstructions(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    async with AIOFile(os.path.join(gameRootDirectoryPath, "game.json")) as game:
        return json.loads(await game.read())

async def loadCompanyInstructions(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path cannot be None")

    async with AIOFile(os.path.join(gameRootDirectoryPath, "company.json")) as company:
        return json.loads(await company.read())

async def loadComponentInstructions(componentDirectoryPath):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    async with AIOFile(os.path.join(componentDirectoryPath, "component.json")) as componentFile:
        return json.loads(await componentFile.read())