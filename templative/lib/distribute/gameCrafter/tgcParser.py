import json
from os import path
from templative.lib.distribute.gameCrafter.util import httpOperations
from templative.lib.stockComponentInfo import STOCK_COMPONENT_INFO
from templative.lib.componentInfo import COMPONENT_INFO
import time
import re

blankSvgFileContents = '<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg version="1.1" id="template" x="0px" y="0px" width="%s" height="%s" viewBox="0 0 1125 1725" enable-background="new 0 0 270 414" xml:space="preserve" sodipodi:docname="blank.svg" inkscape:version="1.2.2 (b0a8486, 2022-12-01)" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"> <defs id="defs728" /> <sodipodi:namedview id="namedview726" pagecolor="#ffffff" bordercolor="#999999" borderopacity="1" showgrid="false" /></svg>'
componentsDirectoryPath = "C:/Users/User/Documents/git/nextdaygames/templative/templative/lib/create/componentTemplates"

INCH_TO_MILLIMETERS = 25.4

bannedCustomComponentTagNames = set({"and", "bi", "top", "side", "color", "custom"})

def convertVarNameIntoTagSet(varname):
    varnameTags = re.findall('[A-Z][^A-Z]*', varname)
    varNameTagSet = set()
    for varnameTag  in varnameTags:
        if len(varnameTag) == 1:
            continue
        lowercaseVarname = varnameTag.lower()
        if lowercaseVarname in bannedCustomComponentTagNames:
            continue
        if lowercaseVarname == "d6" or lowercaseVarname == "d4" or lowercaseVarname == "d8" or lowercaseVarname == "d20":
            lowercaseVarname = varNameTagSet.add(lowercaseVarname)
            continue
        lowercaseVarname = re.sub(r'[0-9]', '', lowercaseVarname)
        varNameTagSet.add(lowercaseVarname)
    return varNameTagSet

def createTemplateSvgFileAtDimensionsIfMissing(filename, widthPixels, heightPixels):
    templateFileContents = blankSvgFileContents % (widthPixels, heightPixels)
    templateFilepath = path.join(componentsDirectoryPath, "%s.svg" % filename)
    if path.exists(templateFilepath):
        return
    with open(templateFilepath, "a") as f:
        f.write(templateFileContents)  

def parseArtdataTypes(allArtdataTypes, sides):
    ardataTypes = set()
    for side in sides:
        ardataType = side["label"]
        isFront = ardataType == "Face" or ardataType == "Top" or ardataType == "Image" or ardataType == "Face(Exposed)" or ardataType == "Outside" or ardataType.startswith("Side")
        if isFront:
            ardataType = "Front"
        if ardataType == "Bottom" or ardataType == "Back(Reflected)" or ardataType == "Inside":
            ardataType = "Back"
        ardataTypes.add(ardataType)
        allArtdataTypes.add(ardataType)
    return ardataTypes

def parseUploadTask(uploadTasks, apiEndpoint):
    uploadTokens = path.split(apiEndpoint)
    uploadTask = uploadTokens[len(uploadTokens)-1]
    uploadTasks.add(uploadTask)
    return uploadTask

def collateTagsUsingExistingAndVarname(varnameTagSet, varname):
    tags = set()
    if varname in COMPONENT_INFO and "Tags" in COMPONENT_INFO[varname]:
        tags = set(COMPONENT_INFO[varname]["Tags"])
    for varnameTag in varnameTagSet:
        tags.add(varnameTag)

async def parseCustomStuff (gameCrafterSession):
    productInfo = await httpOperations.getCustomPartInfo(gameCrafterSession)
        
    componentInfo = COMPONENT_INFO
    uploadTasks = set()
    allArtdataTypes = set()

    componentInfo = COMPONENT_INFO
    for component in productInfo:
        varname = component["identity"]
        varnameTagSet = convertVarNameIntoTagSet(varname)
        widthInches = float(component["size"]["finished_inches"][0])
        heightInches = float(component["size"]["finished_inches"][1])
        widthPixels = component["size"]["pixels"][0]
        heightPixels = component["size"]["pixels"][1]

        createTemplateSvgFileAtDimensionsIfMissing(varname, widthPixels, heightPixels)
        ardataTypes = parseArtdataTypes(allArtdataTypes, component["sides"])
        uploadTask = parseUploadTask(uploadTasks, component["create_api"])
        
        millimeterDepthIsDefined = len(component["size"]["finished_inches"]) == 3
        millimeterDepth = float(component["size"]["finished_inches"][2])*INCH_TO_MILLIMETERS if millimeterDepthIsDefined else 0 
                
        tags = collateTagsUsingExistingAndVarname(varnameTagSet, varname)
        isDie = component["sides"][0]["label"].startswith("Side")
            
        componentInfo[varname] = COMPONENT_INFO[varname] if varname in COMPONENT_INFO else {}
        componentInfo[varname]["DisplayName"] = varname
        componentInfo[varname]["DimensionsPixels"] = [widthPixels, heightPixels]
        componentInfo[varname]["DimensionsInches"] = [widthInches, heightInches]
        componentInfo[varname]["GameCrafterUploadTask"] = uploadTask
        componentInfo[varname]["GameCrafterPackagingDepthMillimeters"] = millimeterDepth
        componentInfo[varname]["HasPieceData"] = True
        componentInfo[varname]["HasPieceQuantity"] = not isDie
        componentInfo[varname]["ArtDataTypeNames"] = list(ardataTypes)
        componentInfo[varname]["Tags"] = list(tags)
            
    for key in componentInfo:
        if not "DisplayName" in componentInfo[key]:
            componentInfo[key]["DisplayName"] = key
        if not "Tags" in componentInfo[key]:
            componentInfo[key]["Tags"] = []
    for componentKey in COMPONENT_INFO:
        if componentKey in componentInfo:
            continue
        print("%s is missing"%componentKey)
    with open('./customComponents.json', 'w') as f:
        json.dump(componentInfo, f, indent=4)


def tagListHasColor(tagList, possibleColor): 
    for tag in tagList:
        if tag.lower() == possibleColor.lower():
            return True
    return False

async def parseStockStuff(gameCrafterSession):
    pageNumber = 1
    stockInfo = STOCK_COMPONENT_INFO
    allTags = set()
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
                if item == "":
                    del tags[index]
            for tag in tags:
                allTags.add(tag)
            if "color" in component and component["color"] != None:
                color = component["color"].lower()
                if not tagListHasColor(tags, color):
                    tags.append(color)
            stockInfo[varname] = STOCK_COMPONENT_INFO[varname] if varname in STOCK_COMPONENT_INFO else {}
            description = component["description"] if ("description" in component and component["description"] != None) else ""
            stockInfo[varname]["DisplayName"] = component["name"]
            stockInfo[varname]["Description"] = description
            stockInfo[varname]["GameCrafterGuid"] = component["id"]
            stockInfo[varname]["GameCrafterSkuId"] = component["sku_id"]
            stockInfo[varname]["Tags"] = tags
            
        if int(stockPartInfoPage["paging"]["page_number"]) >= int(stockPartInfoPage["paging"]["total_pages"]):
            break
        pageNumber = pageNumber + 1
        time.sleep(1/4)

    gameCrafterIds = {}
    for key in stockInfo:
        if not "DisplayName" in stockInfo[key]:
            stockInfo[key]["DisplayName"] = key
        if stockInfo[key]["GameCrafterGuid"] in gameCrafterIds:
            print("Duplicate part: %s" % key)
        gameCrafterIds[stockInfo[key]["GameCrafterGuid"]] = True
    print(allTags)
    # with open('./stockComponents.json', 'w') as f:
    #     json.dump(stockInfo, f, indent=2)
