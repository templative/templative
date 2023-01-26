import os
import asyncio
from datetime import datetime
from . import httpClient

gameCrafterBaseUrl = "https://www.thegamecrafter.com/api"

async def login(gameCrafterSession, publicApiKey, userName, userPassword):
    url = "%s/session" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        api_key_id = publicApiKey,
        username = userName,
        password = userPassword
    )

async def logout(gameCrafterSession):
    url = "%s/session/%s" % (gameCrafterBaseUrl, gameCrafterSession.sessionId)
    await httpClient.delete(gameCrafterSession, url)
    await gameCrafterSession.httpSession.close()

async def getUser(gameCrafterSession):
    url = "%s/user/%s" % (gameCrafterBaseUrl, gameCrafterSession.userId)

    return await httpClient.get(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId
    )

async def getDesigners(gameCrafterSession):
    url = "%s/user/%s/designers" % (gameCrafterBaseUrl, gameCrafterSession.userId)
    return await httpClient.get(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId
    )

async def getGamesForDesignerId(gameCrafterSession, designerId):
    url = "%s/designer/%s/games" % (gameCrafterBaseUrl, designerId)
    return await httpClient.get(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId
    )

async def getGamesForUser(gameCrafterSession):
    url = "%s/user/%s/games" % (gameCrafterBaseUrl, gameCrafterSession.userId)
    return await httpClient.get(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId
    )

async def postGame(gameCrafterSession, name, designerId):
    url = "%s/game" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        designer_id = designerId,
        description='Automatically created (%s)' % name,
    )

async def postPokerDeck(gameCrafterSession, name, quantity, gameId, backImageFileId):
    url = "%s/deck" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        game_id = gameId,
        identity = "PokerDeck",
        quantity = quantity,
        back_id = backImageFileId,
        has_proofed_back = 1
    )

async def postPokerCard(gameCrafterSession, name, deckId, quantity, imageFileId):
    url = "%s/card" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        deck_id = deckId,
        quantity = quantity,
        face_id = imageFileId,
        back_from = "Deck",
        has_proofed_face = 1,
        has_proofed_back = 1
    )

async def postSmallStoutBox(gameCrafterSession, gameId, name, quantity, topImageFileId, backImageFileId):
    url = "%s/twosidedbox" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        game_id = gameId,
        quantity = quantity,
        top_id = topImageFileId,
        has_proofed_top = 1,
        identity = "SmallStoutBox",
        bottom_id = backImageFileId,
        has_proofed_bottom = 1
    )

async def postDocument(gameCrafterSession, name, quantity, gameId, pdfFileId):
    url = "%s/document" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        game_id = gameId,
        quantity = quantity,
        identity = "Document",
        pdf_id = pdfFileId,
    )

async def postFolder(gameCrafterSession, name, folderParentId):
    url = "%s/folder" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name=name,
        user_Id=gameCrafterSession.userId,
        parent_id=folderParentId,
    )

async def postFile(gameCrafterSession, file, filename, folderId):
    url = "%s/file" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        file=file,
        name=filename,
        folder_id=folderId)





