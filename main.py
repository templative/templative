import click
from lib.gameCrafterClient import operations as gameCrafterClient
from lib.illustratorClient import illustrator as illustratorClient
from lib.sheetsClient import sheets as sheetsClient
from lib.templateManagement import templates as templatesClient
from lib.pipelines import pipeline as pipelineClient

@click.group()
def tyrus():
    """The Tyrus Pipeline CLI"""
    pass

@tyrus.group()
def pipeline():
    """Utilize data entry to production pipelines"""
    pass

@tyrus.group()
def template():
    """Convert row templates to art assets"""
    pass

@pipeline.command()
def sheetIllCraft():
    """Sheet through Illustrator to Game Crafter"""
    pass

@tyrus.group()
def sheets():
    """Manage Google Sheets"""
    pass

@sheets.command()
def sample():
    """Get sample sheet value"""
    sheetsClient.getSample()

@sheets.command()
def download():
    """Download a sheet"""
    pass

@tyrus.group()
def illustrator():
    """Utilize Illustrator"""
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

if __name__ == '__main__':
    tyrus()