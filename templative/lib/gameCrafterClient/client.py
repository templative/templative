import os
import asyncio
from datetime import datetime

import templative.lib.gameCrafterClient.httpClient as httpClient

gameCrafterBaseUrl = "https://www.thegamecrafter.com/api"

async def login(client, publicApiKey, userName, userPassword):
    url = "%s/session" % gameCrafterBaseUrl
    return await httpClient.post(client, url, 
        api_key_id = publicApiKey,
        username = userName,
        password = userPassword
    )

async def getUser(client, session):
    url = "%s/user/%s" % (gameCrafterBaseUrl, session["user_id"])
    
    return await httpClient.get(client, url, 
        session_id = session["id"]
    )

async def getDesigners(client, session):
    url = "%s/user/%s/designers" % (gameCrafterBaseUrl, session["user_id"])
    return await httpClient.get(client, url,
        session_id = session["id"]
    )

async def getGamesForDesignerId(client, session, designerId):
    url = "%s/designer/%s/games" % (gameCrafterBaseUrl, designerId)
    return await httpClient.get(client, url,
        session_id = session["id"]
    )

async def getGamesForUser(client, session):
    url = "%s/user/%s/games" % (gameCrafterBaseUrl, session["user_id"])
    return await httpClient.get(client, url,
        session_id = session["id"]
    )

async def postGame(client, session, name, designerId):
    url = "%s/game" % gameCrafterBaseUrl
    return await httpClient.post(client, url,
        session_id = session["id"],
        name = name,
        designer_id = designerId,
        description='Automatically created (%s)' % name,
    )

async def postPokerDeck(client, session, name, quantity, gameId, backImageFileId):
    url = "%s/pokerdeck" % gameCrafterBaseUrl
    return await httpClient.post(client, url,
        session_id = session["id"],
        name = name,
        game_id = gameId,
        quantity = quantity,
        back_id = backImageFileId,
        has_proofed_back = 1
    )

async def postPokerCard(client, session, name, deckId, quantity, imageFileId):
    url = "%s/pokercard" % gameCrafterBaseUrl
    return await httpClient.post(client, url,
        session_id = session["id"],
        name = name,
        deck_id = deckId,
        quantity = quantity,
        face_id = imageFileId,
        back_from = "Deck",
        has_proofed_face = 1,
        has_proofed_back = 1
    )

async def postSmallStoutBox(client, session, gameId, name, quantity, topImageFileId, backImageFileId):
    url = "%s/smallstoutbox" % gameCrafterBaseUrl
    return await httpClient.post(client, url,
        session_id = session["id"],
        name = name,
        game_id = gameId,
        quantity = quantity,
        top_id = topImageFileId,
        has_proofed_top = 1,
        bottom_id = backImageFileId,
        has_proofed_bottom = 1
    )

async def postDocument(client, session, name, quantity, gameId, pdfFileId):
    url = "%s/document" % gameCrafterBaseUrl
    return await httpClient.post(client, url,
        session_id = session["id"],
        name = name,
        game_id = gameId,
        quantity = quantity,
        pdf_id = pdfFileId,
    )

async def postFolder(client, session, name, folderParentId):
    url = "%s/folder" % gameCrafterBaseUrl
    return await httpClient.post(client, url,
        session_id = session["id"],
        name=name,
        user_Id=session["user_id"],
        parent_id=folderParentId,
    )

async def postFile(client, session, file, filename, folderId):
    url = "%s/file" % gameCrafterBaseUrl
    return await httpClient.post(client, url,
        session_id = session["id"],
        file=file, 
        name=filename, 
        folder_id=folderId)





