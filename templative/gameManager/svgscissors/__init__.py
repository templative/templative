from . import svgScissors
import asyncio

async def createArtFilesForComponent(game, studioCompose, gameCompose, componentCompose, frontMetaData, backMetaData, componentGameData, piecesGamedata, outputDirectory, isSimple):
    if game == None:
        print("game cannot be None.")
        return

    if studioCompose == None:
        print("studioCompose cannot be None.")
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
        tasks.append(asyncio.create_task(svgScissors.createArtFileOfPiece(game, studioCompose, gameCompose, componentCompose, componentGameData, pieceGamedata, frontMetaData, outputDirectory, isSimple)))
    tasks.append(asyncio.create_task(svgScissors.createArtFileOfPiece(game, studioCompose, gameCompose, componentCompose, componentGameData, {"name":"back"}, backMetaData, outputDirectory, isSimple)))

    for task in tasks:
        await task