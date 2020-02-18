import click
from lib.gameCrafterClient import operations as gameCrafterClient
import lib.sheets as sheetsClient
from lib.pipelines import pipeline as pipelineClient
from lib.svgmanipulation import operations as svg

@click.group()
def tyrus():
    """The Tyrus Pipeline CLI"""
    pass

@tyrus.group()
def pipeline():
    """Utilize data entry to production pipelines"""
    pass

@pipeline.command()
def magickCraft():
    """ImageMagick to Game Crafter"""
    pass


@tyrus.group()
def sheets():
    """Manage Google Sheets"""
    pass

@sheets.command()
def sheetsSample():
    """Get sample sheet value"""
    sheetsClient.getSample()

@sheets.command()
def download():
    """Download a sheet"""
    pass

@tyrus.group()
def gamecrafter():
    """Manage game crafter assets"""
    pass

@gamecrafter.group()
def games():
    """Manage games"""
    pass

@games.command()
def ls():
    """List all games"""
    gameCrafterClient.getGames()

@tyrus.group()
def svgmanip():
    """Utilize SVG Manipulation"""
    pass

@svgmanip.command()
def createDemoCard():
    """Create a demo card"""
    demoCard = svg.createDemoCard()

if __name__ == '__main__':
    tyrus()