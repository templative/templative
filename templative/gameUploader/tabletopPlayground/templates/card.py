def createCard(guid, name, frontTextureName, backTextureName, cardColumnCount, cardRowCount, dimensions, indices):
    {
        "Type": "Card",
        "GUID": guid,
        "Name": name,
        "Metadata": "",
        "CollisionType": "Regular",
        "Friction": 0.7,
        "Restitution": 0,
        "Density": 0.5,
        "SurfaceType": "Cardboard",
        "Roughness": 1,
        "Metallic": 0,
        "PrimaryColor":
        {
            "R": 255,
            "G": 255,
            "B": 255
        },
        "SecondaryColor":
        {
            "R": 0,
            "G": 0,
            "B": 0
        },
        "Flippable": True,
        "AutoStraighten": False,
        "ShouldSnap": True,
        "ScriptName": "",
        "Blueprint": "",
        "Models": [],
        "Collision": [],
        "SnapPointsGlobal": False,
        "SnapPoints": [],
        "ZoomViewDirection":
        {
            "X": 0,
            "Y": 0,
            "Z": 0
        },
        "Tags": [],
        "FrontTexture": frontTextureName,
        "BackTexture": backTextureName,
        "HiddenTexture": "",
        "BackIndex": -2,
        "HiddenIndex": -1,
        "NumHorizontal": cardColumnCount,
        "NumVertical": cardRowCount,
        "Width": dimensions[0],
        "Height": dimensions[1],
        "Thickness": dimensions[2],
        "HiddenInHand": True,
        "UsedWithCardHolders": True,
        "CanStack": True,
        "UsePrimaryColorForSide": False,
        "FrontTextureOverrideExposed": False,
        "AllowFlippedInStack": False,
        "MirrorBack": True,
        "EmissiveFront": False,
        "Model": "Rounded",
        "Indices": indices,
        "CardNames":
        {
        },
        "CardMetadata":
        {
        },
        "CardTags":
        {
        }
    }