import click
# from lib.gameCrafterClient import operations as gameCrafterClient
import lib.gameManager as gameManagerClient

@click.group()
def cli():
    """The Tyrus Pipeline CLI"""
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
    pass

@cli.group()
def gameManager():
    """Manage game defines"""
    pass

@gameManager.command()
def produce():
    """Produce a game based on a directory"""
    producedGame = gameManagerClient.produceGame(".", "./output")