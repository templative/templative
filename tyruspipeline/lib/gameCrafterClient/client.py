import os
from datetime import datetime
from ..http import httpClient

gameCrafterBaseUrl = "https://www.thegamecrafter.com/api"

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

    loginResponse = httpClient.post(gameCrafterBaseUrl + "/session", params=loginParameters)

    if loginResponse.status_code == 200:
        result = loginResponse.json()['result']
        sessionId = result["id"]
        userId = result["user_id"]
        return sessionId
    
    raise Exception('%s Could not log in. %s' % (loginResponse.error.code, loginResponse.error.message))

def getGames(sessionId):
    if sessionId is None or not sessionId:
        raise Exception('Session id is None.')

    params = {
        'session_id': sessionId
    }

    result = httpClient.get(session, 'user/%s/games' % session.UserId, params)

    if result['paging']['total_pages'] > 1:
        raise NotImplemented('Cannot handle pages yet')
    return result['items']

def getDesigners(session):
    result = httpClient.get(session, 'user/%s/designers' % session.UserId)

    if result['paging']['total_pages'] > 1:
        raise NotImplemented('Cannot handle pages yet')
    if len(result['items']) != 1:
        raise NotImplemented('Cannot handle 0 or >1 designers yet')

    return result['items']

def postGame(session, name):
    return httpClient.post(session, 'game',
        name = name,
        designer_id = session.designerId,
        description='Automatically created (%s)' % name,
    )

def postFolder(session, asset_name, parent_id=None):
    if parent_id is None:
        parent_id = user['root_folder_id']
    return httpClient.post(session, 'folder',
        name=asset_name,
        user_Id=user.id,
        parent_id=parent_id,
    )

def postFile(session, filepath, folder_id):
    if not os.path.isfile(filepath):
        raise Exception('Not a file: %s' % filepath)
    fp = file(filepath)
    filename = os.path.basename(filepath)
    return httpClient.post(session, 'file', files={'file':fp}, name=filename, folder_id=folder_id)

def makeSquareDeck(session, dirpath):
    asset = '%s-sqdeck-%s' % (self['name'], len(self.parts))

    def face_card_test(filename):
        return filename.startswith('deck') and filename.endswith('.png')

    return self.make_deck(
        'smallsquaredeck', 'smallsquarecard', asset, dirpath, face_card_test
    )

def makePokerDeck(session, dirpath):
    asset = '%s-pdeck-%s' % (self['name'], len(self.parts))

    def face_card_test(filename):
        return filename.startswith('face') and filename.endswith('.png')

    return self.make_deck(
        'pokerdeck', 'pokercard', asset, dirpath, face_card_test
    )

def makeDeck(session, deck_kind, card_kind, asset, dirpath, face_card_test):
    folder = core.new_folder(session, asset, self.folder['id'])

    back_filepath = dirpath + '/back.png'
    file_result = core.new_file(back_filepath, folder['id'])

    deck = new_deck(
        deck_kind, asset, self.id, back_file_id=file_result['id']
    )

    print 'Deck'
    print deck

    self.parts.append(deck)

    file_list = [dirpath + '/' + x
                    for x in os.listdir(dirpath)
                    if face_card_test(x)]
    for filepath in file_list:
        file_result = core.new_file(filepath, folder['id'])
        card = new_card(
            card_kind,
            os.path.basename(filepath),
            deck_id=deck['id'],
            file_id=file_result['id']
        )

def makeBooklet(session, dirpath):
    asset = '%s-booklet-%s' % (self['name'], len(self.parts))
    folder = core.new_folder(self.user, asset, self.folder['id'])

    booklet = new_booklet('smallbooklet', asset, self.id)

    print 'Booklet'
    print booklet

    self.parts.append(booklet)

    file_list = [dirpath + '/' + x
                    for x in os.listdir(dirpath)
                    if x.endswith('.png')]
    for filepath in file_list:
        file_result = core.new_file(filepath, folder['id'])
        card = new_booklet_page(
            'smallbookletpage',
            os.path.basename(filepath),
            booklet_id=booklet['id'],
            image_id=file_result['id']
        )







