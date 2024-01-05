import os
import aiohttp
from templative.lib.distribute.gameCrafter.util import httpOperations

class GameCrafterSession:
    def __init__ (self, httpSession):
        self.httpSession = httpSession

    def login(self, sessionId, userId):
        self.sessionId = sessionId
        self.userId = userId

async def login(publicApiKey, userName, userPassword):
    gameCrafterSession = GameCrafterSession(aiohttp.ClientSession())
    login = await httpOperations.login(gameCrafterSession, publicApiKey, userName, userPassword)
    gameCrafterSession.login(sessionId=login["id"], userId=login["user_id"])
    return gameCrafterSession

async def logout(gameCrafterSession):
    await httpOperations.logout(gameCrafterSession)