import asyncio
from tabulate import tabulate
from templative.distribute.gameCrafter.util import httpOperations

async def printUser(gameCrafterSession):
    print(await httpOperations.getUser(gameCrafterSession))

async def listGames(gameCrafterSession):
    gamesResponse = await httpOperations.getGamesForUser(gameCrafterSession)
    await printGames(gamesResponse["items"])

async def deletePageOfGames(gameCrafterSession):
    gamesResponse = await httpOperations.getGamesForUser(gameCrafterSession)
    deleted = ""
    tasks = []
    for game in gamesResponse["items"]:
        deleted = deleted + game["name"] + " "
        asyncio.create_task((httpOperations.deleteGame(gameCrafterSession, game["id"])))
    res = await asyncio.gather(*tasks, return_exceptions=True)

async def listGamesForUserDesigners(gameCrafterSession):
    designersResponse = await httpOperations.getDesigners(gameCrafterSession)
    designers = designersResponse["items"]

    games = []
    for designer in designers:
        gamesResponse = await httpOperations.getGamesForDesignerId(gameCrafterSession, designer["id"])
        games.extend(gamesResponse["items"])

    printGames(games)

async def printGames(games):
    headers = ["name", "skuId", "link"]
    data = []

    for game in games:
        gameName = game["name"]
        skuId = game["sku_id"]
        gameLink = "https://www.thegamecrafter.com" + game["edit_uri"]
        data.append([gameName, skuId, gameLink])

    print(tabulate(data, headers=headers, tablefmt='orgtbl'))

async def listDesigners(gameCrafterSession):
    designersResponse = await httpOperations.getDesigners(gameCrafterSession)

    headers = ["name", "id"]
    data = []
    for designer in designersResponse["items"]:
        print(designer)
        name = designer["name"]
        designerId = designer["id"]
        data.append([name, designerId])

    print(tabulate(data, headers=headers, tablefmt='orgtbl'))
