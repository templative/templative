import os
from tabulate import tabulate
import aiohttp

from . import gameCrafterOperations
from .gameCrafterSession import GameCrafterSession

baseUrl = "https://www.thegamecrafter.com"

async def createGame(gameCrafterSession, gameInfo, designerId, isPublish):
    gameName = gameInfo["displayName"] if isPublish else gameInfo["name"]
    uploadedGame = await gameCrafterOperations.postGame(gameCrafterSession, gameName, designerId)
    gameId = uploadedGame["id"]
    editUrl = "%s%s%s" % (baseUrl, "/make/games/", gameId)
    print("Created %s. Edit it here %s" % (gameName, editUrl))

    return uploadedGame

advertismentImages = [
    "C:/Users/User/Documents/git/nextdaygames/templative/templative/gameUploader/gameCrafterClient/testImages/actionShot.png",
    "C:/Users/User/Documents/git/nextdaygames/templative/templative/gameUploader/gameCrafterClient/testImages/advertisment.png",
    "C:/Users/User/Documents/git/nextdaygames/templative/templative/gameUploader/gameCrafterClient/testImages/backdrop.png",
    "C:/Users/User/Documents/git/nextdaygames/templative/templative/gameUploader/gameCrafterClient/testImages/logo.png"
]

async def createAdvertisementImages(gameCrafterSession):
    folder = await createFolderAtRoot(gameCrafterSession, "AdvertisementImages")
    
    for filepath in advertismentImages:
        print(filepath)
        file = await uploadFile(gameCrafterSession, filepath, folder["id"])
        print(filepath, file["id"])

async def createActionShot(gameCrafterSession, gameId):
    await gameCrafterOperations.createActionShot(gameCrafterSession, gameId)

async def createFolderAtRoot(gameCrafterSession, name):
    user = await gameCrafterOperations.getUser(gameCrafterSession)
    return await gameCrafterOperations.postFolder(gameCrafterSession, name, user['root_folder_id'])

async def createFolderAtParent(gameCrafterSession, name, folderId):
    return await gameCrafterOperations.postFolder(gameCrafterSession, name, folderId)

async def uploadFile(gameCrafterSession, filepath, folderId):
    if not os.path.isfile(filepath):
        raise Exception ('Not a file: %s' % filepath)

    filename = os.path.basename(filepath)

    with open(filepath, "rb") as fileToUpload:
        return await gameCrafterOperations.postFile(gameCrafterSession, fileToUpload, filename, folderId)

async def createStockPart(gameCrafterSession, stockPartId, quantity, gameId):
    return await gameCrafterOperations.postStockPart(gameCrafterSession, stockPartId, quantity, gameId)

async def createDeck(gameCrafterSession, name, identity, quantity, gameId, imageFileId):
    return await gameCrafterOperations.postDeck(gameCrafterSession, name, identity, quantity, gameId, imageFileId)

async def createDeckCard(gameCrafterSession, name, deckId, quantity, imageFileId):
    return await gameCrafterOperations.postDeckCard(gameCrafterSession, name, deckId, quantity, imageFileId)

async def createTwoSidedSluggedSet(gameCrafterSession, name, identity, quantity, gameId, backImageFileId):
    return await gameCrafterOperations.postTwoSidedSluggedSet(gameCrafterSession, name, identity, quantity, gameId, backImageFileId)

async def createTwoSidedSlugged(gameCrafterSession, name, setId, quantity, imageFileId):
    return await gameCrafterOperations.postTwoSidedSlugged(gameCrafterSession, name, setId, quantity, imageFileId)

async def createTwoSidedBox(gameCrafterSession, gameId, name, identity, quantity, topImageFileId, bottomImageFileId):
    return await gameCrafterOperations.postTwoSidedBox(gameCrafterSession, gameId, name, identity, quantity, topImageFileId, bottomImageFileId)

async def createDocument(gameCrafterSession, name, quantity, gameId, pdfFileId):
    return await gameCrafterOperations.postDocument(gameCrafterSession, name, quantity, gameId, pdfFileId)

async def createDownloadableDocument(gameCrafterSession, gameId, pdfFileId):
    return await gameCrafterOperations.postDownloadableDocument(gameCrafterSession,  gameId, pdfFileId)

async def createTuckBox(gameCrafterSession, name, identity, quantity, gameId, backImageFileId):
    return await gameCrafterOperations.postTuckBox(gameCrafterSession, name, identity, quantity, gameId, backImageFileId)

async def createTwoSidedSet(gameCrafterSession, name, identity, quantity, gameId, backImageFileId):
    return await gameCrafterOperations.postTwoSidedSet(gameCrafterSession, name, identity, quantity, gameId, backImageFileId)

async def createTwoSided(gameCrafterSession, name, setId, quantity, imageFileId):
    return await gameCrafterOperations.postTwoSided(gameCrafterSession, name, setId, quantity, imageFileId)

async def printUser(gameCrafterSession):
    print(await gameCrafterOperations.getUser(gameCrafterSession))

async def listGames(gameCrafterSession):
    gamesResponse = await gameCrafterOperations.getGamesForUser(gameCrafterSession)
    await printGames(gamesResponse["items"])

async def listGamesForUserDesigners(gameCrafterSession):
    designersResponse = await gameCrafterOperations.getDesigners(gameCrafterSession)
    designers = designersResponse["items"]

    games = []
    for designer in designers:
        gamesResponse = await gameCrafterOperations.getGamesForDesignerId(gameCrafterSession, designer["id"])
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
    designersResponse = await gameCrafterOperations.getDesigners(gameCrafterSession)

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
    login = await gameCrafterOperations.login(gameCrafterSession, publicApiKey, userName, userPassword)
    gameCrafterSession.login(sessionId=login["id"], userId=login["user_id"])
    return gameCrafterSession

async def logout(gameCrafterSession):
    await gameCrafterOperations.logout(gameCrafterSession)