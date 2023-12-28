from io import StringIO 
import sys
import asyncio

async def emit(sio, emitTarget, message):
    if message.isspace():
        return
    if message == "\n":
        return
    await sio.emit(emitTarget, message)

class EmitPrintStatements():
    def __init__(self, sio, emitTarget):
        self.sio = sio
        self.emitTarget = emitTarget

    def __enter__(self):
        self.oldStdOutWrite = sys.stdout.write
        def printAndPushToArray(message):
            self.oldStdOutWrite(message)
            asyncio.run_coroutine_threadsafe(emit(self.sio, self.emitTarget, message), loop=asyncio.get_event_loop())
        sys.stdout.write = printAndPushToArray

    def __exit__(self, *args):
        sys.stdout.write = self.oldStdOutWrite
