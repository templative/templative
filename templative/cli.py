import click
import asyncio
from .lib import gamecrafterclient as gameCrafterClient
from .lib import gameManager as gameManagerClient
from .lib import gameCrafterUpload as gameCrafterUpload
from functools import wraps

def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper

@click.group()
def cli():
    """Tyrus Templative CLI"""
    pass

@cli.group()
async def gamecrafter():
    """Manage game crafter assets"""
    pass

@gamecrafter.group()
async def designers():
    """Manage designers"""
    pass

@designers.command(name="ls")
async def listDesigners():
    """List designers"""
    session = await gameCrafterClient.login()
    await gameCrafterClient.listDesigners(session)

@gamecrafter.group()
async def games():
    """Manage games"""
    pass

@games.command(name="ls")
async def listGames():
    """List games"""
    session = await gameCrafterClient.login()
    await gameCrafterClient.listGames(session)

@games.command()
@click.option('-n', '--gameName', required=True, prompt='Game name', help='The name of the new game.')
@click.option('-d', '--designerId', default=-1, prompt='Designer id', help='The id of the game crafter designer creating the game.')
async def create(gameName, designerId):
    """Create a game"""
    session = await gameCrafterClient.login()
    await gameCrafterClient.createGame(session, gameName, designerId)

@gamecrafter.group()
async def upload():
    """Upload folders and files"""
    pass

@upload.command()
@click.option('-n', '--name', required=True, prompt='Folder name', help='The name of the new folder.')
@click.option('-f', '--id', default=-1, prompt='Parent id', help='The id of the parent folder. A default of -1 creates it at the user root.')
async def folder(name, id):
    """Upload a folder"""
    session = await gameCrafterClient.login()
    folder = None
    if id > 0:
        folder = await gameCrafterClient.createFolderAtParent(session, name, id)
        print("Created folder %s under parent %s" % (folder["id"], folder["parent_id"]))
    else:
        folder = await gameCrafterClient.createFolderAtRoot(session, name)
        print("Created folder %s under users root directory %s" % (folder["id"], folder["parent_id"]))

@upload.command()
@click.option('-n', '--name', required=True, prompt='Folder name', help='The name of the new folder.')
@click.option('-f', '--folderId', required=True, prompt='Parent id', help='The id of the parent folder.')
async def file(filepath, folderId):
    """Upload a file"""
    session = await gameCrafterClient.login()
    uploadedFile = await gameCrafterClient.uploadFile(session, filepath, folderId)
    print("Uploaded file %s under %s" % (uploadedFile["id"], folderId))  

@upload.command(name="ls")
@click.option('-f', '--folderId', default=-1, prompt='Parent id', help='The id of the folder. A default of -1 searches from the user root.')
@click.option('r', '--recursive', default=False, prompt='Recursive', help='Whether to list recursively.')
@click.option('--includeFiles', default=False, prompt='Include files', help='Whether to include files in the list.')
async def listFolderChildren(folderId, recursive, includeFiles):
    """List the folder's contents"""
    print("listFolderChildren not implemented.")
    return
    session = await gameCrafterClient.login()
    folder = None
    if id > 0:
        pass
    else:
        pass


@cli.command()
@coro
@click.option('-u/--no-upload', default=False, help='Whether to upload after the game is produced.')
@click.option('-c', default=None, help="Produce only a specific component by its name. Ignores disabled.")
async def produce(u, c, _anyio_backend="asyncio"):
    """Produce the game in the current directory"""
    producedGame = await gameManagerClient.produceGame(".", c)
    if(u):
        session = await gameCrafterClient.login()
        gameUploadUrl = await gameCrafterUpload.uploadGame(session, producedGame)
        await gameCrafterClient.logout(session)

@cli.command()
@coro
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
async def upload(input):
    """Upload a produced game in a directory"""
    session = await gameCrafterClient.login()
    gameUploadUrl = await gameCrafterUpload.uploadGame(session, input)
    await gameCrafterClient.logout(session)

@cli.command()
async def init():
    """Deprecated - Create the default game project here"""
    print("Init is not implemented.")
    pass
    await gameManagerClient.createTemplate()

if __name__ == '__main__':
    cli()