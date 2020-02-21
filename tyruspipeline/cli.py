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

@gamecrafter.group()
def designers():
    """Manage designers"""
    pass

@designers.command(name="ls")
def listDesigners():
    """List designers"""
    session = gameCrafterClient.login()
    gameCrafterClient.listDesigners(session)

@gamecrafter.group()
def games():
    """Manage games"""
    pass

@games.command(name="ls")
def listGames():
    """List games"""
    session = gameCrafterClient.login()
    gameCrafterClient.listGames(session)

@games.command()
def create():
    """Create a game"""
    session = gameCrafterClient.login()
    gameCrafterClient.createGame(session, "Gamerino")

@cli.command()
def produce():
    """Produce a game based on a directory"""
    producedGame = gameManagerClient.produceGame(".", "./output")