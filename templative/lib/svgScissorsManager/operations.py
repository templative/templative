import os
import svgScissors
import asyncio

async def createArtFilesForComponent(game, gameCompose, componentCompose, frontMetaData, backMetaData, componentGameData, piecesGamedata, outputDirectory):
    if game == None:
        print("game cannot be None.")
        return
    
    if componentCompose == None:
        print("componentCompose cannot be None.")
        return

    if frontMetaData == None:
        print("artMetaData cannot be None.")
        return

    if componentGameData == None:
        print("componentGameData cannot be None.")
        return

    if piecesGamedata == None:
        print("piecesGamedata cannot be None.")
        return

    if outputDirectory == None: 
        print("outputDirectory cannot be None.")
        return
    
    tasks = []
    for pieceGamedata in piecesGamedata:
        tasks.append(asyncio.create_task(svgScissors.createArtFileOfPiece(game, gameCompose, componentCompose, componentGameData, pieceGamedata, frontMetaData, outputDirectory)))
    tasks.append(asyncio.create_task(svgScissors.createArtFileOfPiece(game, gameCompose, componentCompose, componentGameData, {"name":"back"}, backMetaData, outputDirectory)))

    for task in tasks:
        await task

async def getInstructionSetsForFiles(game, componentCompose, componentGamedata, componentFilepath):
    if game == None:
        print("game cannot be None.")
        return
    
    if componentCompose == None:
        print("component cannot be None.")
        return

    if componentGamedata == None:
        print("componentGamedata cannot be None.")
        return

    instructionSets = []
    for pieceGamedata in componentGamedata:
        filename = "%s-%s.jpg" % (componentCompose["name"], pieceGamedata["name"])
        artFilepath = os.path.join(componentFilepath, filename)
        instructionSets.append({"name": pieceGamedata["name"], "filepath": artFilepath, "quantity": pieceGamedata["quantity"]})

    return instructionSets

async def getBackInstructionSet(componentCompose, componentFilepath):
    filename = "%s-back.jpg" % componentCompose["name"]
    backFilepath = os.path.join(componentFilepath, filename)
    return {"name": filename, "filepath": backFilepath}
