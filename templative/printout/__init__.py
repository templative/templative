import asyncclick as click
from PIL import Image
from os import path, walk
from json import dump, load
import math
from fpdf import FPDF

from templative.gameUploader.instructionsLoader import getLastOutputFileDirectory

componentDimensions = {
    "PokerDeck": (2.5, 3.5),
    "MiniDeck": (1.75, 2.5),
    "MicroDeck": (1.25, 1.75),
    "MintTinDeck": (2.05, 3.43),
    "HexDeck": (3.75, 3.25),
}

printoutSizeType = "Letter"
marginsInches = 0.5
printoutPlayAreaInches = (8.5-(marginsInches*2), 11 - (marginsInches*2))
inchToPixelConversion = 80
pieceMarginInches = 0.11811 * 1/3

@click.group()
async def printout():
    """Create a prototyping printout of the game"""
    pass

@printout.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
async def front(input):
    """Create a pdf for printing on the front only"""

    if input is None:
        input = await getLastOutputFileDirectory()

    await createPdfForPrinting(input, False)

# @printout.command()
# @click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
# async def frontback(input):
#     """Create a pdf for printing on the front and back"""
#     if input is None:
#         input = await getLastOutputFileDirectory()

#     await createPdfForPrinting(input, True)

async def createPdfForPrinting(producedDirectoryPath, frontBack):
    pdf = FPDF("P", "in", "Letter")

    for directoryPath in next(walk(producedDirectoryPath))[1]:
        createdPageImages = await convertComponentDirectoryToPageImages(producedDirectoryPath, directoryPath)
        await addPageImagesToPdf(pdf, createdPageImages)

    pdf.output("./printout.pdf", "F")

async def convertComponentDirectoryToPageImages(producedDirectoryPath, directoryPath):
    componentDirectoryPath = "%s/%s" % (producedDirectoryPath, directoryPath)
    componentInstructionsFilepath = path.join(componentDirectoryPath, "component.json")
    componentInstructionsFile = open(componentInstructionsFilepath, "r")

    componentInstructions = load(componentInstructionsFile)
    createdPageImages = await createPageImagesFromPieceImages(componentInstructions)
    componentInstructionsFile.close()
    # print(componentInstructions["name"], "created", len(createdPageImages), "pages")
    return createdPageImages

async def addPageImagesToPdf(pdf, pageImages):
    for image in pageImages:
        pdf.add_page()
        pdf.image(image,marginsInches,marginsInches,printoutPlayAreaInches[0],printoutPlayAreaInches[1])

async def createPageImagesFromPieceImages(componentInstructions):
    if not componentInstructions["type"] in componentDimensions:
        print("Skipping unsupported %s named %s" %(componentInstructions["type"],componentInstructions["name"]))
        return []
    
    componentSize = componentDimensions[componentInstructions["type"]]
    pieceSizeInches = (componentSize[0] + pieceMarginInches, componentSize[1] + pieceMarginInches)

    columns = math.floor(printoutPlayAreaInches[0] / pieceSizeInches[0])
    rows = math.floor(printoutPlayAreaInches[1] / pieceSizeInches[1])
    pageImages = await createBlankImagesForComponent(componentInstructions, columns, rows)
    
    pieceIndex = 0
    for f in range(len(componentInstructions["frontInstructions"])):
        instruction = componentInstructions["frontInstructions"][f]

        pieceImage = Image.open(instruction["filepath"])
        resizedSize = (
            int(componentSize[0] * inchToPixelConversion), 
            int(componentSize[1] * inchToPixelConversion)
        )
        print(resizedSize, "pixels")
        pieceImage = pieceImage.resize(resizedSize)
        for _ in range(int(instruction["quantity"])):
            pageIndex = math.floor(pieceIndex / (columns*rows))
            pageImage = pageImages[pageIndex]
            pieceIndexOnPage = pieceIndex - (pageIndex * columns * rows)
            xIndex = math.floor(pieceIndexOnPage % columns)
            yIndex = math.floor(pieceIndexOnPage / columns)
            position = (
                int(xIndex * pieceSizeInches[0] * inchToPixelConversion),
                int(yIndex * pieceSizeInches[1] * inchToPixelConversion)
            )
            pageImage.paste(pieceImage, position)
            pieceIndex+=1

    return pageImages

async def createBlankImagesForComponent(componentInstructions, columns, rows):
    whiteColorRGB = (255,255,255)

    totalCount = 0
    for instruction in componentInstructions["frontInstructions"]:
        totalCount += int(instruction["quantity"])

    itemsPerPage = columns * rows
    totalPages = math.ceil(totalCount/itemsPerPage)
    # print("Because a page fits", columns*rows, "we need", totalPages, "to accomidate", totalCount, componentInstructions["name"], "pieces")
    pageImages = []
    for _ in range(totalPages):
        imageSize = (int(printoutPlayAreaInches[0]*inchToPixelConversion), int(printoutPlayAreaInches[1]*inchToPixelConversion))
        createdImage = Image.new("RGB", imageSize, whiteColorRGB)
        pageImages.append(createdImage)

    return pageImages
