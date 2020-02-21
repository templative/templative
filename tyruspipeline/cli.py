import click
from lib.gameCrafterClient import operations as gameCrafterClient
import lib.gameManager as gameManagerClient

@click.group()
def cli():
    """The Tyrus Pipeline CLI"""
    pass

@cli.group()
def gamecrafter():
    """Manage game crafter assets"""
    pass

@gamecrafter.command()
def ls():
    """List all games"""
    pass

@gamecrafter.command()
def create():
    """Create a game"""
    gameCrafterClient.createGame("Gamerino")

@cli.command()
def produce():
    """Produce a game based on a directory"""
    producedGame = gameManagerClient.produceGame(".", "./output")