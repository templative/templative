def createGameState(name, slotTeams, slotIds):
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
            "delete": -1, "objectLibrary": -1, "copyPaste": -1, "cardPeek": -1, 
            "cardExplorer": 0, "containerExplorer": -1,
            "changeOwner": -1, "changeTeam": -1,
            "editZones": 0, "draw": 0,
            "ground": -1, "throw": 0,
            "editLabels": 0,
            "saveGame": -1
        },
        
        "currentTurn": 0,
        "bCanBeDamaged": False
    }