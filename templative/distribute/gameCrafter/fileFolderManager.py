import os
from templative.distribute.gameCrafter.util import httpOperations

async def createGame(gameCrafterSession, gameInfo, designerId, isPublish, shortDescription, longDescription, coolFactors, logoFileId, backdropFileId, advertisementFileId, websiteUrl, category, minAge:str, playTime:str, minPlayers:str, maxPlayers:str):
    gameName = gameInfo["displayName"] if isPublish else gameInfo["name"]

    uploadedGame = await httpOperations.postGame(gameCrafterSession, gameName, designerId, shortDescription, longDescription, coolFactors, logoFileId, backdropFileId, advertisementFileId, websiteUrl, category, minAge, playTime, minPlayers, maxPlayers)
    gameId = uploadedGame["id"]
    editUrl = "%s%s%s" % ("https://www.thegamecrafter.com", "/make/games/", gameId)
    print("Created %s. Edit it here %s" % (gameName, editUrl))

    return uploadedGame

async def createFolderAtRoot(gameCrafterSession, name):
    user = await httpOperations.getUser(gameCrafterSession)
    return await httpOperations.postFolder(gameCrafterSession, name, user['root_folder_id'])

async def postFile(gameCrafterSession, filepath, folderId):
    if not os.path.isfile(filepath):
        raise Exception ('Not a file: %s' % filepath)

    filename = os.path.basename(filepath)

    with open(filepath, "rb") as fileToUpload:
        return await httpOperations.postFile(gameCrafterSession, fileToUpload, filename, folderId)

async def createFileInFolder(gameCrafterSession, name, filepath, cloudComponentFolderId):
    print("Uploading %s from %s" % (name, filepath))
    cloudFile = await postFile(gameCrafterSession, filepath, cloudComponentFolderId)
    return cloudFile["id"]