from .util import httpOperations
from .fileFolderManager import createFolderAtRoot, createFileInFolder

advertismentImages = [
    "C:/Users/User/Documents/git/nextdaygames/templative/templative/gameCrafter/testImages/actionShot.png",
    "C:/Users/User/Documents/git/nextdaygames/templative/templative/gameCrafter/testImages/advertisment.png",
    "C:/Users/User/Documents/git/nextdaygames/templative/templative/gameCrafter/testImages/backdrop.png",
    "C:/Users/User/Documents/git/nextdaygames/templative/templative/gameCrafter/testImages/logo.png"
]
async def createAdvertisementImages(gameCrafterSession):
    folder = await createFolderAtRoot(gameCrafterSession, "AdvertisementImages")
    
    for filepath in advertismentImages:
        print(filepath)
        file = await createFileInFolder(gameCrafterSession, filepath, "advertisement.png", folder["id"])
        print(filepath, file["id"])

async def createActionShot(gameCrafterSession, gameId):
    await httpOperations.createActionShot(gameCrafterSession, gameId)