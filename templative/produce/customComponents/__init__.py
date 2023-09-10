from .. import outputWriter
from . import svgscissors
import os 

from templative.manage.models.produceProperties import ProduceProperties
from templative.manage.models.gamedata import StudioData, GameData, ComponentData, ComponentBackData, PieceData
from templative.manage.models.composition import ComponentComposition
from templative.manage.models.artdata import ComponentArtdata
from templative.manage import defineLoader

from templative.componentInfo import COMPONENT_INFO

async def produceCustomComponent(produceProperties:ProduceProperties, gamedata:GameData, componentComposition:ComponentComposition) -> None:
    componentName = componentComposition.componentCompose["name"]
    
    componentDataBlob = await defineLoader.loadComponentGamedata(produceProperties.inputDirectoryPath, componentComposition.gameCompose, componentComposition.componentCompose["componentGamedataFilename"])
    if not componentDataBlob or componentDataBlob == {}:
        print("Skipping %s component due to missing component gamedata." % componentName)
        return

    componentArtdata = await getComponentArtdata(componentName, produceProperties.inputDirectoryPath, componentComposition)
    if componentArtdata == None:
        return
    
    componentData = ComponentData(gamedata.studioDataBlob, gamedata.gameDataBlob, componentDataBlob)

    # THere are front, frontback, front back overlay, front back front overlay back overylay

    if "Back" in componentArtdata.artDataBlobDictionary: 
        await createItemWithBack(produceProperties, componentComposition, componentData, componentArtdata)


    if "Front" in componentArtdata.artDataBlobDictionary and len(componentArtdata.artDataBlobDictionary) == 1:
        await createItemWithoutBack(produceProperties, componentComposition, componentData, componentArtdata)

    print("Creating art assets for %s component." % (componentName))

async def createItemWithBack(produceProperties:ProduceProperties, componentComposition:ComponentComposition, componentData:ComponentData, componentArtdata:ComponentArtdata):

    piecesDataBlob = await defineLoader.loadPiecesGamedata(produceProperties.inputDirectoryPath, componentComposition.gameCompose, componentComposition.componentCompose["piecesGamedataFilename"])
    if not piecesDataBlob or piecesDataBlob == {}:
        print("Skipping %s component due to missing pieces gamedata." % componentComposition.componentCompose["name"])
        return

    sourcedVariableNamesSpecificToPieceOnBackArtData = getSourcedVariableNamesSpecificToPieceOnBackArtdata(componentArtdata.artDataBlobDictionary["Back"])
    
    uniqueComponentBackDatas = createNewComponentBackPerUniqueBackGamedata(sourcedVariableNamesSpecificToPieceOnBackArtData, componentData, piecesDataBlob)
    
    for uniqueComponentBackData in uniqueComponentBackDatas:
        await createComponentBackDataPieces(uniqueComponentBackDatas[uniqueComponentBackData], sourcedVariableNamesSpecificToPieceOnBackArtData, componentComposition, produceProperties, componentArtdata, piecesDataBlob)

async def createItemWithoutBack(produceProperties:ProduceProperties, componentComposition:ComponentComposition, componentData:ComponentData, componentArtdata:ComponentArtdata):
    pass
    # piecesDataBlob = await defineLoader.loadPiecesGamedata(produceProperties.inputDirectoryPath, componentComposition.gameCompose, componentComposition.componentCompose["piecesGamedataFilename"])
    # if not piecesDataBlob or piecesDataBlob == {}:
    #     print("Skipping %s component due to missing pieces gamedata." % componentComposition.componentCompose["name"])
    #     return
    
    # componentBackOutputDirectory = await outputWriter.createComponentFolder(componentComposition.componentCompose["name"], produceProperties.outputDirectoryPath)
    # componentInstructionFilepath = os.path.join(componentBackOutputDirectory, "component.json")
    # frontInstructionSets = await getInstructionSetsForFilesForBackArtdataHash(uniqueComponentBackData.pieceUniqueBackHash, sourcedVariableNamesSpecificToPieceOnBackArtData, componentFolderName, piecesGamedata, componentBackOutputDirectory)

    # componentInstructions = {
    #     "name": componentComposition.componentCompose["name"],
    #     "isDebugInfo": False if not "isDebugInfo" in componentComposition.componentCompose else componentComposition.componentCompose["isDebugInfo"],
    #     "type": componentComposition.componentCompose["type"],
    #     "quantity": componentComposition.componentCompose["quantity"],
    #     "frontInstructions": frontInstructionSets
    # }
    # await outputWriter.dumpInstructions(componentInstructionFilepath, componentInstructions)
    # await svgscissors.createArtFilesForComponent(componentComposition, componentArtdata, uniqueComponentBackData, piecesDataBlob, componentBackOutputDirectory, produceProperties)


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

async def getComponentArtdata(componentName, inputDirectoryPath, componentComposition) -> ComponentArtdata:
    artDatas = {}
    componentType = componentComposition.componentCompose["type"]
    for artDataTypeName in COMPONENT_INFO[componentType]["ArtDataTypeNames"]:
        print(artDataTypeName)
        artDataTypeFilepath = componentComposition.componentCompose["artdata%sFilename" % artDataTypeName]
        print(artDataTypeFilepath)
        artData = await defineLoader.loadArtdata(inputDirectoryPath, componentComposition.gameCompose["artdataDirectory"], artDataTypeFilepath)
        if not artData or artData == None:
            print("Skipping %s component due to missing %s art metadata." % (componentName, artDataTypeName))
        artDatas[artDataTypeName] = artData
    
    return ComponentArtdata(artDatas)

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