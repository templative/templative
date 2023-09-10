from templative.create import templateComponentProjectUpdater
from templative.manage import defineLoader
from templative.componentInfo import COMPONENT_INFO

async def createCustomComponent(name, type):

    if name == None or name == "":
        print("Must include a name.")
        return
    
    if type == None or type == "":
        raise Exception("Must include a type.")

    if not type in COMPONENT_INFO:
        print("Skipping %s component as we don't have component info on %ss" % (name, type))
        return
    componentInfo = COMPONENT_INFO[type]

    gameRootDirectoryPath = "."
    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)
    componentComposeData = await defineLoader.loadComponentCompose(gameRootDirectoryPath)
    await templateComponentProjectUpdater.addToComponentCompose(name, type, gameRootDirectoryPath, componentComposeData, componentInfo)

    if componentInfo["HasPieceData"]:
        await templateComponentProjectUpdater.createPiecesCsv(gameCompose["piecesGamedataDirectory"], name, hasPieceQuantity=True)

    await templateComponentProjectUpdater.createComponentJson(gameCompose["componentGamedataDirectory"], name)
    await templateComponentProjectUpdater.createArtDataFiles(gameCompose["artdataDirectory"], name, componentInfo["ArtDataTypeNames"])
    await templateComponentProjectUpdater.createArtFiles(gameCompose["artTemplatesDirectory"], name, type, componentInfo["ArtDataTypeNames"])

async def createStockComponent(name, stockPartId):
    gameRootDirectoryPath = "."
    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)
    componentComposeData = await defineLoader.loadComponentCompose(gameRootDirectoryPath)
    await templateComponentProjectUpdater.addStockComponentToComponentCompose(name, stockPartId, gameRootDirectoryPath, componentComposeData)
    await templateComponentProjectUpdater.createComponentJson(gameCompose["componentGamedataDirectory"], name)


