import os
from .element import Element
from . import svgScissors
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