from markdown2 import markdown, markdown_path
from weasyprint import HTML, CSS
from os import path

async def produceRulebook(rules, gameFolderPath):
    outputFilepath = path.join(gameFolderPath, "rules.pdf")
    cssFilepath = path.join(path.dirname(path.realpath(__file__)), "pdfStyles.css")
    convertMarkdownToPdf(outputFilepath, md_content=rules, css_file_path=cssFilepath)

def convertMarkdownToPdf(pdf_file_path, md_content=None, md_file_path=None, css_file_path=None, base_url=None):
    raw_html = ''
    extras = ['cuddled-lists', 'tables']
    if md_file_path:
        raw_html = markdown_path(md_file_path, extras=extras)
    elif md_content:
        raw_html = markdown(md_content, extras=extras)

    if not len(raw_html):
        raise Exception('Input markdown seems empty')

    html = HTML(string=raw_html, base_url=base_url)

    css = []
    if css_file_path:
        css.append(CSS(filename=css_file_path))

    html.write_pdf(pdf_file_path, stylesheets=css)

async def convertRulesMdToHtml(rules, gameFolderPath):
    htmlContent = markdown(rules)

    with open(path.join(gameFolderPath, "rules.html"), 'w', encoding="utf-8") as rulesHtmlFile:
        rulesHtmlFile.write(htmlContent)

async def convertRulesMdToSpans(rules, gameFolderPath):

    fontSize = 18
    fontSizeProgression = 5

    htmlContent = markdown(rules)
    htmlContent = htmlContent.replace("\n", "")

    # This creates a newline at the beginning of doc
    htmlContent = htmlContent.replace("<h1>", "<tspan font-weight='bold' font-size='%spx'>\\n" % ((5*fontSizeProgression)+fontSize))
    htmlContent = htmlContent.replace("<h2>", "<tspan font-weight='bold' font-size='%spx'>\\n" % ((4*fontSizeProgression)+fontSize))
    htmlContent = htmlContent.replace("<h3>", "<tspan font-weight='bold' font-size='%spx'>\\n" % ((3*fontSizeProgression)+fontSize))
    htmlContent = htmlContent.replace("<h4>", "<tspan font-weight='bold' font-size='%spx'>\\n" % ((2*fontSizeProgression)+fontSize))
    htmlContent = htmlContent.replace("<h5>", "<tspan font-weight='bold' font-size='%spx'>\\n" % ((1*fontSizeProgression)+fontSize))

    htmlContent = htmlContent.replace("</h1>", "</tspan>\\n")
    htmlContent = htmlContent.replace("</h2>", "</tspan>\\n")
    htmlContent = htmlContent.replace("</h3>", "</tspan>\\n")
    htmlContent = htmlContent.replace("</h4>", "</tspan>\\n")
    htmlContent = htmlContent.replace("</h5>", "</tspan>\\n")

    htmlContent = htmlContent.replace("<p>", "<tspan font-size='18px'>")
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