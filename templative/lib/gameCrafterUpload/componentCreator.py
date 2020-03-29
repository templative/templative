from templative.lib.gameCrafterClient import operations as gamecrafter
from os.path import isfile, join
import asyncio 

async def createPokerDeck(client, session, component, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await gamecrafter.createFolderAtParent(client, session, componentName, cloudGameFolderId)
    
    backImageId = await createFileInFolder(client, session, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await gamecrafter.createPokerDeck(client, session, componentName, quantity, cloudGameId, backImageId)

    for instructions in frontInstructions:
        await createPokerCardPiece(client, session, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])

async def createSmallStoutBox(client, session, component, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await gamecrafter.createFolderAtParent(client, session, componentName, cloudGameFolderId)
    topImageFileId = await createFileInFolder(client, session, frontInstructions[0]["name"], frontInstructions[0]["filepath"], cloudComponentFolder["id"])
    bottomImageFileId = await createFileInFolder(client, session, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])

    cloudPokerDeck = await gamecrafter.createSmallStoutBox(client, session, cloudGameId, componentName, quantity, topImageFileId, bottomImageFileId)

async def createRules(client, session, gameRootDirectoryPath, cloudGame, folderId):
    name = "rules"
    filepath = join(gameRootDirectoryPath, "rules.pdf")
    quantity = 1
    print("Uploading %s" % (filepath))

    cloudFile = await gamecrafter.uploadFile(client, session, filepath, folderId)
    document = await gamecrafter.createDocument(client, session, name, quantity, cloudGame["id"], cloudFile["id"])

async def createFileInFolder(client, session, name, filepath, cloudComponentFolderId):
    print("Uploading %s from %s" % (name, filepath))
    cloudFile = await gamecrafter.uploadFile(client, session, filepath, cloudComponentFolderId)
    return cloudFile["id"]

async def createPokerCardPiece(client, session, instructions, deckId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    print("Uploading %s" % (filepath))

    cloudFile = await gamecrafter.uploadFile(client, session, filepath, cloudComponentFolderId)
    pokerCard = await gamecrafter.createPokerCard(client, session, name, deckId, quantity, cloudFile["id"])