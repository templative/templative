from markdown2 import markdown, markdown_path
from weasyprint import HTML, CSS

def convertMarkdownToPdf(pdf_file_path, md_content=None, md_file_path=None, css_file_path=None, base_url=None):
    raw_html = ''
    extras = ['cuddled-lists', 'tables']
    if md_file_path:
        raw_html = markdown_path(md_file_path, extras=extras)
    elif md_content:
        raw_html = markdown(md_content, extras=extras)

    if not len(raw_html):
        raise ValidationError('Input markdown seems empty')

    html = HTML(string=raw_html, base_url=base_url)

    css = []
    if css_file_path:
        css.append(CSS(filename=css_file_path))

    html.write_pdf(pdf_file_path, stylesheets=css)
