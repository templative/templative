import os
import requests as old_requests
import requests_async as requests
import json
import aiohttp

async def post(session, url, **kwargs):
    async with session.post(url, data=kwargs) as response:
        return await handleResponse(url, response)

async def get(session, url, **kwargs):
    async with  session.get(url, params=kwargs) as response:
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