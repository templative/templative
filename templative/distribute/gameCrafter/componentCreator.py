import asyncio, os
from templative.distribute.gameCrafter.util import httpOperations
from templative.componentInfo import COMPONENT_INFO
from templative.stockComponentInfo import STOCK_COMPONENT_INFO
from templative.manage import instructionsLoader
from templative.distribute.gameCrafter import fileFolderManager

async def createRules(gameCrafterSession, gameRootDirectoryPath, cloudGame, folderId):
    filepath = os.path.join(gameRootDirectoryPath, "rules.pdf")
    print("Uploading %s" % (filepath))
    cloudFile = await fileFolderManager.postFile(gameCrafterSession, filepath, folderId)
    document = await httpOperations.postDownloadableDocument(gameCrafterSession, cloudGame["id"], cloudFile["id"])

async def createComponents(gameCrafterSession, outputDirectory, cloudGame, cloudGameFolderId, isPublish):
    if not outputDirectory:
        raise Exception("outputDirectory cannot be None")

    tasks = []
    for directoryPath in next(os.walk(outputDirectory))[1]:
        componentDirectoryPath = "%s/%s" % (outputDirectory, directoryPath)
        tasks.append(asyncio.create_task(createComponent(gameCrafterSession, componentDirectoryPath, cloudGame, cloudGameFolderId, isPublish)))

    res = await asyncio.gather(*tasks, return_exceptions=True)

async def createComponent(gameCrafterSession, componentDirectoryPath, cloudGame, cloudGameFolderId, isPublish):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    componentFile = await instructionsLoader.loadComponentInstructions(componentDirectoryPath)

    isDebugInfo = False if not "isDebugInfo" in componentFile else componentFile["isDebugInfo"]
    if isDebugInfo and isPublish:
        print("!!! Skipping %s. It is debug only and we are publishing." % (componentFile["name"]))
        return

    componentType = componentFile["type"]
    if componentFile["quantity"] == 0:
        return
    
    componentTypeTokens = componentType.split("_")
    isStockComponent = componentTypeTokens[0].upper() == "STOCK" 

    if isStockComponent:
        await createStockPart(gameCrafterSession, componentFile, cloudGame["id"])
        return

    await createCustomComponent(gameCrafterSession, componentType, componentFile, cloudGame["id"], cloudGameFolderId)
        

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
        "D4Plastic": createCustomPlasticDie,
        "D6Plastic": createCustomPlasticDie,
        "D8Plastic": createCustomPlasticDie,
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

    await httpOperations.postStockPart(gameCrafterSession, gameCrafterGuid, quantity, cloudGameId)

async def createTwoSided(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, identity))

    cloudComponentFolder = await httpOperations.postFolder(gameCrafterSession, componentName, cloudGameFolderId)

    tasks = []
    backImageId = await fileFolderManager.createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await httpOperations.postTwoSidedSet(gameCrafterSession, componentName, identity, quantity, cloudGameId, backImageId)

    for instructions in frontInstructions:
        tasks.append(asyncio.create_task(createTwoSidedPiece(gameCrafterSession, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])))

    res = await asyncio.gather(*tasks, return_exceptions=True)

async def createTwoSidedPiece(gameCrafterSession, instructions, setId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    if int(quantity) == 0:
        return
    print("Uploading %s" % (filepath))

    cloudFile = await fileFolderManager.postFile(gameCrafterSession, filepath, cloudComponentFolderId)
    twoSided = await httpOperations.postTwoSided(gameCrafterSession, name, setId, quantity, cloudFile["id"])

async def createTwoSidedSlugged(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, identity))

    cloudComponentFolder = await httpOperations.postFolder(gameCrafterSession, componentName, cloudGameFolderId)

    tasks = []
    backImageId = await fileFolderManager.createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await httpOperations.postTwoSidedSluggedSet(gameCrafterSession, componentName, identity, quantity, cloudGameId, backImageId)

    for instructions in frontInstructions:
        tasks.append(asyncio.create_task(createTwoSidedSluggedPiece(gameCrafterSession, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])))

    res = await asyncio.gather(*tasks, return_exceptions=True)

async def createTwoSidedSluggedPiece(gameCrafterSession, instructions, setId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    if int(quantity) == 0:
        return
    print("Uploading %s" % (filepath))

    cloudFile = await fileFolderManager.postFile(gameCrafterSession, filepath, cloudComponentFolderId)
    twoSidedSlugged = await httpOperations.postTwoSidedSlugged(gameCrafterSession, name, setId, quantity, cloudFile["id"])

async def createTwoSidedBox(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await httpOperations.postFolder(gameCrafterSession, componentName, cloudGameFolderId)

    topImageFileId = await fileFolderManager.createFileInFolder(gameCrafterSession, frontInstructions[0]["name"], frontInstructions[0]["filepath"], cloudComponentFolder["id"])
    bottomImageFileId = await fileFolderManager.createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])

    cloudTwoSidedBox = await httpOperations.postTwoSidedBox(gameCrafterSession, cloudGameId, componentName, identity, quantity, topImageFileId, bottomImageFileId)

async def createTuckBox(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
    frontInstructions = component["frontInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await httpOperations.postFolder(gameCrafterSession, componentName, cloudGameFolderId)

    imageId = await fileFolderManager.createFileInFolder(gameCrafterSession, frontInstructions[0]["name"], frontInstructions[0]["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await httpOperations.postTuckBox(gameCrafterSession, componentName, identity, quantity, cloudGameId, imageId)

async def createDeck(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await httpOperations.postFolder(gameCrafterSession, componentName, cloudGameFolderId)

    tasks = []
    backImageId = await fileFolderManager.createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await httpOperations.postDeck(gameCrafterSession, componentName, identity, quantity, cloudGameId, backImageId)

    for instructions in frontInstructions:
        tasks.append(asyncio.create_task(createDeckCard(gameCrafterSession, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])))

    res = await asyncio.gather(*tasks, return_exceptions=True)

async def createDeckCard(gameCrafterSession, instructions, deckId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    if int(quantity) == 0:
        return
    print("Uploading %s" % (filepath))

    cloudFile = await fileFolderManager.postFile(gameCrafterSession, filepath, cloudComponentFolderId)
    pokerCard = await httpOperations.postDeckCard(gameCrafterSession, name, deckId, quantity, cloudFile["id"])

async def createCustomPlasticDie(gameCrafterSession, componentInstructionsOutput, identity, cloudGameId, cloudGameFolderId):
    componentName = componentInstructionsOutput["name"]
    quantity = componentInstructionsOutput["quantity"]
    if int(quantity) == 0:
        return
    sideInstructions = componentInstructionsOutput["sideInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, identity))

    cloudComponentFolder = await httpOperations.postFolder(gameCrafterSession, componentName, cloudGameFolderId)

    imageFileIds = []
    for sideInstruction in sideInstructions:
        imageFileIds.append(await fileFolderManager.createFileInFolder(gameCrafterSession, sideInstruction["name"], sideInstruction["filepath"], cloudComponentFolder["id"])
    )
    dieCreationFunctions = {
        "4": httpOperations.postCustomD4,
        "6": httpOperations.postCustomD6,
        "8": httpOperations.postCustomD8,
    }
    
    if not str(len(sideInstructions)) in dieCreationFunctions:
        raise Exception("Cannot create %s sided die for %s." % (len(sideInstructions), componentName))
    
    dieCreationFunction = dieCreationFunctions[str(len(sideInstructions))]
    dieId = await dieCreationFunction(gameCrafterSession, cloudGameId, componentName, quantity, componentInstructionsOutput["color"], imageFileIds)