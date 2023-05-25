import asyncclick as click
from templative import gameManager, gameUploader, commands, zettelkasten, printout

@click.group()
async def cli():
    """Templative CLI"""
    pass

# Add "reduce complexity for youtube videos"
@cli.command()
@click.option('--name', default=None, help='The component to produce.')
@click.option('-s/-c', '--simple/--complex', default=False, required=False, type=bool, help='Whether complex information is shown. Used for videos.')
@click.option('-p/-d', '--publish/--debug', default=False, required=False, type=bool, help='Where debug information is included.')
async def produce(name, simple, publish):
    """Produce the game in the current directory"""
    await gameManager.produceGame(".", name, simple, publish)

@cli.command()
async def components():
    """Get a list of quantities of the game in the current directory"""
    await gameManager.listComponents(".")

@cli.command()
async def depth():
    """Get the depth of all components"""
    await gameManager.calculateComponentsDepth(".")

@cli.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
@click.option('-p/-d', '--publish/--debug', default=False, required=False, type=bool, help='Whether to treat this as the official release.')
async def upload(input, publish):
    """Upload a produced game in a directory"""
    await gameUploader.uploadGame(input, publish)

@cli.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
@click.option('-o', '--output', default=None, help='The Tabletop Playground packages directory. Such as "~/Library/Application Support/Epic/TabletopPlayground/Packages" or "C:\Program Files (x86)\Steam\steamapps\common\TabletopPlayground\TabletopPlayground\PersistentDownloadDir"')
async def playground(input,output):
    """Convert a produced game into a tabletop playground game"""    
    await gameUploader.convertToTabletopPlayground(input, output)

@cli.group()
async def rules():
    """Rules Commands"""
    pass

@rules.command()
async def toHtml():
    """Convert the rules markdown to html"""
    await gameManager.convertRulesMdToHtml(".")

@rules.command()
async def toTspans():
    """Convert the rules markdown to svg tspans"""
    await gameManager.convertRulesMdToSpans(".")

@cli.command()
async def init():
    """Create the default game project here"""
    await gameManager.createTemplate()

cli.add_command(commands.create)
cli.add_command(zettelkasten.zk)
cli.add_command(printout.printout)