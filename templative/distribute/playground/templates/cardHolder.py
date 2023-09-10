import uuid

def createCardHolder(playerIndex, ownerColor, locationX, locationY, rotationQuaternion):
    return {
        "uniqueId": str(uuid.uuid4()),
        "objectName": "CardHolder",
        "objectDescription": "",
        "objectType": "CardHolder",
        "templateId": "A12757C14B19B37232C9FCAC9B04CEA7",

        "ownerIndex": playerIndex,
        "primaryColor": ownerColor,
        "secondaryColor": { "b": 20, "g": 20, "r": 20, "a": 255 },

        "transform":
        {
            "translation": { "x": locationX, "y": locationY, "z": 100 },
            "rotation": { "x": rotationQuaternion[0], "y": rotationQuaternion[1], "z": rotationQuaternion[2], "w": rotationQuaternion[3] },
            "scale3D": { "x": 1.7715610265731812, "y": 1.7715610265731812, "z": 1.7715610265731812 }
        },
        "previousPosition": { "x": 0, "y": 0, "z": 0 },

        "canOnlyOwnerTakeCards": True,
        "showCardBacks": True,
        "showCardFronts": False,
        
        "simulatingPhysics": True, "shouldSnap": True,
        "collisionType": "CB_Regular", "surfaceType": "SurfaceType1", 
        "metallic": 1, "roughness": 0.5, "friction": 0.69999998807907104, "restitution": 0, "density": 5, 
        "objectScriptName": "", "objectScriptPackage": "00000000000000000000000000000000",
        "persistentData": "", "persistentKeyData": {},
        "cardsJson": [], "drawingLines": [], "objectTags": [], "objectGroupId": -1, "bCanBeDamaged": False
    }