import click
import tcgClient
from lib.gameCrafterClient import operations as gameCrafterOperations

@click.group()
def tyrus():
    """Main application portal"""
    pass

@tyrus.group()
def gamecrafter():
    """Manages game crafter assets"""
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