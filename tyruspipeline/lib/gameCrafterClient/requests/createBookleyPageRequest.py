def createBookletPageRequest(session, kind, name, booklet_id, image_id):
    res = post(session, 
        kind,
        name=name,
        booklet_id=booklet_id,
        image_id=image_id,
        has_proofed_image=1,
    )
    return res