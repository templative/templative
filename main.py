import click
import tcgClient
from lib.gameCrafterClient import operations as gameCrafterOperations

@click.group()
def tyrus():
    """Main application portal"""
    pass

@tyrus.group()
def pipeline():
    """Utilize data entry to production pipelines"""
    pass

@tyrus.group()
def template():
    """Manage row templates to art assets"""
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
    gameCrafterOperations.getGames()

if __name__ == '__main__':
    tyrus()