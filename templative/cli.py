import click
from templative.lib.gameCrafterClient import operations as gameCrafterClient
from templative.lib.gameManager import operations as gameManagerClient
from templative.lib.gameCrafterUpload import operations as gameCrafterUpload

@click.group()
def cli():
    """Tyrus Templative CLI"""
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
@click.option('-n', '--gameName', required=True, prompt='Game name', help='The name of the new game.')
@click.option('-d', '--designerId', default=-1, prompt='Designer id', help='The id of the game crafter designer creating the game.')
def create(gameName, designerId):
    """Create a game"""
    session = gameCrafterClient.login()
    gameCrafterClient.createGame(session, gameName, designerId)

@gamecrafter.group()
def upload():
    """Upload folders and files"""
    pass

@upload.command()
@click.option('-n', '--name', required=True, prompt='Folder name', help='The name of the new folder.')
@click.option('-f', '--id', default=-1, prompt='Parent id', help='The id of the parent folder. A default of -1 creates it at the user root.')
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
@click.option('-n', '--name', required=True, prompt='Folder name', help='The name of the new folder.')
@click.option('-f', '--folderId', required=True, prompt='Parent id', help='The id of the parent folder.')
def file(filepath, folderId):
    """Upload a file"""
    session = gameCrafterClient.login()
    uploadedFile = gameCrafterClient.uploadFile(session, filepath, folderId)
    print("Uploaded file %s under %s" % (uploadedFile["id"], folderId))  

@upload.command(name="ls")
@click.option('-f', '--folderId', default=-1, prompt='Parent id', help='The id of the folder. A default of -1 searches from the user root.')
@click.option('r', '--recursive', default=False, prompt='Recursive', help='Whether to list recursively.')
@click.option('--includeFiles', default=False, prompt='Include files', help='Whether to include files in the list.')
def listFolderChildren(folderId, recursive, includeFiles):
    """List the folder's contents"""
    print("listFolderChildren not implemented.")
    return
    session = gameCrafterClient.login()
    folder = None
    if id > 0:
        pass
    else:
        pass

@cli.command()
@click.option('-u/--no-upload', default=False, help='Whether to upload after the game is produced.')
@click.option('-c', default=None, help="Produce only a specific component by its name. Ignores disabled.")
def produce(u, c):
    """Produce the game in the current directory"""
    producedGame = gameManagerClient.produceGame(".", c)
    if(u):
        gameUploadUrl = gameCrafterUpload.uploadGame(producedGame)

@cli.command()
@click.option('-i', '--input', prompt='Input directory', help='The directory of the produced game.')
def upload(input):
    """Upload a produced game in a directory"""
    gameUploadUrl = gameCrafterUpload.uploadGame(input)

@cli.command()
def init():
    """Deprecated - Create the default game project here"""
    pass
    gameManagerClient.createTemplate()

if __name__ == '__main__':
    cli()