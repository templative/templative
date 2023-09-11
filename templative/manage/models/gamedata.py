class StudioData:
    def __init__(self, studioDataBlob):
        self.studioDataBlob = studioDataBlob

class GameData(StudioData):
    def __init__(self, studioDataBlob, gameDataBlob):
        super().__init__(studioDataBlob)
        self.gameDataBlob = gameDataBlob

class ComponentData(GameData):
    def __init__(self, studioDataBlob, gameDataBlob, componentDataBlob):
        super().__init__(studioDataBlob, gameDataBlob)
        self.componentDataBlob = componentDataBlob

class ComponentBackData(ComponentData):
    def __init__(self, studioDataBlob, gameDataBlob, componentDataBlob, componentBackDataBlob={}, sourcedVariableNamesSpecificToPieceOnBackArtData=[], pieceUniqueBackHash=""):
        super().__init__(studioDataBlob, gameDataBlob, componentDataBlob)
        self.componentBackDataBlob = componentBackDataBlob
        self.pieceUniqueBackHash = pieceUniqueBackHash
        self.sourcedVariableNamesSpecificToPieceOnBackArtData = sourcedVariableNamesSpecificToPieceOnBackArtData

class PieceData(ComponentBackData):
    def __init__(self, studioDataBlob, gameDataBlob, componentDataBlob, componentBackDataBlob, sourcedVariableNamesSpecificToPieceOnBackArtData, pieceUniqueBackHash, pieceDataBlob):
        super().__init__(studioDataBlob, gameDataBlob,  componentDataBlob, componentBackDataBlob, sourcedVariableNamesSpecificToPieceOnBackArtData, pieceUniqueBackHash)
        self.pieceData = pieceDataBlob

