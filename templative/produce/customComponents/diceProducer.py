from templative.produce.customComponents.producer import Producer

from .. import outputWriter
from . import svgscissors
import os 

from templative.manage.models.produceProperties import ProduceProperties
from templative.manage.models.gamedata import StudioData, GameData, ComponentData, ComponentBackData, PieceData
from templative.manage.models.composition import ComponentComposition
from templative.manage.models.artdata import ComponentArtdata
from templative.manage import defineLoader

from templative.componentInfo import COMPONENT_INFO

class DiceProducer(Producer):
    @staticmethod
    async def createComponent(produceProperties:ProduceProperties, componentComposition:ComponentComposition, componentData:ComponentData, componentArtdata:ComponentArtdata):
        piecesDataBlob = await defineLoader.loadPiecesGamedata(produceProperties.inputDirectoryPath, componentComposition.gameCompose, componentComposition.componentCompose["piecesGamedataFilename"])
        if not piecesDataBlob or piecesDataBlob == {}:
            print("Skipping %s component due to missing pieces gamedata." % componentComposition.componentCompose["name"])
            return

        await DiceProducer.createComponentBackDataPieces(produceProperties, componentComposition, componentData, componentArtdata, piecesDataBlob)

    @staticmethod
    async def createComponentBackDataPieces(produceProperties:ProduceProperties, componentComposition:ComponentComposition, componentData:ComponentData, componentArtdata:ComponentArtdata, piecesDataBlob: [any]):
        componentFolderName = componentComposition.componentCompose["name"]
        
        componentBackOutputDirectory = await outputWriter.createComponentFolder(componentFolderName, produceProperties.outputDirectoryPath)
        await DiceProducer.writeComponentInstructions(componentComposition, componentBackOutputDirectory, componentFolderName, piecesDataBlob)
        
        # We use a component back that has no unique data. It has the same info within it as a componentData.
        componentBackData = ComponentBackData(componentData.studioDataBlob, componentData.gameDataBlob, componentData.componentDataBlob)
        await svgscissors.createArtFilesForComponent(componentComposition, componentArtdata, componentBackData, piecesDataBlob, componentBackOutputDirectory, produceProperties)

    @staticmethod
    async def writeComponentInstructions(compositions: ComponentComposition, componentBackOutputDirectory: str, componentFolderName: str, piecesGamedata: any) -> None:
        componentInstructionFilepath = os.path.join(componentBackOutputDirectory, "component.json")
        dieFaceFilepaths = await DiceProducer.getDieFaceFilepaths(componentFolderName, piecesGamedata, componentBackOutputDirectory)
        
        componentInstructions = {
            "name": componentFolderName,
            "isDebugInfo": False if not "isDebugInfo" in compositions.componentCompose else compositions.componentCompose["isDebugInfo"],
            "type": compositions.componentCompose["type"],
            "quantity": compositions.componentCompose["quantity"],
            "dieFaceFilepaths": dieFaceFilepaths
        }
        await outputWriter.dumpInstructions(componentInstructionFilepath, componentInstructions)

    @staticmethod
    async def getDieFaceFilepaths(componentName:str, piecesGamedata:[any], componentArtDirectoryPath:str):
        filepaths = []
        for pieceGamedata in piecesGamedata:
            filename = "%s-%s.jpg" % (componentName, pieceGamedata["name"])
            artFilepath = os.path.join(componentArtDirectoryPath, filename)
            filepaths.append(artFilepath)

        return filepaths