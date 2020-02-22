from ..gameCrafterClient import operations as gamecrafter
import client as client

def uploadGame(gameRootDirectoryPath):
    
    if gameRootDirectoryPath is None:
        print("gameRootDirectoryPath cannot be None")
        return

    session = gamecrafter.login()

    game = client.loadGame(gameRootDirectoryPath)
    company = client.loadCompany(gameRootDirectoryPath)

    print("Uploading %s for %s." % (game["name"], company["name"]))

    cloudGame = gamecrafter.createGame(session, game["name"], company["gameCrafterDesignerId"])
    cloudGameFolder = gamecrafter.createFolderAtRoot(session, game["name"])

    client.uploadComponents(session, gameRootDirectoryPath, cloudGame, cloudGameFolder)

