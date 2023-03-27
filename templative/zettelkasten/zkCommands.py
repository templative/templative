from os import listdir
from os.path import isfile, join

def convertFilesToCsv():
    files = [f for f in listdir(".") if isfile(join(".", f))]
    csvContents = "name,displayName,quantity,contents\n"

    for file in files:
        permaNoteFile = open(file, "r")
        filenameAndExtension = file.split(".")
        folgezettel = filenameAndExtension[0].split(" ")[0]
        name = '"' + file[len(folgezettel)+1:len(filenameAndExtension[0])] + '"'
        
        spanId = 0
        startingY = 418.9376
        lineHeight = 33.33337

        contents = permaNoteFile.read()
        contents = contents.replace("'", "`")
        contents = contents.replace('"', "`")
        contents = contents.replace("’", "`")
        contents = contents.replace('–', "-")
        contents = '"' + contents.replace('\n', "") + '"'

        # newTspan = '<tspan x=\'-50.472656\' y=\'385.60423\' dy=\'%spx\' id=\'span%s\'>' % (lineHeight*spanId, spanId)
        # contents = newTspan + contents
        # nextNewLineIndex = contents.find("\n",0,len(contents))
        # while nextNewLineIndex != -1:
        #     before = contents[0: nextNewLineIndex-1]
        #     after = contents[nextNewLineIndex+2: len(contents)]
        #     spanId += 1
        #     newTspan = '<tspan x=\'-50.472656\' y=\'385.60423\' dy=\'%spx\' id=\'span%s\'>' % (lineHeight*spanId, spanId)
        #     contents = "%s</tspan>%s%s" % (before, newTspan, after)
        #     nextNewLineIndex = contents.find("\n",0,len(contents))
        # contents = '"%s</tspan>"' % contents

        csvContents = csvContents + "%s,%s,1,%s\n" % (folgezettel, name, contents)
        permaNoteFile.close()
        # break

    with open("../zettelkasten.csv", "w") as csvOutput:
        csvOutput.write(csvContents)

    print("Written to ../zettelkasten.csv")
            