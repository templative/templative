### Further Reading

- [Auto line-wrapping in SVG Text](https://stackoverflow.com/questions/4991171/auto-line-wrapping-in-svg-text)
- [Multiline SVG Text](https://www.oreilly.com/library/view/svg-text-layout/9781491933817/ch04.html)
- [Foreign Object SVG Text](https://codepen.io/maxzz/pen/NzBGVE)

## Installation

- Update `delegates.xml` file to use Inkscape
```
<delegate decode="svg:decode" stealth="True" command="&quot;inkscape&quot; &quot;%s&quot; --o=&quot;%s&quot; --export-dpi=&quot;%s&quot; --export-background=&quot;%s&quot; --export-background-opacity=&quot;%s&quot; &gt; &quot;%s&quot; 2&gt;&amp;1"/>
```
- `cd` into Templative repo
- `python setup.py develop`
-	`pip install -e .`
- `pip show templative`

# Troubleshooting

## Non-Conforming Drawing Primitives
If you see: `wand.exceptions.DrawError: non-conforming drawing primitive definition `letter-spacing' @ error/draw.c/RenderMVGContent/4434`
It's because you need to update the delegates.xml. Line 113~114 should equal:
`  <!-- Change export-png to export-file for inkscape 1.0+ -->
  <delegate decode="svg:decode" stealth="True" command="&quot;inkscape&quot; &quot;%s&quot; --o=&quot;%s&quot; --export-dpi=&quot;%s&quot; --export-background=&quot;%s&quot; --export-background-opacity=&quot;%s&quot; &gt; &quot;%s&quot; 2&gt;&amp;1"/>`

## Delegates.xml Raw Attempt
inkscape "C:\Users\User\Documents\git\studio-tyrus\apcw\apcw-defines\output\capsAndHammers_1.2.51_PaxSouth_2023-01-26_06-27-37\capsAction\capsAction-admiral.svg" --export-filename="C:\Users\User\Documents\git\studio-tyrus\apcw\apcw-defines\output\capsAndHammers_1.2.51_PaxSouth_2023-01-26_06-27-37\capsAction\capsAction-admiral.png" --export-dpi="96" --export-background="rgb(100%,100%,100%)" --export-background-opacity="1"

# If you find a weird A carrot character, check your svgs for highlighted spaces in VSC.

## Why we use the Inkscape delegate
Inkscape support flow roots, which allows for naturally wrapping text without hyphens. This feature is invaluable as we do not know the length of texts we add to our art templates. This is a svg feature (of SVG 1.2?) that has not been universally adopted. The default wand delegate for svg->png throws out flowroots.

# Off Centered Text

Adding images sometimes messes with your svg. There isn't a consistent fix for this. Consider deleting images and remaking the text, testing that, then readding the image.