from . import svgscissors
import asyncio
import os 
import hashlib

from ..models.produceProperties import ProduceProperties
from ..models.gamedata import StudioData, GameData, ComponentData, ComponentBackData, PieceData
from ..models.composition import ComponentComposition
from ..models.artdata import ComponentArtdata
from .. import defineLoader, outputWriter

async def produceCustomComponent(produceProperties:ProduceProperties, gamedata:GameData, componentComposition:ComponentComposition) -> None:
    componentName = componentComposition.componentCompose["name"]
    
    componentDataBlob = await defineLoader.loadComponentGamedata(produceProperties.inputDirectoryPath, componentComposition.gameCompose, componentComposition.componentCompose["componentGamedataFilename"])
    if not componentDataBlob or componentDataBlob == {}:
        print("Skipping %s component due to missing component gamedata." % componentName)
        return

    piecesDataBlob = await defineLoader.loadPiecesGamedata(produceProperties.inputDirectoryPath, componentComposition.gameCompose, componentComposition.componentCompose["piecesGamedataFilename"])
    if not piecesDataBlob or piecesDataBlob == {}:
        print("Skipping %s component due to missing pieces gamedata." % componentName)
        return

    componentArtdata = await getComponentArtdata(componentName, produceProperties.inputDirectoryPath, componentComposition)
    if componentArtdata == None:
        return
    
    componentData = ComponentData(gamedata.studioDataBlob, gamedata.gameDataBlob, componentDataBlob)

    sourcedVariableNamesSpecificToPieceOnBackArtData = getSourcedVariableNamesSpecificToPieceOnBackArtdata(componentArtdata.backArtdataBlob)
    
    uniqueComponentBackDatas = createNewComponentBackPerUniqueBackGamedata(sourcedVariableNamesSpecificToPieceOnBackArtData, componentData, piecesDataBlob)
    
    for uniqueComponentBackData in uniqueComponentBackDatas:
        await createComponentBackDataPieces(uniqueComponentBackDatas[uniqueComponentBackData], sourcedVariableNamesSpecificToPieceOnBackArtData, componentComposition, produceProperties, componentArtdata, piecesDataBlob)

    print("Creating art assets for %s component." % (componentName))

# If the back art data needs data from the piece, that means our component has unique backs. Unique backs are handled as seperate components during manufacturing, so we'll output multiple componennts, one per unqiue back.
def getSourcedVariableNamesSpecificToPieceOnBackArtdata(componentBackArtdata:any) -> [str]:
    keys = []
    for textReplacement in componentBackArtdata["textReplacements"]:
        if textReplacement["scope"] != "piece":
            continue
        keys.append(textReplacement["source"])
    for overlay in componentBackArtdata["overlays"]:
        if overlay["scope"] != "piece":
            continue
        keys.append(overlay["source"])
    for styleUpdate in componentBackArtdata["styleUpdates"]:
        if styleUpdate["scope"] != "piece":
            continue
        keys.append(styleUpdate["source"])
    return keys

async def getComponentArtdata(componentName, inputDirectoryPath, componentComposition: ComponentComposition) -> ComponentArtdata:
    componentArtdata = await defineLoader.loadArtdata(inputDirectoryPath, componentComposition.gameCompose["artdataDirectory"], componentComposition.componentCompose["artdataFilename"])
    if not componentArtdata or componentArtdata == None:
        print("Skipping %s component due to missing front art metadata." % componentName)
        return None

    componentBackArtdata = await defineLoader.loadArtdata(inputDirectoryPath, componentComposition.gameCompose["artdataDirectory"], componentComposition.componentCompose["backArtdataFilename"])
    if not componentBackArtdata or componentBackArtdata == {}:
        print("Skipping %s component due to missing back art metadata." % componentName)
        return None
    
    return ComponentArtdata(componentArtdata, componentBackArtdata)

def createNewComponentBackPerUniqueBackGamedata(sourcedVariableNamesSpecificToPieceOnBackArtData: [str], componentData:ComponentData, piecesDataBlob: any) -> any: 
    uniqueComponentBackDatas = {}
    for pieceGamedata in piecesDataBlob:
        uniqueHashOfSourceData = createUniqueBackHashForPiece(sourcedVariableNamesSpecificToPieceOnBackArtData, pieceGamedata)
        componentBackDataBlob = {}
        for sourcedVariable in sourcedVariableNamesSpecificToPieceOnBackArtData:
            componentBackDataBlob[sourcedVariable] = pieceGamedata[sourcedVariable]

        uniqueComponentBackDatas[uniqueHashOfSourceData] = ComponentBackData(componentData.studioDataBlob, componentData.gameDataBlob, componentData.componentDataBlob, componentBackDataBlob, sourcedVariableNamesSpecificToPieceOnBackArtData, uniqueHashOfSourceData)
          
    return uniqueComponentBackDatas

# Duplicated
def createUniqueBackHashForPiece(pieceSpecificBackArtDataSources: [str], pieceGamedata: any) -> str:
    pieceBackSourceHash = ""
    for pieceSpecificSource in pieceSpecificBackArtDataSources:
        pieceBackSourceHash += pieceGamedata[pieceSpecificSource].replace(" ","")# hashlib.md5(pieceGamedata[pieceSpecificSource].encode("utf")).hexdigest()
    return pieceBackSourceHash

async def createComponentBackDataPieces(uniqueComponentBackData:ComponentBackData, sourcedVariableNamesSpecificToPieceOnBackArtData: [str], compositions:ComponentComposition, produceProperties:ProduceProperties, componentArtdata:ComponentArtdata, piecesDataBlob: [any]):
    componentFolderName = compositions.componentCompose["name"] + uniqueComponentBackData.pieceUniqueBackHash
    
    componentBackOutputDirectory = await outputWriter.createComponentFolder(componentFolderName, produceProperties.outputDirectoryPath)
    await createUniqueComponentBackInstructions(uniqueComponentBackData, sourcedVariableNamesSpecificToPieceOnBackArtData, compositions, componentBackOutputDirectory, componentFolderName, piecesDataBlob)
    await svgscissors.createArtFilesForComponent(compositions, componentArtdata, uniqueComponentBackData, piecesDataBlob, componentBackOutputDirectory, produceProperties)

async def createUniqueComponentBackInstructions(uniqueComponentBackData:ComponentBackData, sourcedVariableNamesSpecificToPieceOnBackArtData: [str], compositions: ComponentComposition, componentBackOutputDirectory: str, componentFolderName: str, piecesGamedata: any) -> None:
    componentInstructionFilepath = os.path.join(componentBackOutputDirectory, "component.json")
    frontInstructionSets = await getInstructionSetsForFilesForBackArtdataHash(uniqueComponentBackData.pieceUniqueBackHash, sourcedVariableNamesSpecificToPieceOnBackArtData, componentFolderName, piecesGamedata, componentBackOutputDirectory)
    backInstructionSetFilepath = await getBackInstructionSetFilepath(componentFolderName, componentBackOutputDirectory)
    
    componentInstructions = {
        "name": componentFolderName,
        "isDebugInfo": False if not "isDebugInfo" in compositions.componentCompose else compositions.componentCompose["isDebugInfo"],
        "type": compositions.componentCompose["type"],
        "quantity": compositions.componentCompose["quantity"],
        "frontInstructions": frontInstructionSets,
        "backInstructions": backInstructionSetFilepath
    }
    await outputWriter.dumpInstructions(componentInstructionFilepath, componentInstructions)

async def getInstructionSetsForFilesForBackArtdataHash(uniqueComponentBackHash: str, sourcedVariableNamesSpecificToPieceOnBackArtData: [str],  componentBackName:str, piecesGamedataBlog:[any], componentBackFilepath:str):
    instructionSets = []
    for pieceGamedata in piecesGamedataBlog:
        pieceUniqueBackHash = createUniqueBackHashForPiece(sourcedVariableNamesSpecificToPieceOnBackArtData, pieceGamedata)
        isPieceInComponentBack = uniqueComponentBackHash == pieceUniqueBackHash
        if not isPieceInComponentBack:
            continue
        filename = "%s-%s.jpg" % (componentBackName, pieceGamedata["name"])
        artFilepath = os.path.join(componentBackFilepath, filename)
        instructionSets.append({"name": pieceGamedata["name"], "filepath": artFilepath, "quantity": pieceGamedata["quantity"]})

    return instructionSets

async def getBackInstructionSetFilepath(componentName, componentFilepath):
    filename = "%s-back.jpg" % componentName
    backFilepath = os.path.join(componentFilepath, filename)
    return {"name": filename, "filepath": backFilepath}