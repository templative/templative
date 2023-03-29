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
        startingY = 406.058
        lineHeight = 33.33337

        contents = permaNoteFile.read()
        contents = contents.replace("'", "`")
        contents = contents.replace('"', "`")
        contents = contents.replace("’", "`")
        contents = contents.replace('–', "-")

        lines = contents.split("\n")
        formattedContent = ""
        for line in lines:
            newTspan = '<tspan x=\'-76.34375px\' y=\'%s\' id=\'span%s\'>%sNEWLINE</tspan>' % (startingY + (lineHeight*spanId), spanId, line)
            spanId += 1
            formattedContent = formattedContent + newTspan

        csvContents = csvContents + "%s,%s,1,\"%s\"\n" % (folgezettel, name, formattedContent)
        permaNoteFile.close()

    with open("../zettelkasten.csv", "w") as csvOutput:
        csvOutput.write(csvContents)

    print("Written to ../zettelkasten.csv")
            