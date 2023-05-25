gameCrafterScaleToPlaygroundScale = 0.014

def createCardTemplate(guid, name, componentType, frontTextureName, totalCount, cardColumnCount, cardRowCount, backTextureName):
    indices = []
    for i in range(totalCount):
        indices.append(i)
        
    componentDimensions = {
        "BusinessDeck": (675 * gameCrafterScaleToPlaygroundScale, 1125 * gameCrafterScaleToPlaygroundScale, 0.05),
        "PokerDeck": (825 * gameCrafterScaleToPlaygroundScale, 1125 * gameCrafterScaleToPlaygroundScale, 0.05),
        "MiniDeck": (600 * gameCrafterScaleToPlaygroundScale, 825 * gameCrafterScaleToPlaygroundScale, 0.05),
        "MicroDeck": (450 * gameCrafterScaleToPlaygroundScale, 600 * gameCrafterScaleToPlaygroundScale, 0.2),
        "MintTinDeck": (750 * gameCrafterScaleToPlaygroundScale, 1125 * gameCrafterScaleToPlaygroundScale, 0.05),
        "HexDeck": (1200 * gameCrafterScaleToPlaygroundScale, 1050 * gameCrafterScaleToPlaygroundScale, 0.05),
        "SmallSquareChit": (225 * gameCrafterScaleToPlaygroundScale, 225 * gameCrafterScaleToPlaygroundScale, 0.2),
        "MediumSquareChit": (300 * gameCrafterScaleToPlaygroundScale, 300 * gameCrafterScaleToPlaygroundScale, 0.2),
        "LargeSquareChit": (375 * gameCrafterScaleToPlaygroundScale, 375 * gameCrafterScaleToPlaygroundScale, 0.2),
    }
    dimensions = (6,9,0.05)
    if componentType in componentDimensions:
        dimensions = componentDimensions[componentType]
    else:
        print("Missing dimensions for %s, using 6,9,0.05." % componentType)


    return {
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

def createBoardTemplate(guid, name, componentType, frontTextureName, backTextureName):
    scaleDown = gameCrafterScaleToPlaygroundScale / 53 * 1.5
    componentDimensions = {
        "MintTinAccordion4": (1125 * scaleDown, 2550 * scaleDown),
        "MintTinAccordion6": (1125 * scaleDown, 3825 * scaleDown),
        "MintTinAccordion8": (1125 * scaleDown, 5025 * scaleDown),
    }
    dimensions = 1
    if componentType in componentDimensions:
        dimensions = componentDimensions[componentType]
    else:
        print("Missing dimensions for %s, using 1." % componentType)

    return {
        "Type": "Generic",
        "GUID": guid,
        "Name": name,
        "Metadata": "",
        "CollisionType": "Ground",
        "Friction": 0.7,
        "Restitution": 0.3,
        "Density": 1,
        "SurfaceType": "Wood",
        "Roughness": 0.34,
        "Metallic": 1,
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
        "Blueprint": "Blueprints/Board.json",
        "Models": [
            {
                "Model": "StaticMesh'/Game/Meshes/Generic/BoardSurface.BoardSurface'",
                "Offset":
                {
                    "X": 0,
                    "Y": 0,
                    "Z": 0
                },
                "Scale":
                {
                    "X": dimensions[0],
                    "Y": dimensions[1],
                    "Z": 1
                },
                "Rotation":
                {
                    "X": 0,
                    "Y": 0,
                    "Z": 0
                },
                "Texture": frontTextureName,
                "NormalMap": "",
                "ExtraMap": "",
                "ExtraMap2": "",
                "IsTransparent": False,
                "CastShadow": True,
                "IsTwoSided": False,
                "UseOverrides": True,
                "SurfaceType": "Plastic"
            },
            {
                "Model": "StaticMesh'/Game/Meshes/Generic/BoardBody.BoardBody'",
                "Offset":
                {
                    "X": 0,
                    "Y": 0,
                    "Z": 0
                },
                "Scale":
                {
                    "X": dimensions[0],
                    "Y": dimensions[1],
                    "Z": 1
                },
                "Rotation":
                {
                    "X": 0,
                    "Y": 0,
                    "Z": 0
                },
                "Texture": "Texture2D'/Game/Textures/Boards/BoardWood_Diffuse.BoardWood_Diffuse'",
                "NormalMap": "Texture2D'/Game/Textures/Boards/BoardWood_Normal.BoardWood_Normal'",
                "ExtraMap": "Texture2D'/Game/Textures/Boards/BoardWood_Extra.BoardWood_Extra'",
                "ExtraMap2": "",
                "IsTransparent": False,
                "CastShadow": True,
                "IsTwoSided": False,
                "UseOverrides": False,
                "Roughness": 0.8,
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
                "SurfaceType": "Plastic"
            },
            {
                "Model": "StaticMesh'/Game/Meshes/Generic/BoardSurface.BoardSurface'",
                "Offset":
                {
                    "X": 0,
                    "Y": 0,
                    "Z": -1
                },
                "Scale":
                {
                    "X": dimensions[0],
                    "Y": dimensions[1],
                    "Z": 1
                },
                "Rotation":
                {
                    "X": 0,
                    "Y": 0,
                    "Z": 0
                },
                "Texture": backTextureName,
                "NormalMap": "",
                "ExtraMap": "",
                "ExtraMap2": "",
                "IsTransparent": False,
                "CastShadow": True,
                "IsTwoSided": False,
                "UseOverrides": True,
                "SurfaceType": "Plastic"
            }
        ],
        "Collision": [],
        "SnapPointsGlobal": False,
        "SnapPoints": [],
        "ZoomViewDirection":
        {
            "X": 0,
            "Y": 0,
            "Z": 0
        },
        "Tags": []
    }
