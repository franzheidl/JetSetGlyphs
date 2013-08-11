from AppKit import *
from vanilla import *
from mojo.roboFont import *
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.extensions import ExtensionBundle
from PyASOpenFileDialog import ASOpenFileDialog
from PyASSaveFileDialog import ASSaveFileDialog
import subprocess
import os


class JetSetGlyphs(BaseWindowController):

    def __init__(self):
        self.bundle = ExtensionBundle("JetSetGlyphs")
        #self.resourcesPath = self.bundle.resourcesPath()
        self.sourceFont = False
        self.targetFont = False
        self.sourceName = ""
        self.sourceGlyphs = []
        self.targetGlyphs = []
        
        self.w = Window((10, 20, 240, 560), "JetSetGlyphs", minSize=(240, 450))
        self.w.importFontButton = Button((20, 10, -20, 20), "Import from Font", sizeStyle="small", callback=self.ImportFontGlyphs)
        self.w.importFileButton = Button((20, 35, -20, 20), u"Import from File \u2026", sizeStyle="small", callback=self.ImportFileGlyphs)
        self.w.departBox = Box((10, 65, -10, 100))
        self.w.departIcon = ImageView((18, 72, 28, 28))
        self.w.departIcon.setImage(imageObject=(self.bundle.get("departures")))
        self.w.departTitle = TextBox((50, 70, -10, 20), "Departures")
        self.w.departCount = TextBox((50, 88, -10, 16), "--", sizeStyle="small")
        self.w.arriveBox = Box((10, -140, -10, -95))
        self.w.arriveIcon = ImageView((18, -130, 28, 28))
        self.w.arriveIcon.setImage(imageObject=(self.bundle.get("arrivals")))
        self.w.glyphList = List((10, 105, -10, -135), [], enableDelete=True, editCallback=self.UpdateArrivalCount)
        self.w.glyphList.enable(0)
        self.w.arriveTitle = TextBox((50, -132, -10, 20), "Arrivals")
        self.w.arriveCount = TextBox((50, -114, -10, 16), "--", sizeStyle="small")
        self.w.CreateGlyphsButton = Button((20, -85, -20, 20), "Create Glyphs in Font", sizeStyle="small", callback=self.CreateGlyphs)
        self.w.ExportGlyphsButton = Button((20, -60, -20, 20), u"Export Glyphset to File \u2026", sizeStyle="small", callback=self.ExportGlyphs)
        self.w.CopyToClipBoardButton = Button((20, -35, -20, 20), "Copy Glyphset to Clipboard", sizeStyle="small", callback=self.CopyToClipBoard)
        self.w.open()
        
    def ImportFontGlyphs(self, sender):
        self.sourceFont = CurrentFont()
        if self.sourceFont == None:
            self.showMessage(u"Ergh\u2026", "Open a font to get a glyphset from!")
        else:
            self.sourceGlyphs = self.sourceFont.lib["public.glyphOrder"]
            self.w.glyphList.enable(1)
            self.w.glyphList.set(self.sourceGlyphs)
            if self.sourceFont.info.familyName != None:
                self.sourceName = self.sourceFont.info.familyName
            else:
                self.sourceName = "Unnamed"
            if self.sourceFont.info.styleName != None:
                self.sourceName = self.sourceName + " " + self.sourceFont.info.styleName
            
            self.UpdateDepartureCount()
            self.UpdateArrivalCount(self.w.glyphList)
    
    def CreateGlyphs(self, sender):
        self.targetFont = CurrentFont()
        
        if len(self.sourceGlyphs) > 0:
            if self.targetFont != None:
                if self.targetFont != self.sourceFont:
                    self.targetGlyphs = self.targetFont.lib["public.glyphOrder"]
                    
                    targetGlyphOrder = self.targetGlyphs
                    sourceGlyphOrder = self.w.glyphList.get()
                    newGlyphOrder = targetGlyphOrder
                    
                    for glyph in sourceGlyphOrder:
                        if glyph not in targetGlyphOrder:
                            newGlyphOrder.append(glyph)
                            
                    newGlyphOrder.sort()
                    self.targetFont.glyphOrder = newGlyphOrder
                    self.targetFont.update()
                else:
                    self.showMessage(u"Ergh\u2026", "You are trying to apply a glyphset to the font you took it from!")
            else:
                self.showMessage(u"Ouch\u2026", "There needs to be an open font to apply the glyphset to!")
        else:
            self.showMessage(u"Ergh\u2026", "No glyphs have been imported yet.")
    
    
    def ImportFileGlyphs(self, sender):
        filePath = ASOpenFileDialog(type="public.plain-text").result()
        if filePath != "False":
            self.sourceName = os.path.basename(filePath)
            # read file
            f = open(str(filePath), "r")
            glyphString = f.read()
            f.close()
            # create list from string
            self.sourceGlyphs = glyphString.split(" ")
            # update list and text above list
            self.w.glyphList.enable(1)
            self.w.glyphList.set(self.sourceGlyphs)
            self.UpdateDepartureCount()
            
    
    def ExportGlyphs(self, sender):
        charSet = self.GlyphSetString()
        filePath = ASSaveFileDialog(defaultName="glyphset.txt").result()
        if filePath != "False":
            f = open(str(filePath), "w")
            f.write(charSet)
            f.close()
    
        
    def CopyToClipBoard(self, sender):
        charSet = self.GlyphSetString()
        subprocess.Popen(['osascript', '-e', 'set the clipboard to ' + '\"' + charSet + '\"'])
        
    def UpdateDepartureCount(self):
        dCount = str(len(self.sourceGlyphs)) + " glyphs from " + self.sourceName
        self.w.departCount.set(dCount)
           
    def UpdateArrivalCount(self, sender):
        aCount = str(len(sender.get())) + " glyphs from " + self.sourceName
        self.w.arriveCount.set(aCount)
    
    def GlyphSetString(self):
        glyphSet = self.w.glyphList.get()
        glyphSet = " ".join([aGlyph for aGlyph in glyphSet if aGlyph])
        return glyphSet
        
JetSetGlyphs()
