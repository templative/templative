from templative.manage import defineLoader

from markdown2 import markdown
from os import path

async def convertRulesMdToHtml(gameRootDirectoryPath):
    rules = await defineLoader.loadRules(gameRootDirectoryPath)
    htmlContent = markdown(rules)

    with open(path.join(gameRootDirectoryPath, "rules.html"), 'w', encoding="utf-8") as rulesHtmlFile:
        rulesHtmlFile.write(htmlContent)

async def convertRulesMdToSpans(gameRootDirectoryPath):
    rules = await defineLoader.loadRules(gameRootDirectoryPath)
    await convertRulesMdToSpansRaw(rules, gameRootDirectoryPath)

async def convertRulesMdToSpansRaw(rules, gameFolderPath):

    fontSize = 24
    fontSizeProgression = 5

    htmlContent = markdown(rules)
    htmlContent = htmlContent.replace("\n", "")

    # This creates a newline at the beginning of doc
    htmlContent = htmlContent.replace("<h1>", "<tspan font-weight='bold' font-size='%spx'>\\n" % ((6*fontSizeProgression)+fontSize))
    htmlContent = htmlContent.replace("<h2>", "<tspan font-weight='bold' font-size='%spx'>\\n" % ((5*fontSizeProgression)+fontSize))
    htmlContent = htmlContent.replace("<h3>", "<tspan font-weight='bold' font-size='%spx'>\\n" % ((4*fontSizeProgression)+fontSize))
    htmlContent = htmlContent.replace("<h4>", "<tspan font-weight='bold' font-size='%spx'>\\n" % ((3*fontSizeProgression)+fontSize))
    htmlContent = htmlContent.replace("<h5>", "<tspan font-weight='bold' font-size='%spx'>\\n" % ((2*fontSizeProgression)+fontSize))
    htmlContent = htmlContent.replace("<h6>", "<tspan font-weight='bold' font-size='%spx'>\\n" % ((1*fontSizeProgression)+fontSize))

    htmlContent = htmlContent.replace("</h1>", "</tspan>\\n")
    htmlContent = htmlContent.replace("</h2>", "</tspan>\\n")
    htmlContent = htmlContent.replace("</h3>", "</tspan>\\n")
    htmlContent = htmlContent.replace("</h4>", "</tspan>\\n")
    htmlContent = htmlContent.replace("</h5>", "</tspan>\\n")
    htmlContent = htmlContent.replace("</h6>", "</tspan>\\n")

    htmlContent = htmlContent.replace("<p>", "<tspan font-size='%spx'>" % (fontSize))
    htmlContent = htmlContent.replace("</p>", "</tspan>\\n")

    htmlContent = htmlContent.replace("<ul>", "<tspan font-size='%spx'>" % (fontSize))
    htmlContent = htmlContent.replace("</ul>", "</tspan>")
    htmlContent = htmlContent.replace("<li>", "- ")
    htmlContent = htmlContent.replace("</li>", "\\n")

    htmlContent = htmlContent.replace("<strong>", "<tspan font-weight='bold'>")
    htmlContent = htmlContent.replace("</strong>", "</tspan>")

    htmlContent = htmlContent.replace("<em>", "<tspan font-style='oblique'>")
    htmlContent = htmlContent.replace("</em>", "</tspan>")

    with open(path.join(gameFolderPath, "rules.html"), 'w', encoding="utf-8") as rulesHtmlFile:
        rulesHtmlFile.write(htmlContent)
