import os
import asyncio
from uuid import uuid1
from tabulate import tabulate
from aiofile import AIOFile
import aiohttp

from . import client
from .gameCrafterSession import GameCrafterSession

baseUrl = "https://www.thegamecrafter.com"

async def createGame(gameCrafterSession, name, designerId):
    game = await client.postGame(gameCrafterSession, name, designerId)
    
    gameName = game["name"]
    gameId = game["id"]
    editUrl = "%s%s%s" % (baseUrl, "/publish/editor/", gameId)
    print("Created %s. Edit it here %s" % (gameName, editUrl))

    return game

async def createFolderAtRoot(gameCrafterSession, name):
    user = await client.getUser(gameCrafterSession)
    return await client.postFolder(gameCrafterSession, name, user['root_folder_id'])

async def createFolderAtParent(gameCrafterSession, name, folderId):
    return await client.postFolder(gameCrafterSession, name, folderId)

async def uploadFile(gameCrafterSession, filepath, folderId):
    if not os.path.isfile(filepath):
        raise Exception ('Not a file: %s' % filepath)
    
    filename = os.path.basename(filepath)

    with open(filepath, "rb") as fileToUpload:
        return await client.postFile(gameCrafterSession, fileToUpload, filename, folderId)

async def createPokerDeck(gameCrafterSession, name, quantity, gameId, imageFileId):
    return await client.postPokerDeck(gameCrafterSession, name, quantity, gameId, imageFileId)

async def createPokerCard(gameCrafterSession, name, deckId, quantity, imageFileId):
    return await client.postPokerCard(gameCrafterSession, name, deckId, quantity, imageFileId)

async def createSmallStoutBox(gameCrafterSession, gameId, name, quantity, topImageFileId, bottomImageFileId):
    return await client.postSmallStoutBox(gameCrafterSession, gameId, name, quantity, topImageFileId, bottomImageFileId)

async def createDocument(gameCrafterSession, name, quantity, gameId, pdfFileId):
    return await client.postDocument(gameCrafterSession, name, quantity, gameId, pdfFileId)

async def printUser(gameCrafterSession):
    print(await client.getUser(gameCrafterSession))

async def listGames(gameCrafterSession):
    gamesResponse = await client.getGamesForUser(gameCrafterSession)
    await printGames(gamesResponse["items"])

async def listGamesForUserDesigners(gameCrafterSession):
    designersResponse = await client.getDesigners(gameCrafterSession)
    designers = designersResponse["items"]

    games = []
    for designer in designers:
        gamesResponse = await client.getGamesForDesignerId(gameCrafterSession, designer["id"])
        games.extend(gamesResponse["items"])

    printGames(games)   

async def printGames(clientSession, games):
    headers = ["name", "id", "link"]
    data = []

    for game in games:
        gameName = game["name"]
        gameId = game["id"]
        gameLink = os.path.join(baseUrl, game["edit_uri"])
        data.append([gameName, gameId, gameLink])

    print(tabulate(data, headers=headers, tablefmt='orgtbl'))

async def listDesigners(gameCrafterSession):
    designersResponse = await client.getDesigners(gameCrafterSession)

    headers = ["name", "id"]
    data = []
    for designer in designersResponse["items"]:
        print(designer)
        name = designer["name"]
        designerId = designer["id"]
        data.append([name, designerId])

    print(tabulate(data, headers=headers, tablefmt='orgtbl'))

async def login():
    
    publicApiKey = os.environ.get('THEGAMECRAFTER_PUBLIC_KEY')
    if not publicApiKey:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PUBLIC_KEY. Value is %s' % publicApiKey)
    
    userName = os.environ.get('THEGAMECRAFTER_USER')
    if not userName:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_USER. Value is %s' % userName)

    userPassword = os.environ.get('THEGAMECRAFTER_PASSWORD')
    if not userPassword:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PASSWORD. Value is %s' % userPassword)
    
    gameCrafterSession = GameCrafterSession(aiohttp.ClientSession())
    login = await client.login(gameCrafterSession, publicApiKey, userName, userPassword)
    gameCrafterSession.login(sessionId=login["id"], userId=login["user_id"])
    return gameCrafterSession

async def logout(gameCrafterSession):
    await client.logout(gameCrafterSession)