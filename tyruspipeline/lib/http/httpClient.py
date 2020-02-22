import os
import requests

def post(url, files=None, **kwargs):
    # print(url)
    response = requests.post(url, params=kwargs, files=files)

    if not str(response.status_code).startswith('2'):
        print 'FAIL', response
        print 'FAIL', response.json()
        raise Exception('%s Request failed', url)

    return response.json()['result']

def get(url, **kwargs):
    # print(url)
    response = requests.get(url, params=kwargs)
    
    if not str(response.status_code).startswith('2'):
        print 'FAIL', response
        print 'FAIL', response.json()
        raise Exception('%s Request failed' % url)

    return response.json()['result']