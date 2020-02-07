import os
import requests
import tgcUser

baseUrl = "https://www.thegamecrafter.com/api"

def post(sessionId, endpoint, files=None, **kwargs):
    if sessionId is None or not sessionId:
        raise Exception('Session id is None.')

    url = baseUrl
    if not endpoint.startswith('/'):
        url += '/'
    url += endpoint

    params = kwargs
    params['session_id'] = sessionId
    print 'POST', url, params.keys()
    response = requests.post(url, params=params, files=files)

    if not str(response.status_code).startswith('2'):
        print 'FAIL', response
        print 'FAIL', response.json()
        raise Exception('Request failed')

    return response.json()['result']

def get(sessionId, endpoint, **kwargs):
    if sessionId is None or not sessionId:
        raise Exception('Session id is None.')

    url = baseUrl
    if not endpoint.startswith('/'):
        url += '/'
    url += endpoint

    params = kwargs
    params['session_id'] = sessionId
    print 'GET', url, params.keys()
    response = requests.get(url, params=params)
    if not str(response.status_code).startswith('2'):
        print 'FAIL', response
        print 'FAIL', response.json()
        raise Exception('Request failed')
    return response.json()['result']

def login():
    publicApiKey = os.environ.get('THEGAMECRAFTER_PUBLIC_KEY')
    if not publicApiKey:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PUBLIC_KEY. Value is %s' % publicApiKey)
    
    userName = os.environ.get('THEGAMECRAFTER_USER')
    if not userName:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_USER. Value is %s' % userName)

    userPassword = os.environ.get('THEGAMECRAFTER_PASSWORD')
    if not userPassword:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PASSWORD. Value is %s' % userPassword)

    loginParameters = {
        'api_key_id': publicApiKey,
        'username' : userName,
        'password': userPassword,
    }
    loginResponse = requests.post(baseUrl + "/session", params=loginParameters)

    if loginResponse.status_code == 200:
        result = loginResponse.json()['result']
        sessionId = result["id"]
        userId = result["user_id"]
        return sessionId
    
    raise Exception('%s Could not log in. %s' % (loginResponse.error.code, loginResponse.error.message))

