# Templative

Define the cards you’d like created and how to assemble them, use the CLI, and purchase the game off of the Game Crafter.

# Install



inkscape "C:\Users\User\Documents\git\studio-tyrus\apcw\apcw-defines\output\capsAndHammers_1.2.51_PaxSouth_2023-01-26_06-27-37\capsAction\capsAction-admiral.svg" --export-filename="C:\Users\User\Documents\git\studio-tyrus\apcw\apcw-defines\output\capsAndHammers_1.2.51_PaxSouth_2023-01-26_06-27-37\capsAction\capsAction-admiral.png" --export-dpi="96" --export-background="rgb(100%,100%,100%)" --export-background-opacity="1"

## OSX
- Install Python3 and pip3.
- Install xcode
- `xcode-select --install`
- Install [XQuartz](https://www.xquartz.org/) for OSX
- [Inkscape v1](https://inkscape.org)
- Install `Install Certificates.command` located in Python3.* application directory if you haven't already.
- `brew tap thenextguy32/homebrew-templative`
- `brew install templative`
- Update `/usr/local/etc/Imagemagick-7/delegates.yml` or `/usr/local/Cellar/imagemagick/7.0.10-0/etc/ImageMagick-7/delegates.xml` file to use `export-file` instead of `export-png` as noted in the comment near the middle of the file.'

## Windows
- Install Python3.
- Install [ImageMagick](https://imagemagick.org/script/download.php#windows).
- Install [Inkscape](https://inkscape.org).
- Add `C:\Program Files\Inkscape\bin` to path.
- Update `C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\delegates.xml` to use Inkscape for svg to png conversions `<delegate decode="svg:decode" stealth="True" command="&quot;inkscape&quot; &quot;%s&quot; --o=&quot;%s&quot; --export-dpi=&quot;%s&quot; --export-background=&quot;%s&quot; --export-background-opacity=&quot;%s&quot; &gt; &quot;%s&quot; 2&gt;&amp;1"/>`
- Install [GTK](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases).
- Add `C:\Program Files\GTK3-Runtime Win64\bin` to path.
- `python setup.py develop`
- `pip install -U wand`
- `pip install -U weasyprint`

## QuickStart
- Create and cd into a directory
- `templative init`
- `templative produce` to create a version of the game. 

### Uploading
- Create an account on the [Game Crafter](https://www.thegamecrafter.com)
- Get an [api key](https://www.thegamecrafter.com/account/apikeys) from the Game Crafter
- Add the `THEGAMECRAFTER_PUBLIC_KEY`, `THEGAMECRAFTER_USERNAME`, and `THEGAMECRAFTER_PASSWORD` to your [user env vars](https://www.schrodinger.com/kb/1842)
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

# Deep Dive Troubleshooting
Python3 alias quickfix:
`vim ~/.bashrc`

```
alias python=python3
alias pip=pip3
alias templative="/usr/local/bin/templative"
```

`source ~/.bashrc`

Miniconda2 errors:
`/usr/local/bin/templative produce`

Python3 setuptools not found:
`python3 -m pip install --upgrade setuptools`

If you see: `wand.exceptions.DrawError: non-conforming drawing primitive definition `letter-spacing' @ error/draw.c/RenderMVGContent/4434`
It's because you need to update the delegates.xml. Line 113~114 should equal:
`  <!-- Change export-png to export-file for inkscape 1.0+ -->
  <delegate decode="svg:decode" stealth="True" command="&quot;inkscape&quot; &quot;%s&quot; --o=&quot;%s&quot; --export-dpi=&quot;%s&quot; --export-background=&quot;%s&quot; --export-background-opacity=&quot;%s&quot; &gt; &quot;%s&quot; 2&gt;&amp;1"/>`

