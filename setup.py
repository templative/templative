from setuptools import setup, find_packages

setup(
    name = "templative",
    version = "0.3.10",
    author = "Oliver Barnum",
    author_email = "oliverbarnum32@gmail.com",
    description = "Create GameCrafter games based on art templates, json, and csvs.",
    url = "",
    packages=find_packages(),
    install_requires=["asyncio", "aiofile", "click", "markdown2", "WeasyPrint", "ensure", "svgutils", "wand", "mpmath", "tabulate", "aiohttp", "svgmanip"],
    entry_points = {
        "console_scripts": [
            "templative=templative:cli"
        ]
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)