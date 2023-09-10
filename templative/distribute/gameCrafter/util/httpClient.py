import json
from pprint import pprint

async def post(gameCrafterSession, url, **kwargs):
    async with gameCrafterSession.httpSession.post(url, data=kwargs) as response:
        return await handleResponse(url, response, **kwargs)

async def get(gameCrafterSession, url, **kwargs):
    async with gameCrafterSession.httpSession.get(url, params=kwargs) as response:
        return await handleResponse(url, response, **kwargs)

async def delete(gameCrafterSession, url, **kwargs):
    async with gameCrafterSession.httpSession.delete(url, params=kwargs) as response:
        return await handleResponse(url, response, **kwargs)

async def handleResponse(url, response, **kwargs):
    statusCode = str(response.status)
    responseText = await response.text()
    responseJson = json.loads(responseText)
    if not statusCode.startswith('2'):
        print('!!! Fail', url)
        print(response)
        print(responseJson)
        print(kwargs)
        print(**kwargs)
        print(**kwargs.keys())
        print(kwargs.keys())
        pprint(kwargs)
        pprint(**kwargs)
        pprint(**kwargs.keys())
        pprint(kwargs.keys())
        raise Exception('%s Returned %s.' % (url, statusCode))

    return responseJson['result']