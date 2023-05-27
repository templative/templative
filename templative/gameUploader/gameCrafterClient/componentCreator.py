from .. import gameCrafterClient
from os.path import join
import asyncio
from templative.componentInfo import COMPONENT_INFO
from templative.stockComponentInfo import STOCK_COMPONENT_INFO

async def createCustomComponent(gameCrafterSession, componentType, componentFile, cloudGameId, cloudGameFolderId):
    if not componentType in COMPONENT_INFO:
        print("Missing component info for %s." % component["name"])
        return
    component = COMPONENT_INFO[componentType]

    createDeckTask = createDeck
    createTwoSidedSluggedTask = createTwoSidedSlugged
    createTwoSidedBoxTask = createTwoSidedBox
    createTuckBoxTask = createTuckBox
    createTwoSidedTask = createTwoSided
    
    componentTasks = {        
        "DECK": createDeckTask,
        "TWOSIDEDBOX": createTwoSidedBoxTask,
        "TWOSIDEDSLUG": createTwoSidedSluggedTask,
        "TUCKBOX": createTuckBoxTask,
        "TWOSIDED": createTwoSidedTask,
    }

    if not component["GameCrafterUploadTask"] in componentTasks:
        print("Missing component info for %s." % component["name"])
        return
    uploadTask = componentTasks[component["GameCrafterUploadTask"]]
    await uploadTask(gameCrafterSession, componentFile, componentType, cloudGameId, cloudGameFolderId)

async def createStockPart(gameCrafterSession, component, cloudGameId):
    componentName = component["name"]
    componentType = component["type"]
    componentTypeTokens = componentType.split("_")
    isStockComponent = componentTypeTokens[0].upper() == "STOCK" 
    if not isStockComponent:
        print("%s is not a stock part!" % componentName)
        return
    stockPartId = componentTypeTokens[1]
    quantity = component["quantity"]

    if not stockPartId in STOCK_COMPONENT_INFO:
        print("Skipping missing stock component %s." % stockPartId)
        return
    stockComponentInfo = STOCK_COMPONENT_INFO[stockPartId]

    if not "GameCrafterGuid" in stockComponentInfo:
        print("Skipping stock part %s with missing GameCrafterGuid." % stockPartId)
        return
    gameCrafterGuid = stockComponentInfo["GameCrafterGuid"]

    await gameCrafterClient.createStockPart(gameCrafterSession, gameCrafterGuid, quantity, cloudGameId)

async def createTuckBox(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
    frontInstructions = component["frontInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await gameCrafterClient.createFolderAtParent(gameCrafterSession, componentName, cloudGameFolderId)

    imageId = await createFileInFolder(gameCrafterSession, frontInstructions[0]["name"], frontInstructions[0]["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await gameCrafterClient.createTuckBox(gameCrafterSession, componentName, identity, quantity, cloudGameId, imageId)

async def createDeck(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await gameCrafterClient.createFolderAtParent(gameCrafterSession, componentName, cloudGameFolderId)

    tasks = []
    backImageId = await createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await gameCrafterClient.createDeck(gameCrafterSession, componentName, identity, quantity, cloudGameId, backImageId)

    for instructions in frontInstructions:
        tasks.append(asyncio.create_task(createDeckCard(gameCrafterSession, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])))

    for task in tasks:
        await task

async def createDeckCard(gameCrafterSession, instructions, deckId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    if int(quantity) == 0:
        return
    print("Uploading %s" % (filepath))

    cloudFile = await gameCrafterClient.uploadFile(gameCrafterSession, filepath, cloudComponentFolderId)
    pokerCard = await gameCrafterClient.createDeckCard(gameCrafterSession, name, deckId, quantity, cloudFile["id"])


async def createTwoSidedBox(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await gameCrafterClient.createFolderAtParent(gameCrafterSession, componentName, cloudGameFolderId)

    topImageFileId = await createFileInFolder(gameCrafterSession, frontInstructions[0]["name"], frontInstructions[0]["filepath"], cloudComponentFolder["id"])
    bottomImageFileId = await createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])

    cloudTwoSidedBox = await gameCrafterClient.createTwoSidedBox(gameCrafterSession, cloudGameId, componentName, identity, quantity, topImageFileId, bottomImageFileId)

async def createRules(gameCrafterSession, gameRootDirectoryPath, cloudGame, folderId):
    name = "rules"
    filepath = join(gameRootDirectoryPath, "rules.pdf")
    quantity = 1
    print("Uploading %s" % (filepath))

    cloudFile = await gameCrafterClient.uploadFile(gameCrafterSession, filepath, folderId)
    document = await gameCrafterClient.createDownloadableDocument(gameCrafterSession, cloudGame["id"], cloudFile["id"])

async def createFileInFolder(gameCrafterSession, name, filepath, cloudComponentFolderId):
    print("Uploading %s from %s" % (name, filepath))
    cloudFile = await gameCrafterClient.uploadFile(gameCrafterSession, filepath, cloudComponentFolderId)
    return cloudFile["id"]

async def createTwoSided(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
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
    if int(quantity) == 0:
        return
    print("Uploading %s" % (filepath))

    cloudFile = await gameCrafterClient.uploadFile(gameCrafterSession, filepath, cloudComponentFolderId)
    twoSided = await gameCrafterClient.createTwoSided(gameCrafterSession, name, setId, quantity, cloudFile["id"])

async def createTwoSidedSlugged(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
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
    if int(quantity) == 0:
        return
    print("Uploading %s" % (filepath))

    cloudFile = await gameCrafterClient.uploadFile(gameCrafterSession, filepath, cloudComponentFolderId)
    twoSidedSlugged = await gameCrafterClient.createTwoSidedSlugged(gameCrafterSession, name, setId, quantity, cloudFile["id"])