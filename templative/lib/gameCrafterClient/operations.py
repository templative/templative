from templative.lib.gameCrafterClient import client
import os
from uuid import uuid1
from tabulate import tabulate
import asyncio
from aiofile import AIOFile

baseUrl = "https://www.thegamecrafter.com"

async def createGame(clientSession, session, name, designerId):
    game = await client.postGame(clientSession, session, name, designerId)
    
    gameName = game["name"]
    gameId = game["id"]
    editUrl = "%s%s%s" % (baseUrl, "/publish/editor/", gameId)
    print("Created %s. Edit it here %s" % (gameName, editUrl))

    return game

async def createFolderAtRoot(clientSession, session, name):
    user = await client.getUser(clientSession, session)
    return await client.postFolder(clientSession, session, name, user['root_folder_id'])

async def createFolderAtParent(clientSession, session, name, folderId):
    return await client.postFolder(clientSession, session, name, folderId)

async def uploadFile(clientSession, session, filepath, folderId):
    if not os.path.isfile(filepath):
        raise Exception ('Not a file: %s' % filepath)
    
    filename = os.path.basename(filepath)

    with open(filepath, "rb") as fileToUpload:
        return await client.postFile(clientSession, session, fileToUpload, filename, folderId)

async def createPokerDeck(clientSession, session, name, quantity, gameId, imageFileId):
    return await client.postPokerDeck(clientSession, session, name, quantity, gameId, imageFileId)

async def createPokerCard(clientSession, session, name, deckId, quantity, imageFileId):
    return await client.postPokerCard(clientSession, session, name, deckId, quantity, imageFileId)

async def createSmallStoutBox(clientSession, session, gameId, name, quantity, topImageFileId, bottomImageFileId):
    return await client.postSmallStoutBox(clientSession, session, gameId, name, quantity, topImageFileId, bottomImageFileId)

async def createDocument(clientSession, session, name, quantity, gameId, pdfFileId):
    return await client.postDocument(clientSession, session, name, quantity, gameId, pdfFileId)

async def printUser(clientSession, session):
    print(await client.getUser(clientSession, session))

async def listGames(clientSession, session):
    gamesResponse = await client.getGamesForUser(clientSession, session)
    await printGames(gamesResponse["items"])

async def listGamesForUserDesigners(clientSession, session):
    designersResponse = await client.getDesigners(clientSession, session)
    designers = designersResponse["items"]

    games = []
    for designer in designers:
        gamesResponse = await client.getGamesForDesignerId(clientSession, session, designer["id"])
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

async def listDesigners(clientSession, session):
    designersResponse = await client.getDesigners(clientSession, session)

    headers = ["name", "id"]
    data = []
    for designer in designersResponse["items"]:
        print(designer)
        name = designer["name"]
        designerId = designer["id"]
        data.append([name, designerId])

    print(tabulate(data, headers=headers, tablefmt='orgtbl'))

async def login(clientSession):
    publicApiKey = os.environ.get('THEGAMECRAFTER_PUBLIC_KEY')
    if not publicApiKey:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PUBLIC_KEY. Value is %s' % publicApiKey)
    
    userName = os.environ.get('THEGAMECRAFTER_USER')
    if not userName:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_USER. Value is %s' % userName)

    userPassword = os.environ.get('THEGAMECRAFTER_PASSWORD')
    if not userPassword:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PASSWORD. Value is %s' % userPassword)

    return await client.login(clientSession, publicApiKey, userName, userPassword)