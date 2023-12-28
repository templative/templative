from .. import outputWriter
from . import svgscissors
import os 

from templative.lib.manage.models.produceProperties import ProduceProperties
from templative.lib.manage.models.gamedata import StudioData, GameData, ComponentData, ComponentBackData, PieceData
from templative.lib.manage.models.composition import ComponentComposition
from templative.lib.manage.models.artdata import ComponentArtdata
from templative.lib.manage import defineLoader

from templative.lib.componentInfo import COMPONENT_INFO

class Producer():   
    @staticmethod
    async def createComponent(produceProperties:ProduceProperties, componentComposition:ComponentComposition, componentData:ComponentData, componentArtdata:ComponentArtdata):
        raise NotImplemented("Not implemented")