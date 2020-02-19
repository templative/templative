import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "tyruspipeline",
    version = "0.0.1",
    author = "Oliver Barnum",
    author_email = "oliverbarnum32@gmail.com",
    description = "Populate svgs using csv's, output jpg images, and upload them to the Game Crafter",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "",
    packages = ["tyruspipeline"],
    entry_points = {
        'console_scripts': ['tyruspipeline=tyruspipeline.cli:start']
    },
    install_requires=[
        "click", "svgutils", "requests"
    ],
    python_requires='>=2.7',
)