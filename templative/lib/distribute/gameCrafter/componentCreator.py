import asyncio, os
from templative.lib.distribute.gameCrafter.util import httpOperations
from templative.lib.componentInfo import COMPONENT_INFO
from templative.lib.stockComponentInfo import STOCK_COMPONENT_INFO
from templative.lib.manage import instructionsLoader
from templative.lib.distribute.gameCrafter import fileFolderManager

async def createRules(gameCrafterSession, gameRootDirectoryPath, cloudGame, folderId):
    filepath = os.path.join(gameRootDirectoryPath, "rules.pdf")
    print("Uploading %s" % (filepath))
    cloudFile = await fileFolderManager.postFile(gameCrafterSession, filepath, folderId)
    document = await httpOperations.postDownloadableDocument(gameCrafterSession, cloudGame["id"], cloudFile["id"])

async def createComponents(gameCrafterSession, outputDirectory, cloudGame, cloudGameFolderId, isPublish, isStock, isAsynchronous, isProofed):
    if not outputDirectory:
        raise Exception("outputDirectory cannot be None")

    tasks = []
    for directoryPath in next(os.walk(outputDirectory))[1]:
        componentDirectoryPath = "%s/%s" % (outputDirectory, directoryPath)

        creationTask = asyncio.create_task(createComponent(gameCrafterSession, componentDirectoryPath, cloudGame, cloudGameFolderId, isPublish, isStock, isProofed))

        if isAsynchronous:
            tasks.append(creationTask)
        else:
            await creationTask
            
    res = await asyncio.gather(*tasks, return_exceptions=True)

async def createComponent(gameCrafterSession, componentDirectoryPath, cloudGame, cloudGameFolderId, isPublish, isStock, isProofed):
    if not componentDirectoryPath:
        raise Exception("componentDirectoryPath cannot be None")

    componentFile = await instructionsLoader.loadComponentInstructions(componentDirectoryPath)

    isDebugInfo = False if not "isDebugInfo" in componentFile else componentFile["isDebugInfo"]
    if isDebugInfo and isPublish:
        print("!!! Skipping %s. It is debug only and we are publishing." % (componentFile["name"]))
        return
    
    componentType = componentFile["type"]
    if componentFile["quantity"] == 0:
        print("%s has 0 quantity, skipping." % componentFile["name"])
        return
    
    componentTypeTokens = componentType.split("_")
    isStockComponent = componentTypeTokens[0].upper() == "STOCK" 

    if isStockComponent:
        if not isStock:
            return
        await createStockPart(gameCrafterSession, componentFile, cloudGame["id"])
        return

    await createCustomComponent(gameCrafterSession, componentType, componentFile, cloudGame["id"], cloudGameFolderId, isProofed)
        

async def createCustomComponent(gameCrafterSession, componentType, componentFile, cloudGameId, cloudGameFolderId, isProofed):
    if not componentType in COMPONENT_INFO:
        print("Missing component info for %s." % componentType)
        return
    
    
    component = COMPONENT_INFO[componentType]

    createDeckTask = createDeck
    createTwoSidedSluggedTask = createTwoSidedSlugged
    createTwoSidedBoxTask = createTwoSidedBox
    createTuckBoxTask = createTuckBox
    createTwoSidedTask = createTwoSided
    createCustomPlasticDieTask = createCustomPlasticDie
    createHookboxTask = createHookbox
    createBoxFaceTask = createBoxface
    componentTasks = {        
        "DECK": createDeckTask,
        "TWOSIDEDBOX": createTwoSidedBoxTask,
        "TWOSIDEDSLUG": createTwoSidedSluggedTask,
        "TUCKBOX": createTuckBoxTask,
        "TWOSIDED": createTwoSidedTask,
        "HOOKBOX": createHookboxTask,
        "BOXFACE": createBoxFaceTask,
        "CustomColorD6": createCustomPlasticDieTask,
        "CustomColorD4": createCustomPlasticDieTask,
        "CustomColorD8": createCustomPlasticDieTask,
    }

    if not "GameCrafterUploadTask" in component:
        print("Skipping %s with undefined 'GameCrafterUploadTask'"% componentType)
        return

    if not component["GameCrafterUploadTask"] in componentTasks:
        print("!!! Missing component info for %s." % componentType)
        return
    
    uploadTask = componentTasks[component["GameCrafterUploadTask"]]
    await uploadTask(gameCrafterSession, componentFile, componentType, cloudGameId, cloudGameFolderId, isProofed)

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

async def createTwoSided(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId, isProofed):
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
    cloudPokerDeck = await httpOperations.postTwoSidedSet(gameCrafterSession, componentName, identity, quantity, cloudGameId, backImageId, isProofed)

    for instructions in frontInstructions:
        tasks.append(asyncio.create_task(createTwoSidedPiece(gameCrafterSession, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"], isProofed)))

    res = await asyncio.gather(*tasks, return_exceptions=True)


async def createTwoSidedPiece(gameCrafterSession, instructions, setId, cloudComponentFolderId, isProofed):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    if int(quantity) == 0:
        return
    print("Uploading %s" % (filepath))

    cloudFile = await fileFolderManager.postFile(gameCrafterSession, filepath, cloudComponentFolderId)
    twoSided = await httpOperations.postTwoSided(gameCrafterSession, name, setId, quantity, cloudFile["id"], isProofed)

async def createTwoSidedSlugged(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId, isProofed):
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
    cloudPokerDeck = await httpOperations.postTwoSidedSluggedSet(gameCrafterSession, componentName, identity, quantity, cloudGameId, backImageId, isProofed)

    for instructions in frontInstructions:
        tasks.append(asyncio.create_task(createTwoSidedSluggedPiece(gameCrafterSession, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"], isProofed)))

    res = await asyncio.gather(*tasks, return_exceptions=True)

async def createTwoSidedSluggedPiece(gameCrafterSession, instructions, setId, cloudComponentFolderId, isProofed):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    if int(quantity) == 0:
        return
    print("Uploading %s" % (filepath))

    cloudFile = await fileFolderManager.postFile(gameCrafterSession, filepath, cloudComponentFolderId)
    twoSidedSlugged = await httpOperations.postTwoSidedSlugged(gameCrafterSession, name, setId, quantity, cloudFile["id"], isProofed)

async def createTwoSidedBox(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId, isProofed):
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

    cloudTwoSidedBox = await httpOperations.postTwoSidedBox(gameCrafterSession, cloudGameId, componentName, identity, quantity, topImageFileId, bottomImageFileId, isProofed)


async def createHookbox(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId, isProofed):
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

    cloudHookbox = await httpOperations.postHookBox(gameCrafterSession, cloudGameId, componentName, identity, quantity, topImageFileId, bottomImageFileId, isProofed)


async def createBoxface(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId, isProofed):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
    frontInstructions = component["frontInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await httpOperations.postFolder(gameCrafterSession, componentName, cloudGameFolderId)

    topImageFileId = await fileFolderManager.createFileInFolder(gameCrafterSession, frontInstructions[0]["name"], frontInstructions[0]["filepath"], cloudComponentFolder["id"])

    cloudBoxface = await httpOperations.postBoxFace(gameCrafterSession, cloudGameId, componentName, identity, quantity, topImageFileId, isProofed)


async def createTuckBox(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId, isProofed):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        return
    frontInstructions = component["frontInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await httpOperations.postFolder(gameCrafterSession, componentName, cloudGameFolderId)

    imageId = await fileFolderManager.createFileInFolder(gameCrafterSession, frontInstructions[0]["name"], frontInstructions[0]["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await httpOperations.postTuckBox(gameCrafterSession, componentName, identity, quantity, cloudGameId, imageId, isProofed)

async def createDeck(gameCrafterSession, component, identity, cloudGameId, cloudGameFolderId, isProofed):
    componentName = component["name"]
    quantity = component["quantity"]
    if int(quantity) == 0:
        print(component)
        print("Deck has no quantity, skipping.")
        return
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = await httpOperations.postFolder(gameCrafterSession, componentName, cloudGameFolderId)

    tasks = []
    backImageId = await fileFolderManager.createFileInFolder(gameCrafterSession, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = await httpOperations.postDeck(gameCrafterSession, componentName, identity, quantity, cloudGameId, backImageId, isProofed)

    for instructions in frontInstructions:
        tasks.append(asyncio.create_task(createDeckCard(gameCrafterSession, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"], isProofed)))

    res = await asyncio.gather(*tasks, return_exceptions=True)

async def createDeckCard(gameCrafterSession, instructions, deckId, cloudComponentFolderId, isProofed):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    if int(quantity) == 0:
        return
    print("Uploading %s" % (filepath))

    cloudFile = await fileFolderManager.postFile(gameCrafterSession, filepath, cloudComponentFolderId)
    pokerCard = await httpOperations.postDeckCard(gameCrafterSession, name, deckId, quantity, cloudFile["id"], isProofed)

async def createCustomPlasticDie(gameCrafterSession, componentInstructionsOutput, identity, cloudGameId, cloudGameFolderId, isProofed):
    componentName = componentInstructionsOutput["name"]
    quantity = componentInstructionsOutput["quantity"]
    if int(quantity) == 0:
        return
    dieFaceFilepaths = componentInstructionsOutput["dieFaceFilepaths"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, identity))

    cloudComponentFolder = await httpOperations.postFolder(gameCrafterSession, componentName, cloudGameFolderId)

    imageFileIds = []
    for dieFaceFilepath in dieFaceFilepaths:
        fileId = await fileFolderManager.createFileInFolder(gameCrafterSession, os.path.basename(dieFaceFilepath), dieFaceFilepath, cloudComponentFolder["id"])
        imageFileIds.append(fileId)
    
    dieCreationFunctions = {
        "4": httpOperations.postCustomD4,
        "6": httpOperations.postCustomD6,
        "8": httpOperations.postCustomD8,
    }
    
    if not str(len(dieFaceFilepaths)) in dieCreationFunctions:
        raise Exception("Cannot create %s sided die for %s." % (len(dieFaceFilepaths), componentName))
    
    dieCreationFunction = dieCreationFunctions[str(len(dieFaceFilepaths))]
    await dieCreationFunction(gameCrafterSession,componentName, cloudGameId, quantity, "white", imageFileIds, isProofed)