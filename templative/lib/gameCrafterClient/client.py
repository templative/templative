import os
from datetime import datetime

import templative.lib.gameCrafterClient.httpClient as httpClient

gameCrafterBaseUrl = "https://www.thegamecrafter.com/api"

def login(publicApiKey, userName, userPassword):
    url = "%s/session" % gameCrafterBaseUrl
    return httpClient.post(url, 
        api_key_id = publicApiKey,
        username = userName,
        password = userPassword
    )

def getUser(session):
    url = "%s/user/%s" % (gameCrafterBaseUrl, session["user_id"])
    
    return httpClient.get(url, 
        session_id = session["id"]
    )

def getDesigners(session):
    url = "%s/user/%s/designers" % (gameCrafterBaseUrl, session["user_id"])
    return httpClient.get(url,
        session_id = session["id"]
    )

def getGamesForDesignerId(session, designerId):
    url = "%s/designer/%s/games" % (gameCrafterBaseUrl, designerId)
    return httpClient.get(url,
        session_id = session["id"]
    )

def getGamesForUser(session):
    url = "%s/user/%s/games" % (gameCrafterBaseUrl, session["user_id"])
    return httpClient.get(url,
        session_id = session["id"]
    )

def postGame(session, name, designerId):
    url = "%s/game" % gameCrafterBaseUrl
    return httpClient.post(url,
        session_id = session["id"],
        name = name,
        designer_id = designerId,
        description='Automatically created (%s)' % name,
    )

def postPokerDeck(session, name, quantity, gameId, backImageFileId):
    url = "%s/pokerdeck" % gameCrafterBaseUrl
    return httpClient.post(url,
        session_id = session["id"],
        name = name,
        game_id = gameId,
        quantity = quantity,
        back_id = backImageFileId,
        has_proofed_back = 1
    )

def postPokerCard(session, name, deckId, quantity, imageFileId):
    url = "%s/pokercard" % gameCrafterBaseUrl
    return httpClient.post(url,
        session_id = session["id"],
        name = name,
        deck_id = deckId,
        quantity = quantity,
        face_id = imageFileId,
        back_from = "Deck",
        has_proofed_face = 1,
        has_proofed_back = 1
    )

def postSmallStoutBox(session, name, quantity, gameId, topImageFileId, backImageFileId):
    url = "%s/smallstoutbox" % gameCrafterBaseUrl
    return httpClient.post(url,
        session_id = session["id"],
        name = name,
        game_id = gameId,
        quantity = quantity,
        top_id = topImageFileId,
        has_proofed_top = 1,
        bottom_id = backImageFileId,
        has_proofed_bottom = 1
    )

def postFolder(session, name, folderParentId):
    url = "%s/folder" % gameCrafterBaseUrl
    return httpClient.post(url,
        session_id = session["id"],
        name=name,
        user_Id=session["user_id"],
        parent_id=folderParentId,
    )

def postFile(session, file, filename, folderId):
    url = "%s/file" % gameCrafterBaseUrl
    return httpClient.post(url,
        session_id = session["id"],
        files={"file":file}, 
        name=filename, 
        folder_id=folderId)





