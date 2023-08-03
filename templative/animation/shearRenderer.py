from wand.image import Image
import math
import json
from aiofile import AIOFile
from templative.componentInfo import COMPONENT_INFO
from templative.stockComponentInfo import STOCK_COMPONENT_INFO

async def renderShearInstructions(shearInstructions, lastOutputtedDirectory):
    canvas = Image(width=math.floor(1920), height=math.floor(1080), background="Black")

    i = 0
    for i in range(len(shearInstructions)): 
        fileNameTokens = shearInstructions[i].split("_")
        componentName = fileNameTokens[0]
        frontInsturctionsFilepath = path.join(lastOutputtedDirectory, componentName, "component.json")
        
        if not path.exists(frontInsturctionsFilepath):
            print("%s does not exist." % frontInsturctionsFilepath)
            continue

        componentRenderingInstructions = None
        async with AIOFile(frontInsturctionsFilepath) as componentFile:
            componentRenderingInstructions = json.loads(await componentFile.read())
        
        pieceName = fileNameTokens[1]
        
        pieceRenderingInstructions = None
        for somePieceRenderingInstruction in componentRenderingInstructions["frontInstructions"]:
            if somePieceRenderingInstruction["name"] != pieceName:
                continue
            pieceRenderingInstructions = somePieceRenderingInstruction
            break
        if pieceRenderingInstructions == None:
            print("%s not in %s." % (pieceName, componentName))
            continue
        pieceImage = Image(filename=pieceRenderingInstructions["filepath"])
        pieceImage.resize(width=math.floor(pieceImage.width/4), height=math.floor(pieceImage.height/4))
        x = i % 3
        y = math.floor(i / 3)
        padding = 5
        canvas.composite(pieceImage,left=(x*pieceImage.width) + (x*padding),top=(y*pieceImage.height) + (y*padding))
        pieceImage.close()

    canvas.shear('Black', 30, 15)
    canvas.save(filename="./shear.png")
    canvas.close()