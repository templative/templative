import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "templative",
    version = "0.0.1",
    author = "Oliver Barnum",
    author_email = "oliverbarnum32@gmail.com",
    description = "Populate svgs using csv's, output jpg images, and upload them to the Game Crafter",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['templative=templative.cli:cli']
    },
    python_requires='>=2.7',
)