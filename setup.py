from setuptools import setup, find_packages

setup(
    name = "templative",
    version = "0.3.10",
    author = "Oliver Barnum",
    author_email = "oliverbarnum32@gmail.com",
    description = "Create GameCrafter games based on art templates, json, and csvs.",
    url = "",
    install_requires=[
        "aiofile",
        "aiohttp",
        "asyncclick",
        "fpdf",
        "fpdf2",
        "GitPython",
        "markdown2",
        "Pillow",
        "svgmanip",
        "svgutils",
        "tabulate",
        "Wand",
        "weasyprint"
    ],
    entry_points = {
        "console_scripts": [
            "templative=templative:cli"
        ]
    },
    packages=["templative"],
    package_data={"": ["create/componentTemplates/*.svg", "produce/*.css"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)