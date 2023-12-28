import asyncclick as click
from templative.lib.manage.instructionsLoader import getLastOutputFileDirectory
from templative.lib.distribute.printout import createPdfForPrinting

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
