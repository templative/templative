from templative.gameManager import componentProcessor
import asyncclick as click

@click.group()
async def rules():
    """Rules Commands"""
    pass

@rules.command()
async def toHtml():
    """Convert the rules markdown to html"""
    await componentProcessor.convertRulesMdToHtml(gameRootDirectoryPath)

@rules.command()
async def toTspans():
    """Convert the rules markdown to svg tspans"""
    await componentProcessor.convertRulesMdToSpans(gameRootDirectoryPath)