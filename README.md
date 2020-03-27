# Templative

Define the cards you’d like created and how to assemble them, use the CLI, and purchase the game off of the Game Crafter.

# Requirements
- [Inkscape 0.92.2](https://inkscape.org/release/inkscape-0.92.2/)
- Python 3.8.2

## QuickStart
- Install [XQuartz](https://www.xquartz.org/) for OSX
- `brew install cairo pango gdk-pixbuf libxml2 libxslt libffi`
- `pip3 install templative`
- Create and cd into a directory
- `templative init`
- Create `./output/`
- `templative produce` to create a version of the game. 

### Uploading
- Create an account on the [Game Crafter](https://www.thegamecrafter.com)
- Get an [api key](https://www.thegamecrafter.com/account/apikeys) from the Game Crafter
- Add the `THEGAMECRAFTER_PUBLIC_KEY`, `THEGAMECRAFTER_USERNAME`, and `THEGAMECRAFTER_PASSWORD` to your [env vars](https://www.schrodinger.com/kb/1842)
- `templative produce -u` to upload the game to the Game Crafter.

Use `templative --help` for more info.

## Usage

### Creating a New Component

- Create a new component within `components.json`
- Create a new csv doc within the `componentDataDirectory` defined in the `game-compose`
- Define an svg template within the `artTemplatesDirectory` defined in the `game-compose`. See the [Artfile Guide](###-Artfile-Guide)
- Define an art metadata doc within the `artdataDirectory` defined in the `game-compose`. See [Defining Art Metadata](###-Defining-Art-Metadata)

### Defining Gamedata

Gamedata files are csv's that contain rows of piece data. All gamedata files must include the headers `name`, `displayName`, `quantity`.

### Artfile Guide

- Art files must have a `viewbox` of `0 0 69.86129 95.265602`
- Document sizes must be `69.861 mm x 95.266 mm`

### Defining Art Metadata

Art metadata files are json files that contain instructions for how to assemble a piece jpg from art files.

Data piped into art files using art metadata can come from many sources. Currently data from the `game json blob`, `component json blob`, and `piece csv row` can be used to populate a file.

    { "scope": "game", "source": "displayName", "key": "gameName" }

This would replace all instance of {gameName} in the svg with the game's display name.

#### Text Replacements

Text replacements find instances of the {key} and replace it with the sourced value.

#### Overlays

Overlays are svgs that are overlaid on top of the template svg.

#### Style Updates

Style updates allow you to update a style attribute of a svg element at a given id.


