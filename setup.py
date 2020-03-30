import setuptools

setuptools.setup(
    name = "templative",
    version = "1.0.0",
    author = "Oliver Barnum",
    author_email = "oliverbarnum32@gmail.com",
    description = "Populate svgs using csvs, output jpg images, and upload them to the Game Crafter",
    url = "",
    packages=["templative"],
    install_requires=["aiofile", "aiohttp", "appdirs", "async-timeout", "attrs", "cairocffi", "CairoSVG", "certifi", "cffi", "chardet", "click", "cssselect2", "defusedxml", "distlib", "docopt", "ensure", "filelock", "h11", "h2", "hpack", "html5lib", "http3", "hyperframe", "idna", "lxml", "markdown2", "md2pdf", "mpmath", "multidict", "pbr", "Pillow", "pycparser", "Pyphen", "requests", "requests-async", "rfc3986", "six", "stevedore", "svgutils", "tabulate", "tinycss2", "urllib3", "virtualenv", "virtualenv-clone", "virtualenvwrapper", "Wand", "WeasyPrint", "webencodings", "yarl"],
    entry_points = {
        "console_scripts": ["templative=templative.cli:cli"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)