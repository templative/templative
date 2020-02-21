import os
from datetime import datetime
from ..http import httpClient

gameCrafterBaseUrl = "https://www.thegamecrafter.com/api"

def login(publicApiKey, userName, userPassword):
    url = "%s/session" % gameCrafterBaseUrl
    return httpClient.post(url, 
        api_key_id = publicApiKey,
        username = userName,
        password = userPassword
    )

def postGame(session, name, designerId):
    url = "%s/game" % gameCrafterBaseUrl
    return httpClient.post(url,
        session_id = session["id"],
        name = name,
        designer_id = designerId,
        description='Automatically created (%s)' % name,
    )

def postFolder(session, name, parent_id=None):
    url = "%s/folder" % gameCrafterBaseUrl
    return httpClient.post(url,
        session_id = session["id"],
        name=name,
        user_Id=user.id,
        parent_id=parent_id,
    )

def postFile(session, filepath, folder_id):
    if not os.path.isfile(filepath):
        raise Exception('Not a file: %s' % filepath)
    fp = file(filepath)
    filename = os.path.basename(filepath)
    return httpClient.post(session, 'file', files={'file':fp}, name=filename, folder_id=folder_id)

def makePokerDeck(session, dirpath):
    asset = '%s-pdeck-%s' % (self['name'], len(self.parts))

    def face_card_test(filename):
        return filename.startswith('face') and filename.endswith('.jpg')

    return makeDeck('pokerdeck', 'pokercard', asset, dirpath, face_card_test)

def makeDeck(session, deck_kind, card_kind, asset, dirpath, face_card_test):
    folder = core.new_folder(session, asset, self.folder['id'])

    back_filepath = dirpath + '/back.jpg'
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







