import socketio
from templative.lib.produce import gameProducer 
from .emitPrintStatements import EmitPrintStatements

sio = socketio.AsyncServer(cors_allowed_origins="*")

@sio.event
def connect(sid, environ):
    # print("connect ", sid)
    pass
@sio.event
def disconnect(sid):
    # print('disconnect ', sid)
    pass

@sio.on("produceGame")
async def produceGame(sid, data):
    isDebug = data['isDebug']
    isComplex = data['isComplex']
    componentFilter = 'componentFilter' in data and data['componentFilter'] or None
    language = data['language']
    directoryPath = data["directoryPath"]

    with EmitPrintStatements(sio, "printStatement"):
        await gameProducer.produceGame(directoryPath, componentFilter, not isComplex, not isDebug, language)