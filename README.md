JetSetGlyphs
============
An extension for RoboFont to transfer glyphsets across fonts in style.

![JetSetGlyphs Screenshot](http://github.com/franzheidl/jetsetglyphs/raw/master/screenshots/jetsetglyphs.png)



##Installation
Use [Mechanic](https://github.com/jackjennings/Mechanic) or clone the repo and doubleclick JetSetGlyphs.roboFontExt to install.

## Usage

### Import Glyphset From Font
Import the entire glyphset from the current font.

### Import Glyphset From File
Import a glyphset from a space-separated .txt-file.

### Edit Glyphset In-Flight
To add glyphs to the glyphset click the "+"-button in the toolbar. Enter mutliple glyphs by entering their names space-separated.
To remove glyphs from the passenger list, click-select them in the list and click the "-"-button in the toolbar. Hold Shift to select multiple glyphs.

### Create Glyphs In Font
Create the glyphs from your imported/edited glyphset in the current font. Glyphs that already exist in the current font will be respected, only glyphs that are not present in your current font will be created as template glyphs.

***Warning: Creating Glyphs can not be undone.***

### Export Glyphset to File
Create a space-separated .txt-file of your imported/edited glyphset.

### Copy Glyphset to Clipboard
Copy a space-separated string of your glyphset to the clipboard, ideal for pasting into a new default character set at RoboFont > Preferences > Character Set.

### Update JetSetGlyphs
Use [Mechanic](https://github.com/jackjennings/Mechanic) to update or pull from github and re-install manually.


### Changelist
**v1.4** Filter glyhs, add glyphs, toolbar for adding and removing glyphs.

**v1.1.2** Update version number again to exit update loop bug introduced with v1.1.1.

**v1.1.1** Update version number in plist, no functional changes.

**v.1.1** Use Open/Save dialogs attached to window.

**v1.0** Initial Release.

##The MIT License (MIT)


Copyright (c) 2013 Franz Heidl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
