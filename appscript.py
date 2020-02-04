# https://github.com/lohriialo/photoshop-scripting-python/tree/master/mac_scripting

from appscript import *

illustrator = app('/Applications/Adobe Illustrator CC 2020/Adobe Illustrator CC 2020.app')
illustrator.open(mactypes.Alias(file_name))
docRef = psApp.Documents.Add()
rectRef = docRef.PathItems.Rectangle(700, 50, 100, 100)
areaTextRef = docRef.TextFrames.AreaText(rectRef)
areaTextRef.Contents = "Hello World!"