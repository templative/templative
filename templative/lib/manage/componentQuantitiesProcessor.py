from templative.lib.manage import defineLoader

async def listComponentQuantities(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = await defineLoader.loadGame(gameRootDirectoryPath)
    gameCompose = await defineLoader.loadGameCompose(gameRootDirectoryPath)
    studioCompose = await defineLoader.loadStudio(gameRootDirectoryPath)
    componentCompose = await defineLoader.loadComponentCompose(gameRootDirectoryPath)

    print("%s by %s" % (game["displayName"], studioCompose["displayName"]))
    await printGameComponentQuantities(gameRootDirectoryPath, gameCompose, componentCompose)


async def printGameComponentQuantities(gameRootDirectoryPath, gameCompose, componentCompose):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    componentQuantities ={"Document": [{ "name":"Rules", "componentQuantity": 1, "pieceQuantity": 1}]}
    for component in componentCompose:
        if str(component["disabled"]) == "True":
            print("Skipping disabled %s component." % (component["name"]))
            continue
        
        if component["type"].startswith("STOCK"):
            await addStockComponentQuantities(componentQuantities, component)
            continue
        
        piecesGamedata = await defineLoader.loadPiecesGamedata(gameRootDirectoryPath, gameCompose, component["piecesGamedataFilename"])
        if not piecesGamedata or piecesGamedata == {}:
            print("Skipping %s component due to missing pieces gamedata." % component["name"])
            continue
        await addComponentQuantities(componentQuantities, component, piecesGamedata)
        
    message = ""
    for componentType in componentQuantities:
        componentExplanations = ""
        componentQuantity = 0
        for explanation in componentQuantities[componentType]:
            quantity = explanation["componentQuantity"] * explanation["pieceQuantity"]
            componentQuantity += quantity
            componentExplanations = "%s\n    %sx %s" % (componentExplanations, quantity, explanation["name"])
        message = "%s\n%sx %s Pieces: %s" % (message, componentQuantity, componentType, componentExplanations)
        
    print(message)


async def addStockComponentQuantities(componentQuantities, component):
    if not component["type"] in componentQuantities:
        componentQuantities[component["type"]] = []

    componentQuantities[component["type"]].append({
        "name": component["name"], "componentQuantity": component["quantity"], "pieceQuantity": 1
    })

async def addComponentQuantities(componentQuantities, component, piecesGamedata):
    if not component["type"] in componentQuantities:
        componentQuantities[component["type"]] = []

    quantity = 0
    for piece in piecesGamedata:
        if not "quantity" in piece:
            continue
        quantity += int(piece["quantity"])
    
    componentQuantities[component["type"]].append({
        "name":component["name"], "componentQuantity": component["quantity"], "pieceQuantity": quantity
    })