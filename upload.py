import os
from datetime import datetime
import os
import requests

base_url="https://www.thegamecrafter.com/api"

session = None

def getGames(gameCrafterSession):
    result = get(gameCrafterSession, gameCrafterSession, 'user/%s/games' % gameCrafterSession.UserId)
    if result['paging']['total_pages'] > 1:
        raise NotImplemented('Cannot handle pages yet')
    return result['items']

def getDesigners(gameCrafterSession):
    result = get(gameCrafterSession, 'user/%s/designers' % gameCrafterSession.UserId)

    if result['paging']['total_pages'] > 1:
        raise NotImplemented('Cannot handle pages yet')
    if len(result['items']) != 1:
        raise NotImplemented('Cannot handle 0 or >1 designers yet')

    return result['items']

def postGame(gameCrafterSession, name):
    return post(gameCrafterSession, 'game',
        name = name,
        designer_id = gameCrafterSession.designerId,
        description='Automatically created (%s)' % name,
    )

def postFolder(gameCrafterSession, asset_name, parent_id=None):
    if parent_id is None:
        parent_id = user['root_folder_id']
    return post(gameCrafterSession, 'folder',
        name=asset_name,
        gameCrafterSession.UserId=user.id,
        parent_id=parent_id,
    )

def postFile(gameCrafterSession, filepath, folder_id):
    if not os.path.isfile(filepath):
        raise Exception('Not a file: %s' % filepath)
    fp = file(filepath)
    filename = os.path.basename(filepath)
    return post(gameCrafterSession, 'file', files={'file':fp}, name=filename, folder_id=folder_id)

def make_square_deck(gameCrafterSession, dirpath):
        asset = '%s-sqdeck-%s' % (self['name'], len(self.parts))

        def face_card_test(filename):
            return filename.startswith('deck') and filename.endswith('.png')

        return self.make_deck(
            'smallsquaredeck', 'smallsquarecard', asset, dirpath, face_card_test
        )

def make_poker_deck(gameCrafterSession, dirpath):
    asset = '%s-pdeck-%s' % (self['name'], len(self.parts))

    def face_card_test(filename):
        return filename.startswith('face') and filename.endswith('.png')

    return self.make_deck(
        'pokerdeck', 'pokercard', asset, dirpath, face_card_test
    )

def make_deck(gameCrafterSession, deck_kind, card_kind, asset, dirpath, face_card_test):
    folder = core.new_folder(gameCrafterSession, asset, self.folder['id'])

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

def make_booklet(gameCrafterSession, dirpath):
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

def createDeckRequest(gameCrafterSession, kind, name, game_id, back_file_id=None):
    res = post(gameCrafterSession, 
        kind,
        name=name,
        game_id=game_id,
        back_id=back_file_id,
    )
    return res

def createCardRequest(gameCrafterSession, kind, name, deck_id, file_id=None):
    res = post(gameCrafterSession, 
        kind,
        name=name,
        deck_id=deck_id,
        face_id=file_id,
        has_proofed_face=1,
    )
    return res

def createBookletRequest(gameCrafterSession, kind, name, game_id):
    res = post(gameCrafterSession, 
        kind,
        name=name,
        game_id=game_id,
    )
    return res

def createBookletPageRequest(gameCrafterSession, kind, name, booklet_id, image_id):
    res = post(gameCrafterSession, 
        kind,
        name=name,
        booklet_id=booklet_id,
        image_id=image_id,
        has_proofed_image=1,
    )
    return res