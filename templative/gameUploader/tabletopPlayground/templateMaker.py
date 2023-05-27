from templative.gameUploader.tabletopPlayground.templates import board, card
from templative.componentInfo import COMPONENT_INFO
gameCrafterScaleToPlaygroundScale = 0.014

def createCardTemplate(guid, name, componentType, frontTextureName, totalCount, cardColumnCount, cardRowCount, backTextureName):
    if not componentType in COMPONENT_INFO:
        print("Missing component info for %s." % componentType)
        return
    
    component = COMPONENT_INFO[componentType]
    if not "DimensionsPixels" in component or not "PlaygroundThickness" in component:
        print("Missing playground info for %s." % componentType)
        return
    
    dimensions = (
        component["DimensionsPixels"][0] * gameCrafterScaleToPlaygroundScale, 
        component["DimensionsPixels"][1] * gameCrafterScaleToPlaygroundScale, 
        component["PlaygroundThickness"])
    
    indices = []
    for i in range(totalCount):
        indices.append(i)

    return card.createCard(guid, name, frontTextureName, backTextureName, cardColumnCount, cardRowCount, dimensions, indices)

def createBoardTemplate(guid, name, componentType, frontTextureName, backTextureName):
    if not componentType in COMPONENT_INFO:
        print("Missing component info for %s." % componentType)
        return
    
    component = COMPONENT_INFO[componentType]
    if not "DimensionsPixels" in component or not "PlaygroundThickness" in component:
        print("Missing playground info for %s." % componentType)
        return
    
    scaleDown = gameCrafterScaleToPlaygroundScale / 53 * 1.5
    dimensions = (
        component["DimensionsPixels"][0] * scaleDown,
        component["DimensionsPixels"][1] * scaleDown
    )

    return board.createBoard(guid, name, frontTextureName, backTextureName, dimensions)
