from . import svgScissors
import asyncio
import os 

from .svgScissors import createArtFileOfPiece

from templative.gameManager.models.produceProperties import ProduceProperties
from templative.gameManager.models.gamedata import StudioData, GameData, ComponentData, ComponentBackData, PieceData
from templative.gameManager.models.composition import ComponentComposition
from templative.gameManager.models.artdata import ComponentArtdata

def createUniqueBackHashForPiece(pieceSpecificBackArtDataSources: [str], pieceGamedata: any) -> str:
    pieceBackSourceHash = ""
    for pieceSpecificSource in pieceSpecificBackArtDataSources:
        pieceBackSourceHash = pieceBackSourceHash + pieceGamedata[pieceSpecificSource]
    return pieceBackSourceHash

async def createArtFilesForComponent(compositions:ComponentComposition, componentArtdata:ComponentArtdata, uniqueComponentBackData:ComponentBackData, piecesDataBlob:[any], componentBackOutputDirectory:str, produceProperties:ProduceProperties):
    tasks = []
    for pieceGamedata in piecesDataBlob:
        pieceHash = createUniqueBackHashForPiece(uniqueComponentBackData.sourcedVariableNamesSpecificToPieceOnBackArtData, pieceGamedata)
        if pieceHash != uniqueComponentBackData.pieceUniqueBackHash:
            continue
        pieceData = PieceData(uniqueComponentBackData.studioDataBlob, uniqueComponentBackData.gameDataBlob, uniqueComponentBackData.componentDataBlob, uniqueComponentBackData.componentBackDataBlob, uniqueComponentBackData.sourcedVariableNamesSpecificToPieceOnBackArtData, uniqueComponentBackData.pieceUniqueBackHash, pieceGamedata)
        tasks.append(asyncio.create_task(createArtFileOfPiece(compositions, componentArtdata.frontArtdataBlob, pieceData, componentBackOutputDirectory, produceProperties)))

    uniqueComponentBackData.componentBackDataBlob["name"] = "back"
    tasks.append(asyncio.create_task(createArtFileOfPiece(compositions, componentArtdata.backArtdataBlob, uniqueComponentBackData, componentBackOutputDirectory, produceProperties)))
    
    for task in tasks:
        await task