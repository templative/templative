import asyncclick as click
from templative.distribute.zettelkasten import zkCommands

@click.group()
async def zk():
    """Zettelkasten Commands"""
    pass

@zk.command()
async def toCsv():
    """Convert the perma files here to csv"""
    zkCommands.convertFilesToCsv()