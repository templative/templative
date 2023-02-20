from .. import gameCrafterClient
from os.path import join
import asyncio

async def createTuckBox(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    frontInstructions = component["frontInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await gameCrafterClient.createFolderAtParent(gameCrafterSession, componentName, cloudGameFolderId)

    imageId = await createFileInFolder(gameCrafterSession, frontInstructions[0]["name"], frontInstructions[0]["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await gameCrafterClient.createTuckBox(gameCrafterSession, componentName, identity, quantity, cloudGameId, imageId)

async def createPokerDeck(gameCrafterSession, component, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await gameCrafterClient.createFolderAtParent(gameCrafterSession, componentName, cloudGameFolderId)

    tasks = []
    backImageId = await createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await gameCrafterClient.createPokerDeck(gameCrafterSession, componentName, quantity, cloudGameId, backImageId)

    for instructions in frontInstructions:
        tasks.append(asyncio.create_task(createPokerCardPiece(gameCrafterSession, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])))

    for task in tasks:
        await task

async def createPokerCardPiece(gameCrafterSession, instructions, deckId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    print("Uploading %s" % (filepath))

    cloudFile = await gameCrafterClient.uploadFile(gameCrafterSession, filepath, cloudComponentFolderId)
    pokerCard = await gameCrafterClient.createPokerCard(gameCrafterSession, name, deckId, quantity, cloudFile["id"])


async def createSmallStoutBox(gameCrafterSession, component, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await gameCrafterClient.createFolderAtParent(gameCrafterSession, componentName, cloudGameFolderId)

    topImageFileId = await createFileInFolder(gameCrafterSession, frontInstructions[0]["name"], frontInstructions[0]["filepath"], cloudComponentFolder["id"])
    bottomImageFileId = await createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])

    cloudSmallStoutBox = await gameCrafterClient.createSmallStoutBox(gameCrafterSession, cloudGameId, componentName, quantity, topImageFileId, bottomImageFileId)

async def createRules(gameCrafterSession, gameRootDirectoryPath, cloudGame, folderId):
    name = "rules"
    filepath = join(gameRootDirectoryPath, "rules.pdf")
    quantity = 1
    print("Uploading %s" % (filepath))

    cloudFile = await gameCrafterClient.uploadFile(gameCrafterSession, filepath, folderId)
    document = await gameCrafterClient.createDocument(gameCrafterSession, name, quantity, cloudGame["id"], cloudFile["id"])

async def createFileInFolder(gameCrafterSession, name, filepath, cloudComponentFolderId):
    print("Uploading %s from %s" % (name, filepath))
    cloudFile = await gameCrafterClient.uploadFile(gameCrafterSession, filepath, cloudComponentFolderId)
    return cloudFile["id"]




async def createTwoSided(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, identity))

    cloudComponentFolder = await gameCrafterClient.createFolderAtParent(gameCrafterSession, componentName, cloudGameFolderId)

    tasks = []
    backImageId = await createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await gameCrafterClient.createTwoSidedSet(gameCrafterSession, componentName, identity, quantity, cloudGameId, backImageId)

    for instructions in frontInstructions:
        tasks.append(asyncio.create_task(createTwoSidedPiece(gameCrafterSession, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])))

    for task in tasks:
        await task

async def createTwoSidedPiece(gameCrafterSession, instructions, setId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    print("Uploading %s" % (filepath))

    cloudFile = await gameCrafterClient.uploadFile(gameCrafterSession, filepath, cloudComponentFolderId)
    twoSided = await gameCrafterClient.createTwoSided(gameCrafterSession, name, setId, quantity, cloudFile["id"])

async def createTwoSidedSlugged(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, identity))

    cloudComponentFolder = await gameCrafterClient.createFolderAtParent(gameCrafterSession, componentName, cloudGameFolderId)

    tasks = []
    backImageId = await createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await gameCrafterClient.createTwoSidedSluggedSet(gameCrafterSession, componentName, identity, quantity, cloudGameId, backImageId)

    for instructions in frontInstructions:
        tasks.append(asyncio.create_task(createTwoSidedSluggedPiece(gameCrafterSession, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])))

    for task in tasks:
        await task

async def createTwoSidedSluggedPiece(gameCrafterSession, instructions, setId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    print("Uploading %s" % (filepath))

    cloudFile = await gameCrafterClient.uploadFile(gameCrafterSession, filepath, cloudComponentFolderId)
    twoSidedSlugged = await gameCrafterClient.createTwoSidedSlugged(gameCrafterSession, name, setId, quantity, cloudFile["id"])