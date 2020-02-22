from ..gameCrafterClient import operations as gamecrafter
import client as client

def uploadGame(gameRootDirectoryPath):
    game = client.loadGame(gameRootDirectoryPath)
    company = client.loadCompany(gameRootDirectoryPath)

    print("Uploading %s for %s." % (game["name"], company["name"]))