import math, uuid, os, json, random

playerColors = []
for i in range(20):
    playerColors.append({"r": str(random.random()*255), "g": str(random.random()*255), "b": str(random.random()*255)})

def createTableObject():
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

def createGameState(name, playerCount):
    slotTeams = [  ]
    slotIds = []
    for p in range(playerCount):
        slotTeams.append(p+1)
        slotIds.append(str(uuid.uuid4()))

    return {
        "notes": "This is a Templative generated game state of %s." % (name),
        "mapName": "HDRI_GranCanyon", "backgroundTexture": { "resourceName": "", "packageGuid": "00000000000000000000000000000000" },
        "physicsLocked": False,  "measureUnit": 2.5399999618530273, "rotationStep": 90, "measureAngles": "None", "alwaysSnap": False, "liftOverRegular": True, "gravityMultiplier": 1,
        
        "turnInfo": { },
        "slotTeams": slotTeams,
        "slotIds": slotIds,

        "globalScriptPackage": "00000000000000000000000000000000", "globalScriptName": "",
        
        "persistentData": "", "persistentKeyData": { },
        "permissions":
        {
            "delete": 0, "objectLibrary": 0, "copyPaste": 0, "cardPeek": -1, 
            "cardExplorer": 0, "containerExplorer": 0,
            "changeOwner": 0, "changeTeam": -1,
            "editZones": 0, "draw": 0,
            "ground": -1, "throw": 0,
            "editLabels": 0,
            "saveGame": -1
        },
        
        "currentTurn": 0,
        "bCanBeDamaged": False
    }

def getQuaternionFromEuler(roll, pitch, yaw):
  qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
  qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
  qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
  qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
 
  return [qx, qy, qz, qw]

def createCardHolder(playerIndex, totalPlayerCount):
    ownerColor = {"r": playerIndex/totalPlayerCount*255, "g": 50, "b": 50, "a": 255 }
    distanceFromCenter = 60 + (max(0, totalPlayerCount-2)*20)
    locationX = math.cos(playerIndex/totalPlayerCount*math.pi*2) * distanceFromCenter
    locationY = math.sin(playerIndex/totalPlayerCount*math.pi*2) * distanceFromCenter

    zRotation = (playerIndex/totalPlayerCount*math.pi*2)-math.pi
    rotationQuaternion = getQuaternionFromEuler(0,0,zRotation)
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

def createPokerDeck(name, componentId,  componentTemplateGuid, ownerIndex, translation, totalPieceQuantity):
    stackSerialization = []
    for q in range(totalPieceQuantity-1):
        piece = {
            "index": q+1,
            "templateId": componentTemplateGuid,
            "frontTextureOverride": "",
            "flipped": False
        }
        stackSerialization.append(piece)
    return {
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

def createGameObjects(components, totalPlayerCount):
    gameObjects = [
        createTableObject()
    ]

    for p in range(totalPlayerCount):
        gameObjects.append(createCardHolder(p, totalPlayerCount))

    startingYTranslation = 0
    yTranslationEachComponent = 15
    noOwnerConstant = -1

    for c, component in enumerate(components):
        if component == None:
            continue
        newYPosition = startingYTranslation + (c*yTranslationEachComponent) - (len(components)*yTranslationEachComponent/2)
        gameObjectTranslation = { "x": -5, "y": newYPosition, "z": 90 }
        # print(component)
        totalPieceQuantity = len(component["Indices"])
        # print(totalPieceQuantity)
        gameObject = createPokerDeck(component["Name"], c, component["GUID"], noOwnerConstant, gameObjectTranslation, totalPieceQuantity)
        gameObjects.append(gameObject)

    return gameObjects 

def choosePackages(gameName, packageGuid):
    return [
        {
            "name": gameName,
            "guid": packageGuid
        },
        { "name": "Cards", "guid": "8F8543D040D1C361098594A763847262" },
        { "name": "General", "guid": "D74C7D5D6745CD565913DAA5FB3E9C93" }
    ]

def createRoomForPlayerCount(totalPlayerCount):
    storedCameraSetups = []
    playerCameraSetups = []
    playerSlotNames = []
    customPlayerColors = []
    for p in range(totalPlayerCount):
        locationX = math.cos(p/totalPlayerCount*math.pi*2) * 100
        locationY = math.sin(p/totalPlayerCount*math.pi*2) * 100
        controlRotationYaw = (p * 360 / totalPlayerCount)-180

        storedCameraSetups.append({
            "location": { "x": locationX, "y": locationY, "z": 120 },
            "controlRotation": { "pitch": 330, "yaw": 0, "roll": 0 },
            "pawnRotation": { "x": 0, "y": 0, "z": 0, "w": 0 },
            "playerScale": 1, "flying": True
        })
        playerCameraSetups.append({
            "location": { "x": 0, "y": 0, "z": 90 },
            "controlRotation": { "pitch": 330, "yaw": controlRotationYaw, "roll": 0 },
            "pawnRotation": { "x": 0, "y": 0, "z": 0, "w": 0 },
            "playerScale": 1, "flying": True
        })
        playerSlotNames.append(str(p+1))
        customPlayerColors.append(playerColors[p])

    return {
        "storedCameraSetups": storedCameraSetups,
        "playerCameraSetups": playerCameraSetups,
        "playerSlotNames": playerSlotNames,
        "customPlayerColors": customPlayerColors
    }

async def createGameStateVts(gameName, packageGuid, components, totalPlayerCount, packageDirectoryPath):
    state = {
        "lighting": {
            "intensity": 1, "specular": 1, "altitude": 90, "azimuth": 0, "color": { "r": 255, "g": 255, "b": 255 }
        },

        "grid": {
            "type": 0, "snapType": 0, 
            "visibility": 0, "thickLines": False, "color": { "r": 0, "g": 0, "b": 0, "a": 179 },
            "offset": { "x": 0, "y": 0 }, "rotation": 0, "size": { "x": 5.0799999237060547, "y": 5.0799999237060547 },
        },
        "saveStateVersion": "1.0", "zones": [], "labels": []
    }
    state["gameState"] = createGameState(gameName, totalPlayerCount)
    state["requiredPackages"] = choosePackages(gameName, packageGuid)
    state["objects"] = createGameObjects(components, totalPlayerCount)

    roomData = createRoomForPlayerCount(totalPlayerCount)
    state["storedCameraSetups"] = roomData["storedCameraSetups"]
    state["playerCameraSetups"] = roomData["playerCameraSetups"]
    state["playerSlotNames"] = roomData["playerSlotNames"]
    state["customPlayerColors"] = roomData["customPlayerColors"]

    templateDirectory = os.path.join(packageDirectoryPath, "States")
    templateFilepath = os.path.join(templateDirectory, "%s.vts" % gameName)
    with open(templateFilepath, "w") as gameStateVtsFile:
        json.dump(state, gameStateVtsFile, indent=2)

    return state
