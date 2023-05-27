import uuid

def createTable():
    return {
        "uniqueId": str(uuid.uuid4()),
        "objectName": "Table",
        "objectDescription": "Knock on wood.",

        "objectType": "Table",
        "templateId": "F27689B0431FFA778EC9D6835FA2B8FC",
        
        "transform":
        {
            "rotation": { "x": 0, "y": 0, "z": 0, "w": 1 },
            "translation": { "x": 0, "y": 0, "z": 0 },
            "scale3D": { "x": 4, "y": 2, "z": 1 }
        },
        "previousPosition": { "x": 0, "y": 0, "z": 0 },
        
        "primaryColor":{ "b": 255, "g": 255, "r": 255, "a": 255 },
        "secondaryColor": { "b": 0, "g": 0, "r": 0, "a": 255 },

        "simulatingPhysics": True, "shouldSnap": True,
        "collisionType": "CB_Static", "surfaceType": "SurfaceType1",
        "density": 1,  "metallic": 0, "roughness": 1,
        "friction": 0.69999998807907104, "restitution": 0.30000001192092896,
        
        "objectScriptName": "", "objectScriptPackage": "00000000000000000000000000000000",

        "persistentData": "",
        "persistentKeyData": {},
        
        "drawingLines": [], "objectTags": [],
        "objectGroupId": -1, "ownerIndex": -1,
        "bCanBeDamaged": False
    }