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

@gamecrafter.group()
def upload():
    """Upload folders and files"""
    pass

@upload.command()
@click.option('--name', required=True, prompt='Folder name', help='The name of the new folder.')
@click.option('--id', default=-1, prompt='Parent id', help='The id of the parent folder. A default of -1 creates it at the user root.')
def folder(name, id):
    """Upload a folder"""
    session = gameCrafterClient.login()
    folder = None
    if id > 0:
        folder = gameCrafterClient.createFolderAtParent(session, name, id)
        print("Created folder %s under parent %s" % (folder["id"], folder["parent_id"]))
    else:
        folder = gameCrafterClient.createFolderAtRoot(session, name)
        print("Created folder %s under users root directory %s" % (folder["id"], folder["parent_id"]))

@upload.command()
@click.option('--name', required=True, prompt='Folder name', help='The name of the new folder.')
@click.option('--folderId', required=True, prompt='Parent id', help='The id of the parent folder.')
def file(filepath, folderId):
    """Upload a file"""
    session = gameCrafterClient.login()
    uploadedFile = gameCrafterClient.uploadFile(session, filepath, folderId)
    print("Uploaded file %s under %s" % (uploadedFile["id"], folderId))  

@cli.command()
def produce():
    """Produce a game based on a directory"""
    producedGame = gameManagerClient.produceGame(".", "./output")