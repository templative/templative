import json
from os import path
from templative.lib.distribute.gameCrafter.util import httpOperations
import time

INCH_TO_MILLIMETERS = 25.4
async def parseCustomStuff (gameCrafterSession):
    productInfo = await httpOperations.getCustomPartInfo(gameCrafterSession)
        
    componentInfo = {}
    for component in productInfo:
        widthInches = float(component["size"]["finished_inches"][0])
        heightInches = float(component["size"]["finished_inches"][1])
        widthPixels = component["size"]["pixels"][0]
        heightPixels = component["size"]["pixels"][1]
        ardataTypes = []
        for side in component["sides"]:
            ardataType = side["label"]
            if ardataType == "Face":
                ardataType = "Front"
            ardataTypes.append(ardataType)
        
        uploadTokens = path.split(component["create_api"])
        uploadTask = uploadTokens[len(uploadTokens)-1]
        millimeterDepth = 0
        if len(component["size"]["finished_inches"]) == 3:
            millimeterDepth = float(component["size"]["finished_inches"][2])*INCH_TO_MILLIMETERS
        componentInfo[component["identity"]] = {
            "DimensionsPixels": [widthPixels, heightPixels],
            "DimensionsInches": [widthInches, heightInches],
            "GameCrafterUploadTask": uploadTask,
            "GameCrafterPackagingDepthMillimeters": millimeterDepth,
            "HasPieceData": True,
            "HasPieceQuantity": False,
            "ArtDataTypeNames": ardataTypes,
        }

    with open('./customComponents.json', 'w') as f:
        json.dump(componentInfo, f, indent=4)

def tagListHasColor(tagList, possibleColor): 
    for tag in tagList:
        if tag.lower() == possibleColor.lower():
            return True
    return False

async def parseStockStuff(gameCrafterSession):
    pageNumber = 1
    stockInfo = {}
    while True:
        stockPartInfoPage = await httpOperations.getStockPartInfo(gameCrafterSession, pageNumber=pageNumber)
        print("Reading page %s of %s." % (stockPartInfoPage["paging"]["page_number"], stockPartInfoPage["paging"]["total_pages"]))
        
        for component in stockPartInfoPage["items"]:
            varname = "".join(component["name"].replace(",", "").split(" "))
            tags = []
            if "keywords" in component and component["keywords"] != None:
                tags = component["keywords"].split(", ")

            for index, item in enumerate(tags):
                tags[index] = item.lower()
            if "color" in component and component["color"] != None:
                color = component["color"].lower()
                if not tagListHasColor(tags, color):
                    tags.append(color)
            stockInfo[varname] = {
                "DisplayName": component["name"],
                "Description": component["description"],
                "GameCrafterId": component["id"],
                "GameCrafterSkuId": component["sku_id"],
                "Tags": tags
            }
        if int(stockPartInfoPage["paging"]["page_number"]) >= int(stockPartInfoPage["paging"]["total_pages"]):
            break
        pageNumber = pageNumber + 1
        time.sleep(1/4)
    with open('./stockComponents.json', 'w') as f:
        json.dump(stockInfo, f, indent=4)
