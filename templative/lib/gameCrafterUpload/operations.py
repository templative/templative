
import templative.lib.gameCrafterUpload.client as client

def uploadGame(gameRootDirectoryPath):
    
    if gameRootDirectoryPath is None:
        print("gameRootDirectoryPath cannot be None")
        return

    return client.uploadGame(gameRootDirectoryPath)

