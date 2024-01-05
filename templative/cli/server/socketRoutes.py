import socketio
from templative.lib.produce import gameProducer 
from .emitPrintStatements import EmitPrintStatements

from templative.lib.distribute.gameCrafter.client import uploadGame
from templative.lib.distribute.gameCrafter.accountManagement import listGames, deletePageOfGames
from templative.lib.distribute.gameCrafter.util.gameCrafterSession import login, logout

sio = socketio.AsyncServer(cors_allowed_origins="*")

@sio.event
def connect(sid, environ):
    # print("connect ", sid)
    pass
@sio.event
def disconnect(sid):
    # print('disconnect ', sid)
    pass

@sio.on("upload")
async def upload(sid, data):
    username = data['username']
    if username == None:
        raise Exception("Missing username.")
    
    password = data['password']
    if password == None:
        raise Exception("Missing password.")
    
    apiKey = data['apiKey']
    if apiKey == None:
        raise Exception("Missing apiKey.")
    
    isPublish = data['isPublish']
    if isPublish == None:
        raise Exception("Missing isPublish.")
    
    isIncludingStock = data['isIncludingStock']
    if isIncludingStock == None:
        raise Exception("Missing isIncludingStock.")
    
    isAsync = data['isAsync']
    if isAsync == None:
        raise Exception("Missing isAsync.")
    
    isProofed = data['isProofed']
    if isProofed == None:
        raise Exception("Missing isProofed.")
    
    outputDirectorypath = data['outputDirectorypath']
    if outputDirectorypath == None:
        raise Exception("Missing outputDirectorypath.")
    
    session = await login(apiKey, username, password)

    if session is None:
        raise Exception("You must provide a Game Crafter session.")

    with EmitPrintStatements(sio, "printStatement"):
        await uploadGame(session, outputDirectorypath, isPublish, isIncludingStock, isAsync, isProofed)
    await logout(session)

@sio.on("produceGame")
async def produceGame(sid, data):
    isDebug = data['isDebug']
    isComplex = data['isComplex']
    componentFilter = 'componentFilter' in data and data['componentFilter'] or None
    language = data['language']
    directoryPath = data["directoryPath"]

    with EmitPrintStatements(sio, "printStatement"):
        await gameProducer.produceGame(directoryPath, componentFilter, not isComplex, not isDebug, language)