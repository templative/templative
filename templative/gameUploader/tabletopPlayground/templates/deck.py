import uuid

def createDeck(name, componentTemplateGuid, ownerIndex, translation, stackSerialization):
    {
        "uniqueId": str(uuid.uuid4()),
        "objectName": name,
        "objectDescription": "",
        "objectType": "Card",
        "templateId": componentTemplateGuid,
        "ownerIndex": ownerIndex, # -1 is no one

        "transform":
        {
            "rotation": { "x": 1, "y": -2.9294772048160667e-06, "z": -1.3968835853653272e-12, "w": 4.76837158203125e-07 },
            "translation": translation, # { "x": -5, "y": 2.0626037120819092, "z": 80 },
            "scale3D": { "x": 1, "y": 1, "z": 1 }
        },
        "previousPosition": { "x": 0, "y": 0, "z": 0 },

        "simulatingPhysics": True, "collisionType": "CB_Regular", "shouldSnap": True,

        "atlasIndex": 0,
        "frontTextureOverride": "",
        "inHand": False,
        "stackSerialization": stackSerialization,

        "primaryColor": { "b": 255, "g": 255, "r": 255, "a": 255 },
        "secondaryColor": { "b": 0, "g": 0, "r": 0, "a": 255 },

        "surfaceType": "SurfaceType4", "metallic": 0, "roughness": 1, "friction": 0.69999998807907104, "restitution": 0, "density": 0.5,
        "objectScriptName": "", "objectScriptPackage": "00000000000000000000000000000000",
        "persistentData": "", "persistentKeyData": {},
        "drawingLines": [], "objectTags": [], "objectGroupId": -1, "bCanBeDamaged": False
    }