import asyncclick as click
from . import rulesMdToViewsProcessor

@click.group()
async def rules():
    """Rules Commands"""
    pass

@rules.command()
@click.option('-i', '--input', default="./", help='The directory of the produced game. Defaults to last produced directory.')
async def toHtml(input):
    """Convert the rules markdown to html"""
    await rulesMdToViewsProcessor.convertRulesMdToHtml(input)

@rules.command()
@click.option('-i', '--input', default="./", help='The directory of the produced game. Defaults to last produced directory.')
async def toTspans(input):
    """Convert the rules markdown to svg tspans"""
    await rulesMdToViewsProcessor.convertRulesMdToSpans(input)