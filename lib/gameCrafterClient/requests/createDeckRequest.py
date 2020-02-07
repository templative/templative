def createDeckRequest(session, kind, name, game_id, back_file_id=None):
    res = post(session, 
        kind,
        name=name,
        game_id=game_id,
        back_id=back_file_id,
    )
    return res