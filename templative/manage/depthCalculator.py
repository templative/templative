from templative.manage import defineLoader
from templative.componentInfo import COMPONENT_INFO

async def calculateComponentsDepth(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = await defineLoader.loadGame(gameRootDirectoryPath)
    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)
    studioCompose = await defineLoader.loadStudio(gameRootDirectoryPath)
    componentCompose = await defineLoader.loadComponentCompose(gameRootDirectoryPath)

    print("%s by %s" % (game["displayName"], studioCompose["displayName"]))
    await printGameComponentDepth(gameRootDirectoryPath, gameCompose, componentCompose)

async def printGameComponentDepth(gameRootDirectoryPath, gameCompose, componentCompose):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    depthMillimeters = 0
    for component in componentCompose:
        if str(component["disabled"]) == "True":
            print("Skipping disabled %s component." % (component["name"]))
            continue
        
        if component["type"].startswith("STOCK"):
            print("Skipping stock %s component." % (component["name"]))
            continue
        
        piecesGamedata = await defineLoader.loadPiecesGamedata(gameRootDirectoryPath, gameCompose, component["piecesGamedataFilename"])
        if not piecesGamedata or piecesGamedata == {}:
            print("Skipping %s component due to missing pieces gamedata." % component["name"])
            continue
        
        if not component["type"] in component["type"]:
            print("Missing component info for %s." % component["name"])
            continue

        component = COMPONENT_INFO[component["type"]]
        if not "GameCrafterPackagingDepthMillimeters" in component:
            print("Skipping %s component as we don't have a millimeter measurement for it." % component["name"])
            continue

        depthOfPiece = component["GameCrafterPackagingDepthMillimeters"]
        for piece in piecesGamedata:
            depthMillimeters += int(piece["quantity"]) * depthOfPiece      
    print("%smm" % round(depthMillimeters, 2))