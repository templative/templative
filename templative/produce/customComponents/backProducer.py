from templative.produce.customComponents.producer import Producer

from .. import outputWriter
from . import svgscissors
import os 
from hashlib import md5

from templative.manage.models.produceProperties import ProduceProperties
from templative.manage.models.gamedata import StudioData, GameData, ComponentData, ComponentBackData, PieceData
from templative.manage.models.composition import ComponentComposition
from templative.manage.models.artdata import ComponentArtdata
from templative.manage import defineLoader

from templative.componentInfo import COMPONENT_INFO

class BackProducer(Producer):
    @staticmethod
    async def createComponent(produceProperties:ProduceProperties, componentComposition:ComponentComposition, componentData:ComponentData, componentArtdata:ComponentArtdata):
        piecesDataBlob = await defineLoader.loadPiecesGamedata(produceProperties.inputDirectoryPath, componentComposition.gameCompose, componentComposition.componentCompose["piecesGamedataFilename"])
        if not piecesDataBlob or piecesDataBlob == {}:
            print("Skipping %s component due to missing pieces gamedata." % componentComposition.componentCompose["name"])
            return

        sourcedVariableNamesSpecificToPieceOnBackArtData = BackProducer.getSourcedVariableNamesSpecificToPieceOnBackArtdata(componentArtdata.artDataBlobDictionary["Back"])
        
        uniqueComponentBackDatas = BackProducer.createNewComponentBackPerUniqueBackGamedata(sourcedVariableNamesSpecificToPieceOnBackArtData, componentData, piecesDataBlob)
        
        for uniqueComponentBackData in uniqueComponentBackDatas:
            await BackProducer.createComponentBackDataPieces(uniqueComponentBackDatas[uniqueComponentBackData], sourcedVariableNamesSpecificToPieceOnBackArtData, componentComposition, produceProperties, componentArtdata, piecesDataBlob)
        
    # If the back art data needs data from the piece, that means our component has unique backs. Unique backs are handled as seperate components during manufacturing, so we'll output multiple componennts, one per unqiue back.
    @staticmethod
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
    
    @staticmethod
    def createNewComponentBackPerUniqueBackGamedata(sourcedVariableNamesSpecificToPieceOnBackArtData: [str], componentData:ComponentData, piecesDataBlob: any) -> any: 
        uniqueComponentBackDatas = {}
        for pieceGamedata in piecesDataBlob:
            uniqueHashOfSourceData = BackProducer.createUniqueBackHashForPiece(sourcedVariableNamesSpecificToPieceOnBackArtData, pieceGamedata)
            componentBackDataBlob = {}
            for sourcedVariable in sourcedVariableNamesSpecificToPieceOnBackArtData:
                componentBackDataBlob[sourcedVariable] = pieceGamedata[sourcedVariable]

            uniqueComponentBackDatas[uniqueHashOfSourceData] = ComponentBackData(componentData.studioDataBlob, componentData.gameDataBlob, componentData.componentDataBlob, componentBackDataBlob, sourcedVariableNamesSpecificToPieceOnBackArtData, uniqueHashOfSourceData)
            
        return uniqueComponentBackDatas

    @staticmethod
    def createUniqueBackHashForPiece(pieceSpecificBackArtDataSources: [str], pieceGamedata: any) -> str:
        pieceBackSourceHash = ""
        for pieceSpecificSource in pieceSpecificBackArtDataSources:
            pieceBackSourceHash += pieceGamedata[pieceSpecificSource].replace(" ","")
        if pieceBackSourceHash == "":
            return pieceBackSourceHash
        return md5(pieceBackSourceHash.encode()).hexdigest()[:8]

    @staticmethod
    async def createComponentBackDataPieces(uniqueComponentBackData:ComponentBackData, sourcedVariableNamesSpecificToPieceOnBackArtData: [str], compositions:ComponentComposition, produceProperties:ProduceProperties, componentArtdata:ComponentArtdata, piecesDataBlob: [any]):
        componentFolderName = compositions.componentCompose["name"] + uniqueComponentBackData.pieceUniqueBackHash
        
        componentBackOutputDirectory = await outputWriter.createComponentFolder(componentFolderName, produceProperties.outputDirectoryPath)
        await BackProducer.createUniqueComponentBackInstructions(uniqueComponentBackData, sourcedVariableNamesSpecificToPieceOnBackArtData, compositions, componentBackOutputDirectory, componentFolderName, piecesDataBlob)
        await svgscissors.createArtFilesForComponent(compositions, componentArtdata, uniqueComponentBackData, piecesDataBlob, componentBackOutputDirectory, produceProperties)

    @staticmethod
    async def createUniqueComponentBackInstructions(uniqueComponentBackData:ComponentBackData, sourcedVariableNamesSpecificToPieceOnBackArtData: [str], compositions: ComponentComposition, componentBackOutputDirectory: str, componentFolderName: str, piecesGamedata: any) -> None:
        componentInstructionFilepath = os.path.join(componentBackOutputDirectory, "component.json")
        frontInstructionSets = await BackProducer.getInstructionSetsForFilesForBackArtdataHash(uniqueComponentBackData.pieceUniqueBackHash, sourcedVariableNamesSpecificToPieceOnBackArtData, componentFolderName, piecesGamedata, componentBackOutputDirectory)
        backInstructionSetFilepath = await BackProducer.getBackInstructionSetFilepath(componentFolderName, componentBackOutputDirectory)
        
        componentInstructions = {
            "name": componentFolderName,
            "isDebugInfo": False if not "isDebugInfo" in compositions.componentCompose else compositions.componentCompose["isDebugInfo"],
            "type": compositions.componentCompose["type"],
            "quantity": compositions.componentCompose["quantity"],
            "frontInstructions": frontInstructionSets,
            "backInstructions": backInstructionSetFilepath
        }
        await outputWriter.dumpInstructions(componentInstructionFilepath, componentInstructions)

    @staticmethod
    async def getInstructionSetsForFilesForBackArtdataHash(uniqueComponentBackHash: str, sourcedVariableNamesSpecificToPieceOnBackArtData: [str],  componentBackName:str, piecesGamedataBlog:[any], componentBackFilepath:str):
        instructionSets = []
        for pieceGamedata in piecesGamedataBlog:
            pieceUniqueBackHash = BackProducer.createUniqueBackHashForPiece(sourcedVariableNamesSpecificToPieceOnBackArtData, pieceGamedata)
            isPieceInComponentBack = uniqueComponentBackHash == pieceUniqueBackHash
            if not isPieceInComponentBack:
                continue
            filename = "%s-%s.png" % (componentBackName, pieceGamedata["name"])
            artFilepath = os.path.join(componentBackFilepath, filename)
            instructionSets.append({"name": pieceGamedata["name"], "filepath": artFilepath, "quantity": pieceGamedata["quantity"]})

        return instructionSets

    @staticmethod
    async def getBackInstructionSetFilepath(componentName, componentFilepath):
        filename = "%s-back.png" % componentName
        backFilepath = os.path.join(componentFilepath, filename)
        return {"name": filename, "filepath": backFilepath}