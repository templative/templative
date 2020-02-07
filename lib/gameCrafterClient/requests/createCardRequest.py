def createCardRequest(session, kind, name, deck_id, file_id=None):
    res = post(session, 
        kind,
        name=name,
        deck_id=deck_id,
        face_id=file_id,
        has_proofed_face=1,
    )
    return res