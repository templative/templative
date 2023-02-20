def createCardTemplate(guid, name, frontTextureName, cardColumnCount, totalCount, cardRowCount, backTextureName):
    indices = []
    for i in range(totalCount):
        indices.append(i)
        
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
        "Width": 6,
        "Height": 9,
        "Thickness": 0.05,
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

def createState(name, guid):
    {
        "saveStateVersion": "1.1",
        "gameState":
        {
            "measureUnit": 2.5399999618530273,
            "rotationStep": 90,
            "notes": "You can enter notes for the game here. They will be visible to all players and are stored when the game is saved.\n\nYou can use [color=#ff0000]colors[/color], [b]bold[/b] or [i]italic[/i] text, [size=9]different[/size] [size=16]sizes[/size], and [color=#00ff00][size=8][b][i]combine text styles.[/color][/size][/b][/i]",
            "currentTurn": 0,
            "slotTeams": [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            "globalScriptPackage": "00000000000000000000000000000000",
            "globalScriptName": "",
            "backgroundTexture":
            {
                "resourceName": "",
                "packageGuid": "00000000000000000000000000000000"
            },
            "persistentData": "",
            "persistentKeyData":
            {
            },
            "permissions":
            {
                "delete": 0,
                "objectLibrary": 0,
                "copyPaste": 0,
                "cardPeek": -1,
                "cardExplorer": 0,
                "containerExplorer": 0,
                "changeOwner": 0,
                "changeTeam": 0,
                "editZones": -1,
                "draw": 0,
                "ground": -1,
                "throw": 0,
                "editLabels": -1,
                "saveGame": 1048576
            },
            "physicsLocked": False,
            "measureAngles": "None",
            "alwaysSnap": True,
            "liftOverRegular": True,
            "gravityMultiplier": 1,
            "slotIds": [
                "00028b594f6a45a5916e3bd036615969",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                ""
            ],
            "mapName": "HDRI_GranCanyon",
            "bCanBeDamaged": False
        },
        "requiredPackages": [
            {
                "name": name,
                "guid": guid
            },
            {
                "name": "General",
                "guid": "D74C7D5D6745CD565913DAA5FB3E9C93"
            }
        ],
        "storedCameraSetups": [
            {
                "location":
                {
                    "x": -54.901287078857422,
                    "y": 0.1464335024356842,
                    "z": 120.90038299560547
                },
                "pawnRotation":
                {
                    "x": -0,
                    "y": 0,
                    "z": -0.0013576791388913989,
                    "w": 0.99999910593032837
                },
                "controlRotation":
                {
                    "pitch": 323.66275024414062,
                    "yaw": 359.84445190429688,
                    "roll": 0
                },
                "playerScale": 1,
                "flying": True
            },
            {
                "location":
                {
                    "x": 46.893218994140625,
                    "y": 0.95751029253005981,
                    "z": 130.61611938476562
                },
                "pawnRotation":
                {
                    "x": -0,
                    "y": 0,
                    "z": -0.99994999170303345,
                    "w": 0.010005354881286621
                },
                "controlRotation":
                {
                    "pitch": 319.40786743164062,
                    "yaw": 181.14656066894531,
                    "roll": 0
                },
                "playerScale": 1,
                "flying": True
            },
            False, False, False, False, False, False, False, False ],
        "playerCameraSetups": [ False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False ],
        "playerSlotNames": [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20"
        ],
        "customPlayerColors": [ False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False ],
        "lighting":
        {
            "intensity": 1,
            "specular": 1,
            "altitude": 90,
            "azimuth": 0,
            "color":
            {
                "r": 255,
                "g": 255,
                "b": 255
            }
        },
        "grid":
        {
            "type": 0,
            "snapType": 1,
            "visibility": 1,
            "size":
            {
                "x": 13.6,
                "y": 10
            },
            "offset":
            {
                "x": 0,
                "y": 0
            },
            "rotation": 0,
            "color":
            {
                "r": 0,
                "g": 0,
                "b": 0,
                "a": 77
            },
            "thickLines": False
        },
        "objects": [
            {
                "objectType": "Card",
                "transform":
                {
                    "rotation":
                    {
                        "x": 2.6633148308974341e-07,
                        "y": -2.6630073080013972e-07,
                        "z": -1,
                        "w": 5.7756900787353516e-05
                    },
                    "translation":
                    {
                        "x": -11.177281379699707,
                        "y": -20.19959831237793,
                        "z": 81.030532836914062
                    },
                    "scale3D":
                    {
                        "x": 1,
                        "y": 1,
                        "z": 1
                    }
                },
                "simulatingPhysics": True,
                "atlasIndex": 7,
                "frontTextureOverride": "",
                "inHand": False,
                "stackSerialization": [
                    {
                        "index": 8,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 34,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 15,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 17,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 2,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 4,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 5,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 24,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 26,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 16,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 14,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 22,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 23,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 29,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 21,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 33,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 9,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 13,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 1,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 25,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 18,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 27,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 12,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 3,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 28,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 19,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 30,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 31,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 32,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 20,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 11,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 0,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 6,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 10,
                        "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                        "frontTextureOverride": "",
                        "flipped": False
                    }
                ],
                "primaryColor":
                {
                    "b": 255,
                    "g": 255,
                    "r": 255,
                    "a": 255
                },
                "secondaryColor":
                {
                    "b": 0,
                    "g": 0,
                    "r": 0,
                    "a": 255
                },
                "metallic": 0,
                "roughness": 1,
                "friction": 0.69999998807907104,
                "restitution": 0,
                "density": 0.5,
                "surfaceType": "SurfaceType4",
                "objectName": "",
                "objectDescription": "",
                "collisionType": "CB_Regular",
                "templateId": "D5DDF8766CDE22E4E888C48AC1F079F8",
                "shouldSnap": True,
                "previousPosition":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "objectScriptPackage": "00000000000000000000000000000000",
                "objectScriptName": "",
                "persistentData": "",
                "persistentKeyData":
                {
                },
                "uniqueId": "ggs",
                "drawingLines": [],
                "objectTags": [],
                "objectGroupId": -1,
                "ownerIndex": -1,
                "bCanBeDamaged": False
            },
            {
                "objectType": "Card",
                "transform":
                {
                    "rotation":
                    {
                        "x": -4.8649741302142502e-07,
                        "y": 2.6631610694494157e-07,
                        "z": 1.29562091849382e-13,
                        "w": 1
                    },
                    "translation":
                    {
                        "x": -11.176000595092773,
                        "y": 20.192998886108398,
                        "z": 81.030540466308594
                    },
                    "scale3D":
                    {
                        "x": 1,
                        "y": 1,
                        "z": 1
                    }
                },
                "simulatingPhysics": True,
                "atlasIndex": 23,
                "frontTextureOverride": "",
                "inHand": False,
                "stackSerialization": [
                    {
                        "index": 19,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 14,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 13,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 17,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 32,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 10,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 20,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 8,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 26,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 11,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 0,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 1,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 18,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 34,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 27,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 7,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 25,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 22,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 2,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 4,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 16,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 31,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 24,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 5,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 9,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 3,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 29,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 6,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 28,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 15,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 33,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 12,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 30,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 21,
                        "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                        "frontTextureOverride": "",
                        "flipped": False
                    }
                ],
                "primaryColor":
                {
                    "b": 255,
                    "g": 255,
                    "r": 255,
                    "a": 255
                },
                "secondaryColor":
                {
                    "b": 0,
                    "g": 0,
                    "r": 0,
                    "a": 255
                },
                "metallic": 0,
                "roughness": 1,
                "friction": 0.69999998807907104,
                "restitution": 0,
                "density": 0.5,
                "surfaceType": "SurfaceType4",
                "objectName": "",
                "objectDescription": "",
                "collisionType": "CB_Regular",
                "templateId": "E05750D699A7FCD549B9335A2766CFDE",
                "shouldSnap": True,
                "previousPosition":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "objectScriptPackage": "00000000000000000000000000000000",
                "objectScriptName": "",
                "persistentData": "",
                "persistentKeyData":
                {
                },
                "uniqueId": "1pb",
                "drawingLines": [],
                "objectTags": [],
                "objectGroupId": -1,
                "ownerIndex": -1,
                "bCanBeDamaged": False
            },
            {
                "objectType": "Card",
                "transform":
                {
                    "rotation":
                    {
                        "x": 0.70710688829421997,
                        "y": -0.70710653066635132,
                        "z": -8.4293617419461953e-08,
                        "w": 4.2146845657953236e-07
                    },
                    "translation":
                    {
                        "x": -11.17600154876709,
                        "y": -33.654998779296875,
                        "z": 80.519065856933594
                    },
                    "scale3D":
                    {
                        "x": 1,
                        "y": 1,
                        "z": 1
                    }
                },
                "simulatingPhysics": True,
                "atlasIndex": 3,
                "frontTextureOverride": "",
                "inHand": False,
                "stackSerialization": [
                    {
                        "index": 2,
                        "templateId": "F0DD7A8D3DFED33BD6B41C7C455B3E2E",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 1,
                        "templateId": "F0DD7A8D3DFED33BD6B41C7C455B3E2E",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 0,
                        "templateId": "F0DD7A8D3DFED33BD6B41C7C455B3E2E",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 0,
                        "templateId": "0648DA065A0402E4E12A59405195EA89",
                        "frontTextureOverride": "",
                        "flipped": False
                    }
                ],
                "primaryColor":
                {
                    "b": 255,
                    "g": 255,
                    "r": 255,
                    "a": 255
                },
                "secondaryColor":
                {
                    "b": 0,
                    "g": 0,
                    "r": 0,
                    "a": 255
                },
                "metallic": 0,
                "roughness": 1,
                "friction": 0.69999998807907104,
                "restitution": 0,
                "density": 0.5,
                "surfaceType": "SurfaceType4",
                "objectName": "",
                "objectDescription": "",
                "collisionType": "CB_Regular",
                "templateId": "F0DD7A8D3DFED33BD6B41C7C455B3E2E",
                "shouldSnap": True,
                "previousPosition":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "objectScriptPackage": "00000000000000000000000000000000",
                "objectScriptName": "",
                "persistentData": "",
                "persistentKeyData":
                {
                },
                "uniqueId": "h9i",
                "drawingLines": [],
                "objectTags": [],
                "objectGroupId": -1,
                "ownerIndex": -1,
                "bCanBeDamaged": False
            },
            {
                "objectType": "Card",
                "transform":
                {
                    "rotation":
                    {
                        "x": -1.1748950328183128e-06,
                        "y": -7.1525607836520066e-07,
                        "z": 3.2781349545984995e-07,
                        "w": 1
                    },
                    "translation":
                    {
                        "x": -11.175999641418457,
                        "y": -13.461999893188477,
                        "z": 80.857093811035156
                    },
                    "scale3D":
                    {
                        "x": 1,
                        "y": 1,
                        "z": 1
                    }
                },
                "simulatingPhysics": True,
                "atlasIndex": 22,
                "frontTextureOverride": "",
                "inHand": False,
                "stackSerialization": [
                    {
                        "index": 21,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 14,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 18,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 10,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 2,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 3,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 9,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 12,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 1,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 13,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 4,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 5,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 17,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 7,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 20,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 16,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 19,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 23,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 0,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 6,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 8,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 15,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 11,
                        "templateId": "71BEE43A7A930F904D6194833B9619C9",
                        "frontTextureOverride": "",
                        "flipped": False
                    }
                ],
                "primaryColor":
                {
                    "b": 255,
                    "g": 255,
                    "r": 255,
                    "a": 255
                },
                "secondaryColor":
                {
                    "b": 0,
                    "g": 0,
                    "r": 0,
                    "a": 255
                },
                "metallic": 0,
                "roughness": 1,
                "friction": 0.69999998807907104,
                "restitution": 0,
                "density": 0.5,
                "surfaceType": "SurfaceType4",
                "objectName": "",
                "objectDescription": "",
                "collisionType": "CB_Regular",
                "templateId": "71BEE43A7A930F904D6194833B9619C9",
                "shouldSnap": True,
                "previousPosition":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "objectScriptPackage": "00000000000000000000000000000000",
                "objectScriptName": "",
                "persistentData": "",
                "persistentKeyData":
                {
                },
                "uniqueId": "oyo",
                "drawingLines": [],
                "objectTags": [],
                "objectGroupId": -1,
                "ownerIndex": -1,
                "bCanBeDamaged": False
            },
            {
                "objectType": "Card",
                "transform":
                {
                    "rotation":
                    {
                        "x": 3.5762784023063432e-07,
                        "y": 0.99999988079071045,
                        "z": 1.7881392011531716e-07,
                        "w": 6.3948846218409017e-14
                    },
                    "translation":
                    {
                        "x": -94.501907348632812,
                        "y": 8.9433937072753906,
                        "z": 0.024990873411297798
                    },
                    "scale3D":
                    {
                        "x": 1,
                        "y": 1,
                        "z": 1
                    }
                },
                "simulatingPhysics": True,
                "atlasIndex": 7,
                "frontTextureOverride": "",
                "inHand": False,
                "stackSerialization": [],
                "primaryColor":
                {
                    "b": 255,
                    "g": 255,
                    "r": 255,
                    "a": 255
                },
                "secondaryColor":
                {
                    "b": 0,
                    "g": 0,
                    "r": 0,
                    "a": 255
                },
                "metallic": 0,
                "roughness": 1,
                "friction": 0.69999998807907104,
                "restitution": 0,
                "density": 0.5,
                "surfaceType": "SurfaceType4",
                "objectName": "",
                "objectDescription": "",
                "collisionType": "CB_Regular",
                "templateId": "9BE81D099AEE087E6A8FDCCB9A1E00D9",
                "shouldSnap": True,
                "previousPosition":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "objectScriptPackage": "00000000000000000000000000000000",
                "objectScriptName": "",
                "persistentData": "",
                "persistentKeyData":
                {
                },
                "uniqueId": "xvo",
                "drawingLines": [],
                "objectTags": [],
                "objectGroupId": -1,
                "ownerIndex": -1,
                "bCanBeDamaged": False
            },
            {
                "objectType": "Card",
                "transform":
                {
                    "rotation":
                    {
                        "x": -3.5762795391747204e-07,
                        "y": 1,
                        "z": -3.5762795391747204e-07,
                        "w": -2.3841843699301535e-07
                    },
                    "translation":
                    {
                        "x": -11.175999641418457,
                        "y": 13.461999893188477,
                        "z": 80.557106018066406
                    },
                    "scale3D":
                    {
                        "x": 1,
                        "y": 1,
                        "z": 1
                    }
                },
                "simulatingPhysics": True,
                "atlasIndex": 0,
                "frontTextureOverride": "",
                "inHand": False,
                "stackSerialization": [
                    {
                        "index": 1,
                        "templateId": "9BE81D099AEE087E6A8FDCCB9A1E00D9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 2,
                        "templateId": "9BE81D099AEE087E6A8FDCCB9A1E00D9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 3,
                        "templateId": "9BE81D099AEE087E6A8FDCCB9A1E00D9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 4,
                        "templateId": "9BE81D099AEE087E6A8FDCCB9A1E00D9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 5,
                        "templateId": "9BE81D099AEE087E6A8FDCCB9A1E00D9",
                        "frontTextureOverride": "",
                        "flipped": False
                    },
                    {
                        "index": 6,
                        "templateId": "9BE81D099AEE087E6A8FDCCB9A1E00D9",
                        "frontTextureOverride": "",
                        "flipped": False
                    }
                ],
                "primaryColor":
                {
                    "b": 255,
                    "g": 255,
                    "r": 255,
                    "a": 255
                },
                "secondaryColor":
                {
                    "b": 0,
                    "g": 0,
                    "r": 0,
                    "a": 255
                },
                "metallic": 0,
                "roughness": 1,
                "friction": 0.69999998807907104,
                "restitution": 0,
                "density": 0.5,
                "surfaceType": "SurfaceType4",
                "objectName": "",
                "objectDescription": "",
                "collisionType": "CB_Regular",
                "templateId": "9BE81D099AEE087E6A8FDCCB9A1E00D9",
                "shouldSnap": True,
                "previousPosition":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "objectScriptPackage": "00000000000000000000000000000000",
                "objectScriptName": "",
                "persistentData": "",
                "persistentKeyData":
                {
                },
                "uniqueId": "3g4",
                "drawingLines": [],
                "objectTags": [],
                "objectGroupId": -1,
                "ownerIndex": -1,
                "bCanBeDamaged": False
            },
            {
                "objectType": "Table",
                "transform":
                {
                    "rotation":
                    {
                        "x": 0,
                        "y": 0,
                        "z": 0,
                        "w": 1
                    },
                    "translation":
                    {
                        "x": 0,
                        "y": 0,
                        "z": 0
                    },
                    "scale3D":
                    {
                        "x": 1,
                        "y": 1,
                        "z": 1
                    }
                },
                "simulatingPhysics": True,
                "primaryColor":
                {
                    "b": 255,
                    "g": 255,
                    "r": 255,
                    "a": 255
                },
                "secondaryColor":
                {
                    "b": 0,
                    "g": 0,
                    "r": 0,
                    "a": 255
                },
                "metallic": 0,
                "roughness": 1,
                "friction": 0.69999998807907104,
                "restitution": 0.30000001192092896,
                "density": 1,
                "surfaceType": "SurfaceType1",
                "objectName": "",
                "objectDescription": "",
                "collisionType": "CB_Static",
                "templateId": "F27689B0431FFA778EC9D6835FA2B8FC",
                "shouldSnap": True,
                "previousPosition":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "objectScriptPackage": "00000000000000000000000000000000",
                "objectScriptName": "",
                "persistentData": "",
                "persistentKeyData":
                {
                },
                "uniqueId": "",
                "drawingLines": [],
                "objectTags": [],
                "objectGroupId": -1,
                "ownerIndex": -1,
                "bCanBeDamaged": False
            }
        ],
        "zones": [],
        "labels": []
    }