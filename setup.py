from setuptools import setup, find_packages

setup(
    name = "templative",
    version = "0.3.8",
    author = "Oliver Barnum",
    author_email = "oliverbarnum32@gmail.com",
    description = "Populate svgs using csvs, output jpg images, and upload them to the Game Crafter",
    url = "",
    packages=find_packages(),
    install_requires=["asyncio", "aiofile", "click", "markdown2", "WeasyPrint", "ensure", "svgutils", "wand", "mpmath", "tabulate", "aiohttp"],
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