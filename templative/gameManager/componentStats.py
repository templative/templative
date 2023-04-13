componentImageSizePixels = {
    "PokerDeck": { "width": 825, "height": 1125 },
    "MintTinDeck": { "width": 750, "height": 1125 },
    "HexDeck": { "width": 1200, "height": 1050 },
    "MiniDeck": { "width": 600, "height": 825 },
    "MicroDeck": { "width": 450, "height": 600 },

    "LargeRingChit": { "width": 450, "height": 450 },
    "MediumRingChit": { "width": 375, "height": 375 },
    "SmallRingChit": { "width": 300, "height": 300 },

    "LargeSquareChit": { "width": 375, "height": 375 },
    "MediumSquareChit": { "width": 300, "height": 300 },
    "SmallSquareChit": { "width": 225, "height": 225 },

    "LargeHexTile": { "width": 1200, "height": 1050 },
    "MediumHexTile": { "width": 825, "height": 750 },
    "SmallHexTile": { "width": 675, "height": 600 },

    "HexShard": { "width": 300, "height": 300 },
    "CircleShard": { "width": 300, "height": 300 },
    "SquareShard": { "width": 300, "height": 300 },

    "LargeCircleChit": { "width": 375, "height": 375 },
    "MediumCircleChit": { "width": 300, "height": 300 },
    "SmallCircleChit": { "width": 225, "height": 225 },

    "SmallStoutBox": { "width": 3600, "height": 3000 },
    "MediumStoutBox": { "width": 3675, "height": 4575  },
    "LargeStoutBox": { "width": 5925, "height": 5925 },

    "PokerTuckBox36": { "width": 2100, "height": 1800 },
    "PokerTuckBox54": { "width": 2325, "height": 1950 },
    "PokerTuckBox72": { "width": 2550, "height": 1950 },
    "PokerTuckBox90": { "width": 2775, "height": 2100 },
    "PokerTuckBox108": { "width": 3075, "height": 2250 },

    "PokerFolio": { "width": 2625, "height": 1050 },
    "MintTinFolio": { "width": 2625, "height": 1050 },

    "MintTinAccordion4": { "width": 2550, "height": 1125 },
    "MintTinAccordion6": { "width": 3825, "height": 1125 },
    "MintTinAccordion8": { "width": 5025, "height": 1125 },

    "CustomColorD4": { "width": 300, "height": 300 },
    "CustomColorD6": { "width": 180, "height": 180 },
    "CustomColorD8": { "width": 300, "height": 300 },

    "MintTin": {"width": 750, "height": 1125}
}

from os import path, getcwd

def getTemplateDirectory():
    return path.join(path.dirname(path.realpath(__file__)), "componentTemplates")

for key in componentImageSizePixels:
    templateFile = "%s.svg" % key
    templateFilepath = path.join(getTemplateDirectory(), templateFile)
    if not path.isfile(templateFilepath):
        print("WARNING: Missing %s" % templateFilepath)
