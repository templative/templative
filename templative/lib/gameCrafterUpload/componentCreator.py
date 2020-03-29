from templative.lib.gameCrafterClient import operations as gamecrafter
from os.path import isfile, join

def createPokerDeck(session, component, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = gamecrafter.createFolderAtParent(session, componentName, cloudGameFolderId)
    
    backImageId = createFileInFolder(session, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])
    cloudPokerDeck = gamecrafter.createPokerDeck(session, componentName, quantity, cloudGameId, backImageId)

    for instructions in frontInstructions:
        createPokerCardPiece(session, instructions, cloudPokerDeck["id"], cloudComponentFolder["id"])

def createSmallStoutBox(session, component, cloudGameId, cloudGameFolderId):
    componentName = component["name"]
    quantity = component["quantity"]
    frontInstructions = component["frontInstructions"]
    backInstructions = component["backInstructions"]

    print("Uploading %s %s %s(s)" % (quantity, componentName, component["type"]))

    cloudComponentFolder = gamecrafter.createFolderAtParent(session, componentName, cloudGameFolderId)
    topImageFileId = createFileInFolder(session, frontInstructions[0]["name"], frontInstructions[0]["filepath"], cloudComponentFolder["id"])
    bottomImageFileId = createFileInFolder(session, backInstructions["name"], backInstructions["filepath"], cloudComponentFolder["id"])

    cloudPokerDeck = gamecrafter.createSmallStoutBox(session, cloudGameId, componentName, quantity, topImageFileId, bottomImageFileId)

def createRules(session, gameRootDirectoryPath, cloudGame, folderId):
    name = "rules"
    filepath = join(gameRootDirectoryPath, "rules.pdf")
    quantity = 1
    print("Uploading %s" % (filepath))

    cloudFile = gamecrafter.uploadFile(session, filepath, folderId)
    document = gamecrafter.createDocument(session, name, quantity, cloudGame["id"], cloudFile["id"])

def createFileInFolder(session, name, filepath, cloudComponentFolderId):
    print("Uploading %s from %s" % (name, filepath))
    cloudFile = gamecrafter.uploadFile(session, filepath, cloudComponentFolderId)
    return cloudFile["id"]

def createPokerCardPiece(session, instructions, deckId, cloudComponentFolderId):
    name = instructions["name"]
    filepath = instructions["filepath"]
    quantity = instructions["quantity"]
    print("Uploading %s" % (filepath))

    cloudFile = gamecrafter.uploadFile(session, filepath, cloudComponentFolderId)
    pokerCard = gamecrafter.createPokerCard(session, name, deckId, quantity, cloudFile["id"])