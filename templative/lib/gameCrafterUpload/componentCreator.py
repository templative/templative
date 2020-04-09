from .. import gamecrafterclient as gamecrafter
from os.path import isfile, join
import asyncio 

async def createPokerDeck(gameCrafterSession, component, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await gamecrafter.createFolderAtParent(gameCrafterSession, componentName, cloudGameFolderId)
    
    tasks = []
    backImageId = await createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await gamecrafter.createPokerDeck(gameCrafterSession, componentName, quantity, cloudGameId, backImageId)

    for instructions in frontInstructions:
        tasks.append(asyncio.create_task(createPokerCardPiece(gameCrafterSession, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])))
    
    for task in tasks:
        await task

async def createSmallStoutBox(gameCrafterSession, component, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await gamecrafter.createFolderAtParent(gameCrafterSession, componentName, cloudGameFolderId)
    
    topImageFileId = await createFileInFolder(gameCrafterSession, frontInstructions[0]["name"], frontInstructions[0]["filepath"], cloudComponentFolder["id"])
    bottomImageFileId = await createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])

    cloudPokerDeck = await gamecrafter.createSmallStoutBox(gameCrafterSession, cloudGameId, componentName, quantity, topImageFileId, bottomImageFileId)

async def createRules(gameCrafterSession, gameRootDirectoryPath, cloudGame, folderId):
    name = "rules"
    filepath = join(gameRootDirectoryPath, "rules.pdf")
    quantity = 1
    print("Uploading %s" % (filepath))

    cloudFile = await gamecrafter.uploadFile(gameCrafterSession, filepath, folderId)
    document = await gamecrafter.createDocument(gameCrafterSession, name, quantity, cloudGame["id"], cloudFile["id"])

async def createFileInFolder(gameCrafterSession, name, filepath, cloudComponentFolderId):
    print("Uploading %s from %s" % (name, filepath))
    cloudFile = await gamecrafter.uploadFile(gameCrafterSession, filepath, cloudComponentFolderId)
    return cloudFile["id"]

async def createPokerCardPiece(gameCrafterSession, instructions, deckId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    print("Uploading %s" % (filepath))

    cloudFile = await gamecrafter.uploadFile(gameCrafterSession, filepath, cloudComponentFolderId)
    pokerCard = await gamecrafter.createPokerCard(gameCrafterSession, name, deckId, quantity, cloudFile["id"])