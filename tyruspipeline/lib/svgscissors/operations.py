import os
from client import createArtFileOfPiece

def createArtFilesForComponent(game, gameCompose, component, frontMetaData, backMetaData, componentGamedata, outputDirectory):
    if game == None:
        print("game cannot be None.")
        return
    
    if component == None:
        print("component cannot be None.")
        return

    if frontMetaData == None:
        print("artMetaData cannot be None.")
        return

    if componentGamedata == None:
        print("componentGamedata cannot be None.")
        return

    if outputDirectory == None: 
        print("outputDirectory cannot be None.")
        return
    
    for pieceGamedata in componentGamedata:
        createArtFileOfPiece(game, gameCompose, component, pieceGamedata, frontMetaData, outputDirectory)

    createArtFileOfPiece(game, gameCompose, component, {"name":"back"}, backMetaData, outputDirectory)

def getInstructionSetsForFiles(game, component, componentGamedata, componentFilepath):
    if game == None:
        print("game cannot be None.")
        return
    
    if component == None:
        print("component cannot be None.")
        return

    if componentGamedata == None:
        print("componentGamedata cannot be None.")
        return

    instructionSets = []
    for pieceGamedata in componentGamedata:
        filename = "%s-%s.jpg" % (component["name"], pieceGamedata["name"])
        artFilepath = os.path.join(componentFilepath, filename)
        instructionSets.append({"name": pieceGamedata["name"], "filepath": artFilepath, "quantity": pieceGamedata["quantity"]})

    return instructionSets

def getBackInstructionSet(component, componentFilepath):
    filename = "%s-back.jpg" % component["name"]
    backFilepath = os.path.join(componentFilepath, filename)
    return {"name": filename, "filepath": backFilepath}
