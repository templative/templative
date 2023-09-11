from .. import outputWriter
from . import svgscissors
import os 

from templative.manage.models.produceProperties import ProduceProperties
from templative.manage.models.gamedata import StudioData, GameData, ComponentData, ComponentBackData, PieceData
from templative.manage.models.composition import ComponentComposition
from templative.manage.models.artdata import ComponentArtdata
from templative.manage import defineLoader

from templative.componentInfo import COMPONENT_INFO

class Producer():   
    @staticmethod
    async def createComponent(produceProperties:ProduceProperties, componentComposition:ComponentComposition, componentData:ComponentData, componentArtdata:ComponentArtdata):
        raise NotImplemented("Not implemented")