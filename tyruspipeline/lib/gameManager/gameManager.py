import gameLoader

def produceGame(gameRootDirectoryPath):
    if not gameRootDirectoryPath:
        raise Exception("Game root directory path is invalid.")

    game = gameLoader.loadGame(gameRootDirectoryPath)

    components = gameLoader.loadGameComponents(gameRootDirectoryPath)