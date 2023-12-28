from .. import outputWriter
from . import svgscissors
import os 

from templative.lib.manage.models.produceProperties import ProduceProperties
from templative.lib.manage.models.gamedata import StudioData, GameData, ComponentData, ComponentBackData, PieceData
from templative.lib.manage.models.composition import ComponentComposition
from templative.lib.manage.models.artdata import ComponentArtdata
from templative.lib.manage import defineLoader

from templative.lib.componentInfo import COMPONENT_INFO

from templative.lib.produce.customComponents.backProducer import BackProducer
from templative.lib.produce.customComponents.diceProducer import DiceProducer

async def getComponentArtdata(componentName, inputDirectoryPath, componentComposition) -> ComponentArtdata:
    artDatas = {}
    componentType = componentComposition.componentCompose["type"]
    for artDataTypeName in COMPONENT_INFO[componentType]["ArtDataTypeNames"]:
        artDataTypeFilepath = componentComposition.componentCompose["artdata%sFilename" % artDataTypeName]
        artData = await defineLoader.loadArtdata(inputDirectoryPath, componentComposition.gameCompose["artdataDirectory"], artDataTypeFilepath)
        if not artData or artData == None:
            print("Skipping %s component due to missing %s art metadata." % (componentName, artDataTypeName))
        artDatas[artDataTypeName] = artData
    
    return ComponentArtdata(artDatas)

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

    createdComponent = False
    if "Back" in componentArtdata.artDataBlobDictionary: 
        await BackProducer.createComponent(produceProperties, componentComposition, componentData, componentArtdata)

    elif "Front" in componentArtdata.artDataBlobDictionary and len(componentArtdata.artDataBlobDictionary) == 1:
        await DiceProducer.createComponent(produceProperties, componentComposition, componentData, componentArtdata)
    else:
        print("No production instructions for %s %s." % (componentComposition.componentCompose["type"], componentComposition.componentCompose["name"]))

    print("Creating art assets for %s component." % (componentName))


