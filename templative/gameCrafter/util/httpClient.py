import json

async def post(gameCrafterSession, url, **kwargs):
    async with gameCrafterSession.httpSession.post(url, data=kwargs) as response:
        return await handleResponse(url, response)

async def get(gameCrafterSession, url, **kwargs):
    async with gameCrafterSession.httpSession.get(url, params=kwargs) as response:
        return await handleResponse(url, response)

async def delete(gameCrafterSession, url, **kwargs):
    async with gameCrafterSession.httpSession.delete(url, params=kwargs) as response:
        return await handleResponse(url, response)

async def handleResponse(url, response):
    statusCode = str(response.status)
    responseText = await response.text()
    responseJson = json.loads(responseText)
    if not statusCode.startswith('2'):
        print ('FAIL', response)
        print ('FAIL', responseJson)
        raise Exception('%s Returned %s.' % (url, statusCode))

    return responseJson['result']