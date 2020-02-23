
import client as client

def uploadGame(gameRootDirectoryPath):
    
    if gameRootDirectoryPath is None:
        print("gameRootDirectoryPath cannot be None")
        return

    client.uploadGame(gameRootDirectoryPath)

