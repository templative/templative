import aiohttp
import asyncio
class GameCrafterSession:
    def __init__ (self, httpSession):
        self.httpSession = httpSession

    def login(self, sessionId, userId):
        self.sessionId = sessionId
        self.userId = userId