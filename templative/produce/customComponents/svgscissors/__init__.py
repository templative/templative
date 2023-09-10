import asyncio
import hashlib 

from .svgScissors import createArtFileOfPiece

from templative.manage.models.produceProperties import ProduceProperties
from templative.manage.models.gamedata import StudioData, GameData, ComponentData, ComponentBackData, PieceData
from templative.manage.models.composition import ComponentComposition
from templative.manage.models.artdata import ComponentArtdata

# Duplicated
def createUniqueBackHashForPiece(pieceSpecificBackArtDataSources: [str], pieceGamedata: any) -> str:
    pieceBackSourceHash = ""
    for pieceSpecificSource in pieceSpecificBackArtDataSources:
        pieceBackSourceHash += pieceGamedata[pieceSpecificSource].replace(" ","") # hashlib.md5(pieceGamedata[pieceSpecificSource].encode("utf")).hexdigest()
    return pieceBackSourceHash

async def createArtFilesForComponent(compositions:ComponentComposition, componentArtdata:ComponentArtdata, uniqueComponentBackData:ComponentBackData, piecesDataBlob:[any], componentBackOutputDirectory:str, produceProperties:ProduceProperties):
    tasks = []
    for pieceGamedata in piecesDataBlob:
        pieceHash = createUniqueBackHashForPiece(uniqueComponentBackData.sourcedVariableNamesSpecificToPieceOnBackArtData, pieceGamedata)
        if pieceHash != uniqueComponentBackData.pieceUniqueBackHash:
            continue
        pieceData = PieceData(uniqueComponentBackData.studioDataBlob, uniqueComponentBackData.gameDataBlob, uniqueComponentBackData.componentDataBlob, uniqueComponentBackData.componentBackDataBlob, uniqueComponentBackData.sourcedVariableNamesSpecificToPieceOnBackArtData, uniqueComponentBackData.pieceUniqueBackHash, pieceGamedata)
        tasks.append(asyncio.create_task(createArtFileOfPiece(compositions, componentArtdata.artDataBlobDictionary["Front"], pieceData, componentBackOutputDirectory, produceProperties)))

    uniqueComponentBackData.componentBackDataBlob["name"] = "back"
    if "Back" in componentArtdata.artDataBlobDictionary:
        tasks.append(asyncio.create_task(createArtFileOfPiece(compositions, componentArtdata.artDataBlobDictionary["Back"], uniqueComponentBackData, componentBackOutputDirectory, produceProperties)))
    
    for task in tasks:
        await task