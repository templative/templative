import asyncclick as click
from PIL import Image, ImageDraw 
from os import path, walk
from json import dump, load
import math
from fpdf import FPDF
from templative.componentInfo import COMPONENT_INFO
from templative.manage.instructionsLoader import getLastOutputFileDirectory

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
@click.option('-m/-n', '--margins/--nomargins', default=False, required=False, type=bool, help='Whether to treat this as the official release.')
async def front(input, size, margins):
    """Create a pdf for printing on the front only"""
    if input is None:
        input = await getLastOutputFileDirectory()

    if size != "Letter" and size != "Tabloid":
        print("You must choose either `Letter` or `Tabloid` for size.")
        return

    await createPdfForPrinting(input, False, size, margins)

@printout.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
@click.option('-s', '--size', default="Letter", help='The size of the file, either `Letter` or `Tabloid`.')
@click.option('-m/-n', '--margins/--nomargins', default=False, required=False, type=bool, help='Whether to treat this as the official release.')
async def frontback(input, size, margins):
    """Create a pdf for printing on the front and back"""
    if input is None:
        input = await getLastOutputFileDirectory()

    if size != "Letter" and size != "Tabloid":
        print("You must choose either `Letter` or `Tabloid` for size.")
        return
    
    await createPdfForPrinting(input, True, size, margins)

async def createPdfForPrinting(producedDirectoryPath, isBackIncluded, size, areMarginsIncluded):
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
        createdPageImages = await createPageImagesForComponentTypeImages(componentType, componentTypeFilepathAndQuantity[componentType], isBackIncluded, printoutPlayAreaChoice, areMarginsIncluded)
        await addPageImagesToPdf(pdf, componentType, createdPageImages, printoutPlayAreaChoice)

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

async def addPageImagesToPdf(pdf, componentType, pageImages, printoutPlayAreaInches):
    for image in pageImages:
        pdf.add_page()
        pdf.line(1,0,1,1)
        pdf.image(image,marginsInches,marginsInches,printoutPlayAreaInches[0],printoutPlayAreaInches[1])

async def createPageImagesForComponentTypeImages(componentType, componentTypeImageList, printBack, printoutPlayAreaInches, areMarginsIncluded):
    if "STOCK_" in componentType:
        return []

    if not componentType in COMPONENT_INFO:
        print("Missing %s in COMPONENT_INFO" % componentType)
        return []
    componentInfo = COMPONENT_INFO[componentType]

    if not "DimensionsInches" in componentInfo:
        print("Skipping %s because it's DimensionsInches isn't defined." %(componentType))
        return []
    
    dimensionsPixels = componentInfo["DimensionsPixels"]
    componentSizeInches = componentInfo["DimensionsInches"]

    marginsPixels = componentInfo["MarginsPixels"] if (areMarginsIncluded and "MarginsPixels" in componentInfo) else None
    if marginsPixels != None:
        sizeOfContentPixels = (dimensionsPixels[0]-(marginsPixels[0]*2), dimensionsPixels[1]-(marginsPixels[1]*2))
        accountForMarginsFactor = (dimensionsPixels[0]/sizeOfContentPixels[0], dimensionsPixels[1]/sizeOfContentPixels[1])
        componentSizeInches = (componentSizeInches[0] * accountForMarginsFactor[0], componentSizeInches[1] * accountForMarginsFactor[1])

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

    totalImagesDrawn = 0
    for f in range(len(componentTypeImageList)):
        instruction = componentTypeImageList[f]
        imagesDrawnCount = await drawPieceForQuantities(pageImages, instruction, totalImagesDrawn, printBack, columns, rows, isImageRotated, resizedSizePixels, halfAreaPixels, pieceSizeInches, dimensionsPixels, marginsPixels)
        totalImagesDrawn += imagesDrawnCount

    return pageImages

async def drawPieceForQuantities(pageImages, instruction, totalImagesDrawn, printBack, columns, rows, isImageRotated, resizedSizePixels, halfAreaPixels, pieceSizeInches, dimensionsPixels, marginsPixels):
    frontImage = Image.open(instruction["filepath"])
    backImage = Image.open(instruction["backFilepath"])

    if isImageRotated:
        frontImage = frontImage.rotate(-90, expand=True)
        backImage = backImage.rotate(-90, expand=True)
    
    frontImage = frontImage.resize(resizedSizePixels)
    backImage = backImage.resize(resizedSizePixels)

    pieceIndex = totalImagesDrawn
    marginsToDimensionsRatio = (marginsPixels[0]/dimensionsPixels[0], marginsPixels[1]/dimensionsPixels[1]) if marginsPixels != None else None

    for _ in range(int(instruction["quantity"])):
        await drawPiece(pageImages, frontImage, backImage, pieceIndex, printBack, columns, rows, resizedSizePixels, halfAreaPixels, pieceSizeInches, isImageRotated, marginsToDimensionsRatio)
        pieceIndex += 1

    frontImage.close()
    backImage.close()
    imagesDrawnCount = int(instruction["quantity"])
    return imagesDrawnCount

async def drawPiece(pageImages, frontImage, backImage, pieceIndex, printBack, columns, rows, resizedSizePixels, halfAreaPixels, pieceSizeInches, isImageRotated, marginsToDimensionsRatio):
    
    pageIndex = math.floor(pieceIndex / (columns*rows))
    frontBackPageIndex = pageIndex * (2 if printBack else 1)
    
    pageImage = pageImages[frontBackPageIndex]
    pieceIndexOnPage = pieceIndex - (pageIndex * columns * rows)
    xIndex = math.floor(pieceIndexOnPage % columns)
    yIndex = math.floor(pieceIndexOnPage / columns)
    position = (
        halfAreaPixels[0] + int(xIndex * pieceSizeInches[0] * inchToPixelConversion),
        halfAreaPixels[1] + int(yIndex * pieceSizeInches[1] * inchToPixelConversion)
    )

    pageImage.paste(frontImage, position)

    if marginsToDimensionsRatio != None:
        await createGuidesForPiece(pageImage, position, resizedSizePixels, isImageRotated, marginsToDimensionsRatio)    

    if printBack:
        reversedYAxisXIndex = columns-1 - xIndex
        backPosition = (
            halfAreaPixels[0] + int(reversedYAxisXIndex * pieceSizeInches[0] * inchToPixelConversion),
            position[1]
        )
        pageImages[frontBackPageIndex+1].paste(backImage, backPosition)

async def createGuidesForPiece(pageImage, position, size, isImageRotated, marginsToDimensionsRatio):
    if isImageRotated:
        marginsToDimensionsRatio = (marginsToDimensionsRatio[1], marginsToDimensionsRatio[0])

    lineLength = 6

    topVerticalLeft = (position[0] + (size[0]*marginsToDimensionsRatio[0]), position[1])
    await drawLine(pageImage, topVerticalLeft[0], topVerticalLeft[1], topVerticalLeft[0], topVerticalLeft[1]+lineLength)

    topVerticalRight = (position[0] + size[0] - (size[0]*marginsToDimensionsRatio[0]), position[1])
    await drawLine(pageImage, topVerticalRight[0], topVerticalRight[1], topVerticalRight[0], topVerticalRight[1]+lineLength)

    leftHorizontalTop = (position[0], position[1] + (size[1]*marginsToDimensionsRatio[1]))
    await drawLine(pageImage, leftHorizontalTop[0], leftHorizontalTop[1], leftHorizontalTop[0]+lineLength, leftHorizontalTop[1])

    leftHorizontalBottom = (position[0], position[1] + size[1] - (size[1]*marginsToDimensionsRatio[1]))
    await drawLine(pageImage, leftHorizontalBottom[0], leftHorizontalBottom[1], leftHorizontalBottom[0]+lineLength, leftHorizontalBottom[1])

    bottomVerticalLeft = (position[0] + (size[0]*marginsToDimensionsRatio[0]), position[1]+ size[1])
    await drawLine(pageImage, bottomVerticalLeft[0], bottomVerticalLeft[1], bottomVerticalLeft[0], bottomVerticalLeft[1]-lineLength)

    bottomVerticalRight = (position[0] + size[0] - (size[0]*marginsToDimensionsRatio[0]), position[1] + size[1])
    await drawLine(pageImage, bottomVerticalRight[0], bottomVerticalRight[1], bottomVerticalRight[0], bottomVerticalRight[1]-lineLength)

    rightHorizontalTop = (position[0] + size[0], position[1] + (size[1]*marginsToDimensionsRatio[1]))
    await drawLine(pageImage, rightHorizontalTop[0], rightHorizontalTop[1], rightHorizontalTop[0]-lineLength, rightHorizontalTop[1])

    rightHorizontalBottom = (position[0] + size[0], position[1] + size[1] - (size[1]*marginsToDimensionsRatio[1]))
    await drawLine(pageImage, rightHorizontalBottom[0], rightHorizontalBottom[1], rightHorizontalBottom[0]-lineLength, rightHorizontalBottom[1])

async def drawLine(image, hereX, hereY, thereX, thereY):
    lineImage = ImageDraw.Draw(image)   
    lineImage.line([(hereX, hereY), (thereX, thereY)], fill ="green", width = 2)

async def createBlankImagesForComponent(imageFilepaths, columns, rows, printBack, printoutPlayAreaInches):
    whiteColorRGB = (255,255,255)

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
