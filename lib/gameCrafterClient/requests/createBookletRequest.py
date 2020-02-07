def createBookletRequest(session, kind, name, game_id):
    res = post(session, 
        kind,
        name=name,
        game_id=game_id,
    )
    return res