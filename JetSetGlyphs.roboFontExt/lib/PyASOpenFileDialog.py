# PyASOpenFileDialog
# A simple Python wrapper for an AppleScript Open File dialog.
# Franz Heidl 2013
# http://github.com/franzheidl/py-asalert-asdialog
# MIT license.


import subprocess
import os

class ASOpenFileDialog():
    
    def __init__(self, **kwargs):
        
        self.dialog = {}
        self.dialogString = 'set theFile to choose file'
        
        if "application" in kwargs.keys():
            self.application = kwargs["application"]
        else:
            self.application = "System Events"
        self.dialog["application"] = self.application
        self.applicationString = 'tell application \"' + self.application + '\"'
        
        
        if "prompt" in kwargs.keys():
            self.prompt = kwargs["prompt"]
            self.dialog["prompt"] = self.prompt
            self.dialogString += (' with prompt ' + '\"' + self.prompt + '\"')
            
            
        if "type" in kwargs.keys():
            self.ofType = (kwargs["type"]).split(", ")
            self.dialog["ofType"] = self.ofType
            self.ofTypeString = ', '.join([('\"' + aType + '\"') for aType in self.ofType if aType])
            self.dialogString += ' of type {' + self.ofTypeString + '}'
            
            
        if "defaultLocation" in kwargs.keys():
            defLoc = kwargs["defaultLocation"]
            if defLoc.startswith("~") or defLoc.startswith("/~"):
                defLoc = os.path.expanduser(defLoc)
            if not defLoc.startswith("/"):
                defLoc = "/" + defLoc
            if os.path.exists(defLoc):
                self.defaultLocation = defLoc
                self.dialog["defaultLocation"] = self.defaultLocation
                self.dialogString += (' default location (POSIX file \"' + self.defaultLocation + '\" as alias)')
          
            
        if "invisibles" in kwargs.keys():
            iv = kwargs["invisibles"]
            if iv == True or iv == "True":
                self.invisibles = kwargs["invisibles"]
                self.dialog["invisibles"] = True
                self.dialogString += ' invisibles true'
            else:
                self.invisibles = False
                self.dialog["invisibles"] = self.invisibles
                self.dialogString += ' invisibles false'
            
            
        if "multipleSelectionsAllowed" in kwargs.keys():
            mSA = kwargs["multipleSelectionsAllowed"]
            if mSA == True or mSA == "True":
                self.multipleSelectionsAllowed = kwargs["multipleSelectionsAllowed"]
                self.dialog["multipleSelectionsAllowed"] = True
                self.dialogString += ' with multiple selections allowed'
            else:
                self.multipleSelectionsAllowed = kwargs["multipleSelectionsAllowed"]
                self.dialog["multipleSelectionsAllowed"] = False
                
        
        if "showingPackageContents" in kwargs.keys():
            sPC = kwargs["showingPackageContents"]
            if sPC == True or sPC == "True":
                self.showingPackageContents = kwargs["showingPackageContents"]
                self.dialog["showingPackageContents"] = True
                self.dialogString += ' showing package contents'
            else:
                self.showingPackageContents = kwargs["showingPackageContents"]
                self.dialog["showingPackageContents"] = False
        

        self._result = self.displayOpenDialog(self.applicationString, self.dialogString)
        self.dialog["result"] = self._result
           
        
    def displayOpenDialog(self,theApplication, theDialog):
        self.output = subprocess.check_output(['osascript',
            '-e', 'set theFiles to {}',
            '-e', 'set thePFiles to {}',
            '-e', theApplication,
            '-e', 'activate',
            '-e', 'try',
            '-e', theDialog,
            '-e', 'set theFiles to theFiles & theFile',
            '-e', 'repeat with aFile in theFiles',
            '-e', 'if the length of thePFiles is greater than 1 then',
            '-e', 'set thePFiles to thePFiles & \", \" & (POSIX path of aFile) as text',
            '-e', 'else',
            '-e', 'set thePFiles to thePFiles & (POSIX path of aFile) as text',
            '-e', 'end if',
            '-e', 'end repeat',
            '-e', 'on error number -128',
            '-e', 'set thePFiles to \"False\"',
            '-e', 'end try',
            '-e', 'return thePFiles',
            '-e', 'end tell'])
        pathsString = self.output.strip()
        if pathsString != "False":
            if len(pathsString.split(", ")) > 1:
                paths = pathsString.split(", ")
            else:
                paths = pathsString
        else:
            paths = "False"
        return paths
    
    
    def result(self):
        if self._result:
            return self._result
        else:
            return False
            
            
    def canceled(self):
        if self._result == "False":
            return True
        else:
            return False
    
            
    def __repr__(self):
        return self.result()          
    