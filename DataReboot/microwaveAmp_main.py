'''
8/9/2013
Sean McLaughlin
Companion to the auto-generated microwaveAmp.py. Allows the use to set 
'''

import sys
from PyQt4 import QtGui, QtCore
from microwaveAmp import Ui_Form

class Start(QtGui.QWidget):
    
    class setAmpError(Exception):  # an error for this widget to return if there is a problem . 
        
        def __init__(self, value = None):
            self.value = value
            
        def __str__(self):
            if self.value != None:
                return str(self.value)
            return 'There was a problem setting the amplitude.'
    
    def __init__(self, microwaveSetters, parent = None):
        super(Start ,self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.microwaveSetters = microwaveSetters
        
        if not self.microwaveSetters:
            raise self.setAmpError, 'There are no microwave setters configured.'
        
        for name in self.microwaveSetters:
            self.ui.combo_MSobj.addItem(name)
            
        top = microwaveSetters[self.ui.combo_MSobj.currentText()]
        self.ui.edit_amp.insert(str(top.amp))
        unit = top.ampUnit
        if unit =='DM':
            unit = 'dBm'
        index = self.ui.combo_unit.findText(unit)
        if index != -1:
            self.ui.combo_unit.setCurrentIndex(-1)
            
        self.ui.button_confirm.setEnabled(False)
        
        #signals and slots
        self.ui.edit_amp.editingFinished.connect(self.check_confirm)
        self.ui.button_confirm.clicked.connect(self.confirm)
        
    def check_confirm(self):
        #checks that the input is valid and allows the user to click confirm
        ampText = str(self.ui.edit_amp.text())
        try:
            amp = float(ampText)
        except:
            self.ui.button_confirm.setEnabled(False)
        else:
            self.ui.button_confirm.setEnabled(True)
            
    def confirm(self):
        ampText = str(self.ui.edit_amp.text())
        amp = float(ampText)
        unit = str(self.ui.combo_unit.currentText())
        if unit == 'dBm':
            unit = 'DM' # change it so that it works properly with the INST
        msObj = self.microwaveSetters[str(self.ui.combo_MSobj.currentText())]
        msObj.setMSAmp( amp = amp, ampUnit = unit)
        #self.close() #not sure if I want to close here. 