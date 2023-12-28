# from markdown2 import markdown, markdown_path
# from md2pdf.core import md2pdf
from os import path

async def produceRulebook(rules, gameFolderPath):
    outputFilepath = path.join(gameFolderPath, "rules.pdf")
    # convertMarkdownToPdf(rules, outputFilepath)

# def convertMarkdownPathToHtml(markdownPath, md_content=None, md_file_path=None, css_file_path=None, base_url=None):
#     raw_html = ''
#     extras = ['cuddled-lists', 'tables']
#     if md_file_path:
#         raw_html = markdown_path(md_file_path, extras=extras)
#     elif md_content:
#         raw_html = markdown(md_content, extras=extras)
#     else:
#         raise Exception("Missing markdown data.")

#     if not len(raw_html):
#         raise Exception('Input markdown seems empty.')
    
#     return raw_html

# def convertHtmlToPdf(html):
#     cssFilepath = path.join(path.dirname(path.realpath(__file__)), "pdfStyles.css")
#     from weasyprint import HTML, CSS
#     html = HTML(string=raw_html, base_url=base_url)

#     css = []
#     if css_file_path:
#         css.append(CSS(filename=css_file_path))

#     html.write_pdf(pdf_file_path, stylesheets=css)

# def convertMarkdownToPdf(markdownString, outputPath):
#     md2pdf(outputPath, md_content=markdownString)
