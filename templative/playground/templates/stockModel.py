def createStockModel(name, guid, mesh, color, normalMap, extraMap):
    return {
        "Name": name,
        "GUID": guid,
        "Type": "Generic",
        "Metadata": "",
        "CollisionType": "Regular",
        "Friction": 0.7,
        "Restitution": 0.3,
        "Density": 1,
        "SurfaceType": "Plastic",
        "Roughness": 0.2,
        "Metallic": 0,
        "PrimaryColor": color,
        "SecondaryColor": { "R": 0, "G": 0, "B": 0 },
        "Flippable": False,
        "AutoStraighten": False,
        "ShouldSnap": True,
        "ScriptName": "",
        "Blueprint": "",
        "Models": [
            {
                "Model": mesh,
                "Offset": { "X": 0, "Y": 0, "Z": 0 },
                "Scale": { "X": 1, "Y": 1, "Z": 1 },
                "Rotation": { "X": 0, "Y": 0, "Z": 0 },
                "Texture": "",
                "NormalMap": normalMap,
                "ExtraMap": extraMap,
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
        "ZoomViewDirection": { "X": 0, "Y": 0, "Z": 0 },
        "Tags": []
    }