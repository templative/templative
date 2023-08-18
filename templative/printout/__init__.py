import asyncclick as click
from PIL import Image
from os import path, walk
from json import dump, load
import math
from fpdf import FPDF
from templative.componentInfo import COMPONENT_INFO
from templative.gameManager.instructionsLoader import getLastOutputFileDirectory

marginsInches = 0.5 # or 0.25
inchToPixelConversion = 96
pieceMarginInches = 0.11811 * 1/3

@click.group()
async def printout():
    """Create a prototyping printout of the game"""
    pass

@printout.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
@click.option('-s', '--size', default="Letter", help='The size of the file, either `Letter` or `Tabloid`.')
async def front(input, size):
    """Create a pdf for printing on the front only"""
    if input is None:
        input = await getLastOutputFileDirectory()

    if size != "Letter" and size != "Tabloid":
        print("You must choose either `Letter` or `Tabloid` for size.")
        return

    await createPdfForPrinting(input, False, size)

@printout.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
@click.option('-s', '--size', default="Letter", help='The size of the file, either `Letter` or `Tabloid`.')
async def frontback(input, size):
    """Create a pdf for printing on the front and back"""
    if input is None:
        input = await getLastOutputFileDirectory()

    if size != "Letter" and size != "Tabloid":
        print("You must choose either `Letter` or `Tabloid` for size.")
        return
    
    await createPdfForPrinting(input, True, size)

async def createPdfForPrinting(producedDirectoryPath, isBackIncluded, size):
    fpdfSizes = {
        "Letter": "letter",
        "Tabloid": "a3",
    }
    if not size in fpdfSizes:
        print("Cannot create size %s." % size)
        return
    
    pdf = FPDF("P", "in", fpdfSizes[size])

    componentTypeFilepathAndQuantity = {}
    for directoryPath in next(walk(producedDirectoryPath))[1]:
        await loadFilepathsForComponent(componentTypeFilepathAndQuantity, producedDirectoryPath, directoryPath)
    
    printoutPlayAreaChoices = {
        "Letter": (8.5-(marginsInches*2), 11-(marginsInches*2)),
        "Tabloid": (11-(marginsInches*2), 17-(marginsInches*2))
    }

    if not size in printoutPlayAreaChoices:
        print("Cannot create size %s." % size)
        return
    
    printoutPlayAreaChoice = printoutPlayAreaChoices[size]

    for componentType in componentTypeFilepathAndQuantity.keys():
        createdPageImages = await createPageImagesForComponentTypeImages(componentType, componentTypeFilepathAndQuantity[componentType], isBackIncluded, printoutPlayAreaChoice)
        await addPageImagesToPdf(pdf, createdPageImages, printoutPlayAreaChoice)

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
    
    if "STOCK_" in componentInstructions["type"]:
        return 

    if not "frontInstructions" in componentInstructions:
        print("Skipping %s for lacking frontInstructions" % componentInstructions["name"])
        return

    for instruction in componentInstructions["frontInstructions"]:
        frontBack = {
            "filepath": instruction["filepath"],
            "backFilepath": componentInstructions["backInstructions"]["filepath"],
            "quantity":  int(instruction["quantity"]),

        }
        componentTypeFilepathAndQuantity[componentInstructions["type"]].append(frontBack)

async def addPageImagesToPdf(pdf, pageImages, printoutPlayAreaInches):
    for image in pageImages:
        pdf.add_page()
        pdf.image(image,marginsInches,marginsInches,printoutPlayAreaInches[0],printoutPlayAreaInches[1])

async def createPageImagesForComponentTypeImages(componentType, componentTypeImageList, printBack, printoutPlayAreaInches):
    if "STOCK_" in componentType:
        return []

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
    if rows == 0 or columns == 0:
        print("Skipping the %sx%s\" %s as it's too large for a %sx%s\" print space." % (pieceSizeInches[0], pieceSizeInches[1], componentType, printoutPlayAreaInches[0], printoutPlayAreaInches[1]))
        return []
    
    halfAreaPixels = (
        int((printoutPlayAreaInches[0] - (pieceSizeInches[0] * columns)) / 2 * inchToPixelConversion), 
        int((printoutPlayAreaInches[1] - (pieceSizeInches[1] * rows)) / 2 * inchToPixelConversion)
    )

    pageImages = await createBlankImagesForComponent(componentTypeImageList, columns, rows, printBack, printoutPlayAreaInches)
    
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

async def createBlankImagesForComponent(imageFilepaths, columns, rows, printBack, printoutPlayAreaInches):
    whiteColorRGB = (240,240,240)

    if columns == 0 or rows == 0:
        raise Exception("Rows and columns must be non zero.")

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
