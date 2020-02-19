import os
import requests

def post(url, files=None, **kwargs):
    print(kwargs)
    response = requests.post(url, params=kwargs, files=files)

    if not str(response.status_code).startswith('2'):
        print 'FAIL', response
        print 'FAIL', response.json()
        raise Exception('Request failed')

    return response.json()['result']

def get(url, **kwargs):
    response = requests.get(url, params=kwargs)
    
    if not str(response.status_code).startswith('2'):
        print 'FAIL', response
        print 'FAIL', response.json()
        raise Exception('Request failed')

    return response.json()['result']



