from AppKit import *
from vanilla import *
from mojo.roboFont import *
from defconAppKit.windows.baseWindow import BaseWindowController
from defconAppKit.windows.progressWindow import ProgressWindow
from mojo.extensions import ExtensionBundle
import subprocess
import os
import re



class JetSetGlyphs(BaseWindowController):
    
    def __init__(self):
        self.bundle = ExtensionBundle("JetSetGlyphs")
        self.source_font = False
        self.target_font = False
        self.source_name = ""
        self.source_glyphs = []
        self.glyphset = []
        self.current_glyphs = []
        self.filtered = False
        self.w = Window((10, 20, 240, 560), "JetSetGlyphs", minSize=(240, 450))
        self.w.importFontButton = Button((20, 10, -20, 20), "Import from Font", sizeStyle="small", callback=self.ImportGlyphsFromFont)
        self.w.importFileButton = Button((20, 35, -20, 20), u"Import from File\u2026", sizeStyle="small", callback=self.ShowImportDialog)
        self.w.departBox = Box((10, 65, -10, 100))
        self.w.departPanel = Box((15, 70, -15, 36))
        self.w.departIcon = ImageView((21, 73, 28, 28))
        self.w.departIcon.setImage(imageObject=(self.bundle.get("departures")))
        self.w.departTitle = TextBox((54, 71, -10, 20), "Departures")
        self.w.departTitle.getNSTextField().setTextColor_(NSColor.colorWithCalibratedWhite_alpha_(0, 0.75))
        self.w.departCount = TextBox((54, 89, -10, 16), "--", sizeStyle="small")
        self.w.departCount.getNSTextField().setTextColor_(NSColor.colorWithCalibratedWhite_alpha_(0, 0.75))
        self.w.filterListBox = SearchBox((20, 110, -20, 20), sizeStyle="small", placeholder="Search", callback = self.FilterGlyphListView)
        self.w.arriveBox = Box((10, -160, -10, -92))
        self.w.arrivePanel = Box((15, -134, -15, 36))
        self.w.arriveIcon = ImageView((21, -131, 28, 28))
        self.w.arriveIcon.setImage(imageObject=(self.bundle.get("arrivals")))
        self.w.glyphList = List((10, 135, -10, -154), [], enableDelete=False, selectionCallback=self.ToggleEnableRemoveGlyphsButton)
        self.w.glyphList.enable(0)
        self.w.glyphListToolbar = Box((13, -153, -13, 10))
        self.w.glyphListToolbar.getNSBox().setBoxType_(NSBoxCustom)
        self.w.glyphListToolbar.getNSBox().setBorderType_(NSLineBorder)
        self.w.glyphListToolbar.getNSBox().setFillColor_(NSColor.colorWithPatternImage_(self.bundle.get("toolbar")))
        self.w.addGlyphsButton = ImageButton((10, -156, 30, 18), imageObject=(self.bundle.get("add")), sizeStyle="mini", callback=self.ShowAddGlyphItemsSheet)
        self.w.removeGlyphsButton = ImageButton((39, -156, 30, 18), imageObject=(self.bundle.get("remove")), sizeStyle="mini", callback=self.RemoveGlyphItems)
        self.w.addGlyphsButton.getNSButton().setBezelStyle_(NSSmallSquareBezelStyle)
        self.w.removeGlyphsButton.getNSButton().setBezelStyle_(NSSmallSquareBezelStyle)
        self.w.removeGlyphsButton.getNSButton().setEnabled_(NO)
        self.w.glyphListToolbar.getNSBox().setBorderColor_(NSColor.colorWithCalibratedWhite_alpha_(0, 0.35))
        self.w.arriveTitle = TextBox((54, -134, -10, 20), "Arrivals")
        self.w.arriveTitle.getNSTextField().setTextColor_(NSColor.colorWithCalibratedWhite_alpha_(0, 0.75))
        self.w.arriveCount = TextBox((54, -116, -10, 16), "--", sizeStyle="small")
        self.w.arriveCount.getNSTextField().setTextColor_(NSColor.colorWithCalibratedWhite_alpha_(0, 0.75))
        self.w.CreateGlyphsButton = Button((20, -85, -20, 20), "Create Glyphs in Font", sizeStyle="small", callback=self.CreateGlyphsInFont)
        self.w.ExportGlyphsButton = Button((20, -60, -20, 20), u"Export Glyphset to File\u2026", sizeStyle="small", callback=self.ShowExportDialog)
        self.w.CopyToClipBoardButton = Button((20, -35, -20, 20), "Copy Glyphset to Clipboard", sizeStyle="small", callback=self.CopyGlyphsetToClipboard)
        self.ToggleEnableButtons()
        self.w.open()
        
        
    def ImportGlyphsFromFont(self, sender):
        self.source_font = CurrentFont()
        if self.source_font == None:
            self.showMessage(u"Ergh\u2026", "Open a font to get a glyphset from!")
        else:
            self.source_glyphs = self.GetAllGlyphsFromFont(self.source_font)
            
            if self.source_font.info.familyName != None:
                self.source_name = self.source_font.info.familyName
            else:
                self.source_name = "Unnamed"
            if self.source_font.info.styleName != None:
                self.source_name = self.source_name + " " + self.source_font.info.styleName
            self.glyphset = self.source_glyphs
            self.UpdateGlyphListView(self.glyphset)
            self.UpdateDepartureInfo()
            self.UpdateArrivalInfo()
            self.ResetFilter()
        
    
    def ImportGlyphsFromFile(self, result):
        file_path = str(result[0])
        self.source_name =os.path.basename(file_path)
        f = open(file_path, "r")
        f_str = f.read()
        f.close()
        self.source_glyphs = f_str.split(" ")
        self.glyphset = self.source_glyphs
        self.UpdateGlyphListView(self.glyphset)
        self.UpdateDepartureInfo()
        self.UpdateArrivalInfo()
        self.ResetFilter()
        
        
    def UpdateGlyphListView(self, g_list):
        self.w.glyphList.enable(1)
        self.w.glyphList.set(g_list)
        self.ToggleEnableButtons()
        
    
    def CreateGlyphsInFont(self, sender):
        self.target_font = CurrentFont()
        if len(self.glyphset) > 0:
            if self.target_font != None:
                if self.target_font != self.source_font:
                    
                    newGlyphOrder = self.GetAllGlyphsFromFont(self.target_font)
                    
                    self.w.progressWindow = ProgressWindow(u"Creating Glyphs\u2026", parentWindow=self.w)
                    
                    for glyph in self.glyphset:
                        if glyph not in newGlyphOrder:
                            newGlyphOrder.append(glyph)
                            
                    newGlyphOrder.sort()
                    self.target_font.glyphOrder = newGlyphOrder
                    self.target_font.update()
                    
                    self.w.progressWindow.close()
                    
                else:
                    self.showMessage(u"Ergh\u2026", "You are trying to apply a glyphset to the font you took it from!")
            else:
                self.showMessage(u"Ouch\u2026", "There needs to be an open font to apply the glyphset to!")
        else:
            self.showMessage(u"Ergh\u2026", "No glyphs have been imported yet.")
        
        
    def ExportGlyphsToFile(self, result):
        f = open(str(result), "w")
        f.write(self.GlyphSetToString())
        f.close()
        
        
    def CopyGlyphsetToClipboard(self, sender):
        charSet = self.GlyphSetToString()
        subprocess.Popen(['osascript', '-e', 'set the clipboard to ' + '\"' + charSet + '\"'])
    
        
    def FilterGlyphListView(self, sender):
        search_for = sender.get().strip()
        regex = re.compile(".*(" + search_for + ").*")
        matches = [match.group(0) for c in self.glyphset for match in [regex.search(c)] if match]
        if len(self.glyphset) > 0:
            if search_for != "" or search_for != " ":
                self.UpdateGlyphListView(matches)
                self.filtered = search_for
            else:
                self.UpdateGlyphListView(self.glyphset)
                self.filtered = False
        
        
    def ShowAddGlyphItemsSheet(self, sender):
        self.addGlyphsSheet = Sheet((300, 200), self.w)
        self.addGlyphsSheet.input = TextEditor((10, 10, -10, 150), "")
        self.addGlyphsSheet.cancelButton = Button((-150, -30, 50, 20), "Cancel", sizeStyle="small", callback=self.CancelAddItems)
        self.addGlyphsSheet.addButton = Button((-90, -30, 80, 20), "Add Glyphs", sizeStyle="small", callback=self.AddGlyphItems)
        self.addGlyphsSheet.setDefaultButton(self.addGlyphsSheet.addButton)
        self.addGlyphsSheet.open()
        
        
    def AddGlyphItems(self, sender):
        input_str = str(self.addGlyphsSheet.input.get())
        if input_str != "":
            add_glyphs = input_str.split(" ")
            for a_glyph in add_glyphs:
                a_glyph = a_glyph.strip()
            new_glyphs = self.glyphset
            for a in add_glyphs:
                if a != "" and a not in new_glyphs:
                    new_glyphs.append(a)
            self.glyphset = new_glyphs
            self.UpdateGlyphListView(self.glyphset)
            self.UpdateArrivalInfo()
            
            if self.filtered:
                self.FilterGlyphListView(self.w.filterListBox)
            
        self.addGlyphsSheet.close()
        
        
        
    def CancelAddItems(self, sender):
        self.addGlyphsSheet.close()
        
    
    def RemoveGlyphItems(self, sender):
        rem_index = self.w.glyphList.getSelection()
        visible_glyphs = self.w.glyphList.get()
        if len(rem_index) > 0:
            rem_glyphs = [i for j, i in enumerate(visible_glyphs) if j in rem_index]
            
            for rem_glyph in rem_glyphs:
                if rem_glyph in self.glyphset:
                    self.glyphset.remove(rem_glyph)
                if rem_glyph in visible_glyphs:
                    visible_glyphs.remove(rem_glyph)
                        
            self.UpdateGlyphListView(visible_glyphs)
            self.UpdateArrivalInfo()
            if len(self.glyphset) == 0:
                self.source_name = ""
                self.UpdateDepartureInfo()
        
        
    def ShowImportDialog(self, sender):
        self.showGetFile(["public.plain-text"], self.ImportGlyphsFromFile)
        
    
    def ShowExportDialog(self, sender):
        self.showPutFile(["public.plain-text"], self.ExportGlyphsToFile, fileName = "glyphset.txt")


    def ResetFilter(self):
        self.w.filterListBox.set("")
        
    
    def UpdateDepartureInfo(self):
        d_len = len(self.w.glyphList.get())
        if d_len > 0:
            if d_len == 1:
                d_g_term = " glyph"
            else:
                d_g_term = " glyphs"
            if self.source_name:
                d_count = str(d_len) + d_g_term + " from " + self.source_name
            else:
                d_count = str(d_len) + d_g_term
        else:
            d_count = "--"
        self.w.departCount.set(d_count)
        
        
    def UpdateArrivalInfo(self):
        a_len = len(self.glyphset)
        if a_len > 0:
            if a_len == 1:
                g_a_term = " glyph"
            else:
                g_a_term = " glyphs"
            a_count = str(len(self.glyphset)) + g_a_term
        else:
            a_count = "--"
        self.w.arriveCount.set(a_count)
        
        
    def ToggleEnableRemoveGlyphsButton(self, sender):
        if len(self.w.glyphList.getSelection()) > 0:
            self.w.removeGlyphsButton.getNSButton().setEnabled_(YES)
        else:
            self.w.removeGlyphsButton.getNSButton().setEnabled_(NO)
   
    
    def ToggleEnableButtons(self):
        if len(self.glyphset) > 0:
            self.w.CreateGlyphsButton.getNSButton().setEnabled_(YES)
            self.w.ExportGlyphsButton.getNSButton().setEnabled_(YES)
            self.w.CopyToClipBoardButton.getNSButton().setEnabled_(YES)
        else:
            self.w.CreateGlyphsButton.getNSButton().setEnabled_(NO)
            self.w.ExportGlyphsButton.getNSButton().setEnabled_(NO)
            self.w.CopyToClipBoardButton.getNSButton().setEnabled_(NO)
    
    
    def GetAllGlyphsFromFont(self, f):
        all_glyphs = f.lib["public.glyphOrder"]
        for g in f.glyphOrder:
            if g not in all_glyphs:
                al_glyphs.append(g)
        return all_glyphs
           
          
    def GlyphSetToString(self):
        glyph_set = self.glyphset
        glyph_set = " ".join([aGlyph for aGlyph in glyph_set if aGlyph])
        return glyph_set
        
        
JetSetGlyphs()
