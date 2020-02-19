import click
from lib.gameCrafterClient import operations as gameCrafterClient
from lib.pipelines import pipeline as pipelineClient
from lib.svgmanipulation import operations as svg

@click.group()
def cli():
    """The Tyrus Pipeline CLI"""
    pass

@cli.group()
def pipeline():
    """Utilize data entry to production pipelines"""
    pass

@pipeline.command()
def gameToGameCrafter():
    """ImageMagick to Game Crafter"""
    pass

@cli.group()
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

@cli.group()
def gameManager():
    """Manage game defines"""
    pass

@gameManager.command()
def produce():
    """Produce a game based on a directory"""
    pass