import os
import requests

def post(url, files=None, **kwargs):
    # print(url)
    response = requests.post(url, params=kwargs, files=files)
    return handleResponse(url, response)

def get(url, **kwargs):
    # print(url)
    response = requests.get(url, params=kwargs)
    return handleResponse(url, response)

def handleResponse(url, response):
    statusCode = str(response.status_code)
    if not statusCode.startswith('2'):
        print 'FAIL', response
        print 'FAIL', response.json()
        raise Exception('%s Returned %s. %s' % (url, statusCode, response.message))
    
    return response.json()['result']