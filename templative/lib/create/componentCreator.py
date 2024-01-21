from templative.lib.create import templateComponentProjectUpdater
from templative.lib.manage import defineLoader
from templative.lib.componentInfo import COMPONENT_INFO
from templative.lib.stockComponentInfo import STOCK_COMPONENT_INFO
from os.path import join

async def createComponentByType(gameRootDirectoryPath, name, type):
    if type in COMPONENT_INFO:
        await createCustomComponent(gameRootDirectoryPath, name, type)
        return
    
    if type in STOCK_COMPONENT_INFO:
        await createStockComponent(gameRootDirectoryPath, name, type)
        return
    
    print("Skipping %s component as we don't have component info on %s" % (name, type))

async def createCustomComponent(gameRootDirectoryPath, name, type):
    if name == None or name == "":
        print("Must include a name.")
        return
    
    if type == None or type == "":
        raise Exception("Must include a type.")

    if not type in COMPONENT_INFO:
        print("Skipping %s component as we don't have component info on %s" % (name, type))
        return
    componentInfo = COMPONENT_INFO[type]

    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)
    componentComposeData = await defineLoader.loadComponentCompose(gameRootDirectoryPath)
    await templateComponentProjectUpdater.addToComponentCompose(name, type, gameRootDirectoryPath, componentComposeData, componentInfo)

    piecesDirectoryPath = join(gameRootDirectoryPath, gameCompose["piecesGamedataDirectory"])
    componentGamedataDirectoryPath = join(gameRootDirectoryPath, gameCompose["componentGamedataDirectory"])
    artdataDirectoryPath = join(gameRootDirectoryPath, gameCompose["artdataDirectory"])
    artTemplatesDirectoryPath = join(gameRootDirectoryPath, gameCompose["artTemplatesDirectory"])
    if componentInfo["HasPieceData"]:
        await templateComponentProjectUpdater.createPiecesJson(piecesDirectoryPath, name, hasPieceQuantity=componentInfo["HasPieceQuantity"])

    await templateComponentProjectUpdater.createComponentJson(componentGamedataDirectoryPath, name)
    await templateComponentProjectUpdater.createArtDataFiles(artdataDirectoryPath, name, componentInfo["ArtDataTypeNames"])
    await templateComponentProjectUpdater.createArtFiles(artTemplatesDirectoryPath, name, type, componentInfo["ArtDataTypeNames"])

async def createStockComponent(gameRootDirectoryPath, name, stockPartId):
    if name == None or name == "":
        print("Must include a name.")
        return
    
    if stockPartId == None or stockPartId == "":
        raise Exception("Must include a type.")
    
    if not stockPartId in STOCK_COMPONENT_INFO:
        print("Skipping %s component as we don't have component info on %s" % (name, stockPartId))
        return
    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)
    componentComposeData = await defineLoader.loadComponentCompose(gameRootDirectoryPath)
    await templateComponentProjectUpdater.addStockComponentToComponentCompose(name, stockPartId, gameRootDirectoryPath, componentComposeData)


