# Templative

Define the cards you’d like created and how to assemble them, use the CLI, and purchase the game off of the Game Crafter.

# Requirements
- xcode
- xcode-select --install
- Install [XQuartz](https://www.xquartz.org/) for OSX
- [Inkscape v1](https://inkscape.org)
- Install `Install Certificates.command` located in Python3.8 application directory if you haven't already.
- `brew tap thenextguy32/homebrew-templative`
- `brew install templative`
- Update `/usr/local/etc/Imagemagick-7/delegates.yml` file to use `export-file` instead of `export-png` as noted in the comment near the middle of the file.

## QuickStart
- Create and cd into a directory
- `templative init`
- `templative produce` to create a version of the game. 

### Uploading
- Create an account on the [Game Crafter](https://www.thegamecrafter.com)
- Get an [api key](https://www.thegamecrafter.com/account/apikeys) from the Game Crafter
- Add the `THEGAMECRAFTER_PUBLIC_KEY`, `THEGAMECRAFTER_USERNAME`, and `THEGAMECRAFTER_PASSWORD` to your [env vars](https://www.schrodinger.com/kb/1842)
- `templative upload` to upload the last produced version to the Game Crafter.

Use `templative --help` for more info.

## Creating a New Component

- Create a new csv file within the `piecesGamedataDirectory` defined in the `game-compose`
- Create a new json file within the `componentGamedataDirectory` defined in the `game-compose`
- Define an svg template within the `artTemplatesDirectory` defined in the `game-compose`. See the [Artfile Guide](###-Artfile-Guide)
- Define an art metadata doc within the `artdataDirectory` defined in the `game-compose`. See [Defining Art Metadata](###-Defining-Art-Metadata)
- Create a new component within `component-compose.json` that specifies in the filesnames of the files created above.

### Defining Gamedata

Gamedata files are csv's that contain rows of piece data. All gamedata files must include the headers `name`, `displayName`, `quantity`.

### Artfiles

Art files must have a `viewbox` that matches the gamecrafter specifications. For instance if poker cards require 825px by 1125px then the viewbox must be `0 0 825 1125` and the document size must specify px with width at `825px` and height at `1125px`. Viewbox inherits the units of the width and height.

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


## Component Definition Types - Deprecated

### Mono

- `topArtData` and `bottomArtdata` defined in component compose.
- No `piecesGamedata`.

## Multi

- Has `frontArtdata` and `backArtdata` defined in component compose.
- Has `piecesGamedata`. 
- A piece is created for every piece row defined in the gamedata.
- All pieces has the same front and back artdata.

## Multi Variant

- No artdata in component compose.
- Has `piecesGamedata`.
- Expects a `frontArtdata` and `backArtdata` columns in pieces gamedata.
- A piece is created for every piece of row defined in the gamedata.
- Each piece has a unique front and back artdata.
