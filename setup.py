import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "templative",
    version = "0.0.2",
    author = "Oliver Barnum",
    author_email = "oliverbarnum32@gmail.com",
    description = "Populate svgs using csvs, output jpg images, and upload them to the Game Crafter",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "",
    install_requires=[
        "certifi==2019.11.28"
        "chardet==3.0.4"
        "click==7.1.1"
        "cssselect2==0.2.0"
        "DateTime==4.3"
        "ensure==1.0.0"
        "idna==2.9"
        "lxml==4.5.0"
        "mpmath==1.1.0"
        "Pillow==6.2.2"
        "pyparsing==2.4.6"
        "pytz==2019.3"
        "reportlab==3.5.42"
        "requests==2.23.0"
        "six==1.14.0"
        "svglib==0.9.4"
        "svgmanip==0.0.6"
        "svgutils==0.3.1"
        "svgwrite==1.3.1"
        "tabulate==0.8.7"
        "tinycss2==0.6"
        "urllib3==1.258"
        "Wand==0.5.9"
        "webencodings==0.5.1"
        "zope.interface==5.0.1"
    ],
    entry_points = {
        "console_scripts": ["templative=templative.cli:cli"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires="==3.8.2",
)