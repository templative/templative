
# Templative

[Watch the explanation video!](https://youtu.be/cfaSQqnhyrE)

Templative allows you to assemble board games using json and svgs. To create a complete board game run the following commands:

- `templative init`
- `templative create deckpoker --name potionDeck`
- `templative produce`
- `templative upload`
- `templative playground`
- `templative printout frontback`

Now you have a board game complete with a rules document, a potion deck, a package in Tabletop Playground, a listing on the GameCrafter ready for purchase, and a pdf ready for print-and-play. It's that powerful.

Use `templative --help` for more info.

# Installation

- Follow the OS specific prereqs below
- Install Python3.
- Install [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- `npm install svgexport`
- `git clone https://github.com/templative/templative.git`
- `cd templative`
- `python setup.py develop`
- `pip install -e .`

## OSX Prereqs

- Install [Xcode](https://apps.apple.com/us/app/xcode/id497799835?mt=12)
- `xcode-select --install`
- Install [Inkscape](https://inkscape.org), this make require [XQuartz](https://www.xquartz.org/)
- Install `Install Certificates.command` located in Python3.* application directory if you haven't already.

## Windows Prereqs
- Install [ImageMagick](https://imagemagick.org/script/download.php#windows).
- Add ImageMagick bin to your [path](https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10-with-screensho).
- Install [Inkscape](https://inkscape.org).
- Add `C:\Program Files\Inkscape\bin` to path. Inkscape has a Python installation within it, so take to care to order your Python and Inkscape path declarations.
- Install [GTK](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases).
- Add `C:\Program Files\GTK3-Runtime Win64\bin` to path.

# Usage

## Create a Project
- Create and cd into a directory
- `templative init`
- `templative produce` to create a version of the game in the output folder. 

## Creating Components

Create a new component in your game using the following command:

`templative create TYPE --name NAME`

Replace `TYPE` with the type of the component you'd like, and replace `NAME` with the name of your new component.

To see which component types Templative supports, run the following command (the following output may be outdated):

```
templative create

  Create components from templates

Commands:
  accordionpoker        Create a new poker sized accordion
  chitsquarelarge       Create a new medium ring
  deckpoker             Create a new poker sized deck
  ringlarge             Create a new large ring
  ringmedium            Create a new medium ring
  stoutboxsmall         Create a new small cardboard box
  tuckboxpoker108cards  Create a new poker sized tuckbox fitting 108 cards
```

Each component is defined in `component-compose.json`, and has a pieces csv/json file, a component json file, artdata files, template svgs, and overlaid svgs.

### Defining Gamedata

Gamedata files are csv and json files that contain data for each piece of each component. All gamedata files must include the `name`, `displayName`, `quantity`.

### Artfiles

Art files must have a `viewbox` that matches the gamecrafter specifications. For instance if poker cards require 825px by 1125px then the viewbox must be `0 0 825 1125` and the document size must specify px with width at `825px` and height at `1125px`. Viewbox inherits the units of the width and height.

Add the cmyk color profile in the Document Setup of Inkscape. This adds the following color file to the `<defs>` tag:
```
<color-profile
  name="Generic-CMYK-Profile"
  xlink:href="file:///System/Library/ColorSync/Profiles/Generic%20CMYK%20Profile.icc"
  id="color-profile161" />
</defs>
```

# Using ArtData

ArtData files are json files that contain instructions for how to assemble a piece jpg using art files and metadata.

Each piece begins as a copy of the template file defined in the `templateFilename` field of the artData file. For instance, a `templateFilename` of `action` would copy `art/templates/action.svg`.

An art metadata file can perform three types of commands: *text replacements*, *style updates*, and *overlays*.

What data Templative uses to perform the command depends on the scope of the command. Each command takes in data from the following supported scopes: `piece` from piece gamedata, `component` from component gamedata, `game` from `game.json`, `studio` from `studio.json`, `global` for literals. See examples of how data is used by each command type below.

## Text Replacements Commands

Text replacements find instances of the `{key}` and replace it with a sourced value.

Consider the following text replacements:

```
  "textReplacements": [
    { "scope": "game", "source": "displayName", "key": "gameName" },
    { "scope": "piece", "source": "points", "key": "power",  }
  ]
```

The first text replacement command replaces all instances of the text `{gameName}` in the template svg with the value of the `displayName` field in the `game.json` file.

The second text replacement replaces all instances of `{power}` with the `points` field of the current piece.

## Overlays

Overlays are svgs that we overlay on top of the copied svg template. Consider the two overlay commands below:

```
  "overlays": [
    { "scope": "piece", "source": "graphic" },
    { "scope": "global", "source": "versionQuantity" }
  ]
```

The first overlay looks in the `piece` gamedata file for a field called `graphic`. As an example, a piece's `graphic` field is `bossMonsterA`. This instructs Templative to overlay the svg `graphicalInserts/bossMonsterA.svg` on top of the template. 

The second overlay looks for `graphicalInserts/versionQuantity.svg`, as global implies a literal, non-lookup value.

Overlay commands are the first commands to occur. 

### Overlays

Overlays are svgs found in the `art/graphicalInserts` folder.

Overlays must be the same size as the template it is overlaying. For instance, both the poker card template svg and the overlay svg must be `825x1125px`.

## Style Updates

Style updates allow you to update a style attribute of a svg element at a given id. Consider the following style update:

```
  "styleUpdates":[
    { 
      "id": "background", 
      "cssValue": "fill", 
      "scope": "piece", 
      "source": "colorRGB" 
    }
  ]
```

This command looks for the xml element with the id `background` within the svg and replaces it's `fill` css value with the piece's `colorRGB` value.

Any valid css value for svgs is valid here.


## Uploading to the GameCrafter
- Create an account on the [Game Crafter](https://www.thegamecrafter.com)
- Get an [api key](https://www.thegamecrafter.com/account/apikeys) from the Game Crafter
- Add the `THEGAMECRAFTER_PUBLIC_KEY`, `THEGAMECRAFTER_USERNAME`, and `THEGAMECRAFTER_PASSWORD` to your [user env vars](https://www.schrodinger.com/kb/1842).
- Update `studio.json` with your designer id from the gamecrafter.
- `templative upload` to upload the last produced version to the Game Crafter.
- Visit the url generated at the end of uploading.

## Generating a Tabletop Playground Package

Create a Tabletop Playground package using the following command. 

`templative playground --output PACKAGESDIRECTORY`

Replace `PACKAGESDIRECTORY` with your own Tabletop Playground directory.

From the [Tabletop Playground wiki](https://tabletop-playground.com/knowledge-base/packages/), the packages directories are:
- Mac: `~/Library/Application\ Support/Epic/TabletopPlayground` (Note the `\ `)
- Linux: `~/.config/Epic/TabletopPlayground/Packages`
- Windows: `C:\Program Files (x86)\Steam\steamapps\common\TabletopPlayground\TabletopPlayground\PersistentDownloadDir`


