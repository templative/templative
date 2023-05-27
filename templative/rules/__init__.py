import asyncclick as click
from templative.gameManager import componentProcessor
from templative.gameManager.instructionsLoader import getLastOutputFileDirectory

@click.group()
async def rules():
    """Rules Commands"""
    pass

@rules.command()
@click.option('-i', '--input', default="./", help='The directory of the produced game. Defaults to last produced directory.')
async def toHtml(input):
    """Convert the rules markdown to html"""
    await componentProcessor.convertRulesMdToHtml(input)

@rules.command()
@click.option('-i', '--input', default="./", help='The directory of the produced game. Defaults to last produced directory.')
async def toTspans(input):
    """Convert the rules markdown to svg tspans"""
    await componentProcessor.convertRulesMdToSpans(input)