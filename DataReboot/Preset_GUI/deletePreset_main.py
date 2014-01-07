'''
7/30/2013
Sean McLaughlin
Companion Module for deletePreset. Opens a small window which allows the user to delete presets. 
'''

if __name__ == '__main__':
    print '''This small widget allows the user to delete a preset. It shows a combo box and a text view, and the current selection of the box in the display. 
    When delete is clicked, the changes are written to file. The method currently closes itself but that is not necessary. 
    '''

from PyQt4 import QtGui, QtCore
from deletePreset import Ui_deletePreset

def parseKeyValue(line):
    # a function that will take a line and split it along the equals sign and make a tuple
    #i've used copies of this a few other places in the code as well. 
    splitLine = line.split('=')
    if len(splitLine) != 2:
        return None, None #if the length is not 2, this line may be blank, or not have a key value
    return (splitLine[0].strip(), splitLine[1].strip())

class deletePreset(QtGui.QWidget):
    
    def __init__(self, presetFilename, parent = None):
        super(deletePreset, self).__init__(parent)
        self.ui = Ui_deletePreset()
        self.ui.setupUi(self)
        
        #instance variables. 
        self.PRESETFilename = presetFilename
        
        self.presetDict = {}
        with  open(self.PRESETFilename, 'r') as presetFile:
            for line in presetFile: #gather all the names from the preset file in a dictionary, and include all the info in the value
                key, value = parseKeyValue(line)
                if  key == 'Name':
                    self.presetDict[value] = ''
                    lastName =value
                else:
                    self.presetDict[lastName] += key + '  =  ' + value + '\n'
        
        self.ui.combo_preset.addItems(self.presetDict.keys())
        self.display_current()
        
        #signals and slots
        self.ui.combo_preset.currentIndexChanged.connect(self.display_current)
        self.ui.button_del.clicked.connect(self.del_preset)
        
    def del_preset(self):
        currentPreset = str(self.ui.combo_preset.currentText())
        lines = []
        with open(self.PRESETFilename, 'r') as presetFile:
            for line in presetFile:
                lines.append(line)
        
        out = []
        index = 0
        while index != len(lines): #It should be possible to rewrite this without clumbsy indicies, using a boolean write/don't write variable. 
            key, value = parseKeyValue(lines[i])
            
            if key == 'Name' and value == currentPreset:#we've found the one to delete
                while lines[index] != 'END\n': #skip the rest of it
                    index+=1
                index +=1 #we need to skip END too. 
            else:
                out.append(lines[index])
            index+=1
                
        with  open(self.PRESETFilename, 'w') as presetFile:
            presetFile.write(''.join(out))
        
        self.close() #dont' know if I want to close here or go through al the boxes and make sure that things are ok
                
    
    def display_current(self): #displays the preset that's currently in the combo box. 
        currentPreset = str(self.ui.combo_preset.currentText())
        self.ui.textBrowser.clear()
        self.ui.textBrowser.insertPlainText(self.presetDict[currentPreset])
        