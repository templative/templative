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


async def postGame(gameCrafterSession, name, designerId, shortDescription, longDescription, coolFactors, logoFileId:str, backdropFileId:str, advertisementFileId:str, websiteUrl, category, minAge:str, playTime:str, minPlayers:str, maxPlayers:str):
    url = "%s/game" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        designer_id = designerId,
        short_description=shortDescription,
        description=longDescription,
        cool_factor_1=coolFactors[0],
        cool_factor_2=coolFactors[1],
        cool_factor_3=coolFactors[2],
        logo_id=logoFileId,
        backdrop_id=backdropFileId,
        advertisement_id=advertisementFileId,
        private_sales=1,
        private_viewing=1,
        website_uri=websiteUrl,
        category=category,
        min_age=minAge,
        play_time=playTime,
        min_players=minPlayers,
        max_players=maxPlayers
    )

async def deleteGame(gameCrafterSession, id):
    url = "%s/game/%s" % (gameCrafterBaseUrl, id)
    return await httpClient.delete(gameCrafterSession, url)

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

async def createActionShot(gameCrafterSession, gameId, advertisementFileId:str):
    url = "%s/actionshot" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        game_id=gameId,
        advertisement_id=advertisementFileId,
    )

async def postStockPart(gameCrafterSession, stockPartId, quantity, gameId):
    url = "%s/gamepart" % (gameCrafterBaseUrl)
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        game_id = gameId,
        quantity = quantity,
        part_id = stockPartId
    )

async def postTwoSidedSet(gameCrafterSession, name, identity, quantity, gameId, backImageId):
    url = "%s/twosidedset" % (gameCrafterBaseUrl)
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        game_id = gameId,
        quantity = quantity,
        identity = identity,
        back_id = backImageId,
        has_proofed_back = 1,
    )

async def postTwoSided(gameCrafterSession, name, setId, quantity, faceImageId):
    url = "%s/twosided" % (gameCrafterBaseUrl)
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        set_id = setId,
        quantity = quantity,
        face_id = faceImageId,
        has_proofed_face = 1,
    )

async def postTuckBox(gameCrafterSession, name, identity, quantity, gameId, imageId):
    url = "%s/tuckbox" % (gameCrafterBaseUrl)
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        game_id = gameId,
        quantity = quantity,
        outside_id = imageId,
        identity = identity,
        has_proofed_outside = 1,
    )

async def postDeck(gameCrafterSession, name, identity, quantity, gameId, backImageFileId):
    url = "%s/deck" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        game_id = gameId,
        identity = identity,
        quantity = quantity,
        back_id = backImageFileId,
        has_proofed_back = 1
    )

async def postDeckCard(gameCrafterSession, name, deckId, quantity, imageFileId):
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

async def postTwoSidedBox(gameCrafterSession, gameId, name, identity, quantity, topImageFileId, backImageFileId):
    url = "%s/twosidedbox" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        game_id = gameId,
        quantity = quantity,
        top_id = topImageFileId,
        has_proofed_top = 1,
        identity = identity,
        bottom_id = backImageFileId,
        has_proofed_bottom = 1
    )

async def postTwoSidedSluggedSet(gameCrafterSession, name, identity, quantity, gameId, backImageFileId):
    url = "%s/twosidedsluggedset" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        game_id = gameId,
        identity = identity,
        quantity = quantity,
        back_id = backImageFileId,
        has_proofed_back = 1
    )

async def postTwoSidedSlugged(gameCrafterSession, name, setId, quantity, imageFileId):
    url = "%s/twosidedslugged" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        name = name,
        set_id = setId,
        quantity = quantity,
        face_id = imageFileId,
        has_proofed_face = 1,
        has_proofed_back = 1
    )

async def postDownloadableDocument(gameCrafterSession, gameId, pdfFileId):
    url = "%s/gamedownload" % gameCrafterBaseUrl
    return await httpClient.post(gameCrafterSession, url,
        session_id = gameCrafterSession.sessionId,
        game_id = gameId,
        file_id = pdfFileId,
        name = "rules.pdf"
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
        use_for = "Download"
    )




