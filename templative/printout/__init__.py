import asyncclick as click
from PIL import Image
from os import path, walk
from json import dump, load
import math
from fpdf import FPDF
from templative.componentInfo import COMPONENT_INFO
from templative.gameManager.instructionsLoader import getLastOutputFileDirectory

printoutSizeType = "Letter"
marginsInches = 0.5
printoutPlayAreaInches = (8.5-(marginsInches*2), 11 - (marginsInches*2))
inchToPixelConversion = 96
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

@printout.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
async def frontback(input):
    """Create a pdf for printing on the front and back"""
    if input is None:
        input = await getLastOutputFileDirectory()
    await createPdfForPrinting(input, True)

async def createPdfForPrinting(producedDirectoryPath, printBack):
    pdf = FPDF("P", "in", "Letter")

    componentTypeFilepathAndQuantity = {}
    for directoryPath in next(walk(producedDirectoryPath))[1]:
        await loadFilepathsForComponent(componentTypeFilepathAndQuantity, producedDirectoryPath, directoryPath)
    
    for componentType in componentTypeFilepathAndQuantity.keys():
        createdPageImages = await createPageImagesForComponentTypeImages(componentType, componentTypeFilepathAndQuantity[componentType], printBack)
        await addPageImagesToPdf(pdf, createdPageImages)

    pdf.output("./printout.pdf", "F")

async def loadFilepathsForComponent(componentTypeFilepathAndQuantity, producedDirectoryPath, directoryPath):
    componentDirectoryPath = "%s/%s" % (producedDirectoryPath, directoryPath)
    componentInstructionsFilepath = path.join(componentDirectoryPath, "component.json")
    componentInstructionsFile = open(componentInstructionsFilepath, "r")
    componentInstructions = load(componentInstructionsFile)

    await collectFilepathQuantitiesForComponent(componentTypeFilepathAndQuantity, componentInstructions)
    componentInstructionsFile.close()

async def collectFilepathQuantitiesForComponent(componentTypeFilepathAndQuantity, componentInstructions):    
    if not componentInstructions["type"] in componentTypeFilepathAndQuantity:
        componentTypeFilepathAndQuantity[componentInstructions["type"]] = []

    for instruction in componentInstructions["frontInstructions"]:
        frontBack = {
            "filepath": instruction["filepath"],
            "backFilepath": componentInstructions["backInstructions"]["filepath"],
            "quantity":  int(instruction["quantity"]),

        }
        componentTypeFilepathAndQuantity[componentInstructions["type"]].append(frontBack)

async def addPageImagesToPdf(pdf, pageImages):
    for image in pageImages:
        pdf.add_page()
        pdf.image(image,marginsInches,marginsInches,printoutPlayAreaInches[0],printoutPlayAreaInches[1])

async def createPageImagesForComponentTypeImages(componentType, componentTypeImageList, printBack):
    if not componentType in COMPONENT_INFO:
        print("Missing %s in COMPONENT_INFO" % componentType)
        return []
    component = COMPONENT_INFO[componentType]

    if not "DimensionsInches" in component:
        print("Skipping %s because it's DimensionsInches isn't defined." %(componentType))
        return []
    componentSizeInches = component["DimensionsInches"]

    pieceSizeInches = (componentSizeInches[0] + pieceMarginInches, componentSizeInches[1] + pieceMarginInches)

    columns = math.floor(printoutPlayAreaInches[0] / pieceSizeInches[0])
    rows = math.floor(printoutPlayAreaInches[1] / pieceSizeInches[1])
    
    rotatedColumns = math.floor(printoutPlayAreaInches[0] / pieceSizeInches[1])
    rotatedRows = math.floor(printoutPlayAreaInches[1] / pieceSizeInches[0])

    isImageRotated = rotatedColumns*rotatedRows > columns*rows
    if isImageRotated:
        columns = rotatedColumns
        rows = rotatedRows
        pieceSizeInches = (pieceSizeInches[1], pieceSizeInches[0])
        componentSizeInches = (componentSizeInches[1], componentSizeInches[0])

    halfAreaPixels = (
        int((printoutPlayAreaInches[0] - (pieceSizeInches[0] * columns)) / 2 * inchToPixelConversion), 
        int((printoutPlayAreaInches[1] - (pieceSizeInches[1] * rows)) / 2 * inchToPixelConversion)
    )

    pageImages = await createBlankImagesForComponent(componentTypeImageList, columns, rows, printBack)
    
    resizedSizePixels = (
        int(componentSizeInches[0] * inchToPixelConversion), 
        int(componentSizeInches[1] * inchToPixelConversion)
    )

    pieceIndex = 0
    for f in range(len(componentTypeImageList)):
        instruction = componentTypeImageList[f]

        pieceImage = Image.open(instruction["filepath"])
        backImage = Image.open(instruction["backFilepath"])

        if isImageRotated:
            pieceImage = pieceImage.rotate(-90, expand=True)
            backImage = backImage.rotate(-90, expand=True)
        
        pieceImage = pieceImage.resize(resizedSizePixels)
        backImage = backImage.resize(resizedSizePixels)

        for _ in range(int(instruction["quantity"])):
            pageIndex = math.floor(pieceIndex / (columns*rows))
            frontBackPageIndex = pageIndex * (2 if printBack else 1)
            # print(pageIndex, len(pageImages))
            pageImage = pageImages[frontBackPageIndex]
            pieceIndexOnPage = pieceIndex - (pageIndex * columns * rows)
            xIndex = math.floor(pieceIndexOnPage % columns)
            yIndex = math.floor(pieceIndexOnPage / columns)
            position = (
                halfAreaPixels[0] + int(xIndex * pieceSizeInches[0] * inchToPixelConversion),
                halfAreaPixels[1] + int(yIndex * pieceSizeInches[1] * inchToPixelConversion)
            )
            pageImage.paste(pieceImage, position)

            if printBack:
                reversedYAxisXIndex = columns-1 - xIndex
                backPosition = (
                    halfAreaPixels[0] + int(reversedYAxisXIndex * pieceSizeInches[0] * inchToPixelConversion),
                    position[1]
                )
                pageImages[frontBackPageIndex+1].paste(backImage, backPosition)

            pieceIndex+=1

        pieceImage.close()
        backImage.close()

    return pageImages

async def createBlankImagesForComponent(imageFilepaths, columns, rows, printBack):
    whiteColorRGB = (240,240,240)

    totalCount = 0
    for instruction in imageFilepaths:
        totalCount += int(instruction["quantity"])

    itemsPerPage = columns * rows
    totalPages = math.ceil(totalCount/itemsPerPage) * (2 if printBack else 1)
    print("Because a page fits", columns*rows, "we need", totalPages, "(%s max)"%(columns*rows*totalPages), "to accomidate", totalCount * (2 if printBack else 1), "images", "frontback" if printBack else "")
    pageImages = []
    for _ in range(totalPages):
        imageSize = (int(printoutPlayAreaInches[0]*inchToPixelConversion), int(printoutPlayAreaInches[1]*inchToPixelConversion))
        createdImage = Image.new("RGB", imageSize, whiteColorRGB)
        pageImages.append(createdImage)

    return pageImages
