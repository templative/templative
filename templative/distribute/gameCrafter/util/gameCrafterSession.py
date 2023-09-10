import os
import aiohttp
from templative.distribute.gameCrafter.util import httpOperations

class GameCrafterSession:
    def __init__ (self, httpSession):
        self.httpSession = httpSession

    def login(self, sessionId, userId):
        self.sessionId = sessionId
        self.userId = userId

async def login():
    publicApiKey = os.environ.get('THEGAMECRAFTER_PUBLIC_KEY')
    if not publicApiKey:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PUBLIC_KEY. Value is %s' % publicApiKey)

    userName = os.environ.get('THEGAMECRAFTER_USER')
    if not userName:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_USER. Value is %s' % userName)

    userPassword = os.environ.get('THEGAMECRAFTER_PASSWORD')
    if not userPassword:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PASSWORD. Value is %s' % userPassword)

    gameCrafterSession = GameCrafterSession(aiohttp.ClientSession())
    login = await httpOperations.login(gameCrafterSession, publicApiKey, userName, userPassword)
    gameCrafterSession.login(sessionId=login["id"], userId=login["user_id"])
    return gameCrafterSession

async def logout(gameCrafterSession):
    await httpOperations.logout(gameCrafterSession)