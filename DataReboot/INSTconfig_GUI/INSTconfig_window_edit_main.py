'''
7/1/2013
Sean McLaughlin
Companion module to INStconfig_window_edit
'''
#there's a typo in the GUI

import sys
from PyQt4 import QtGui, QtCore
from INSTconfig_window_edit import Ui_Form
import INSTconfig
import Instruments

if __name__ == '__main__':
    print '''This small dialog allows the user to edit an instrument. The user simply selects a type and types in a resource address and the gui attempts to connect. When Edit is clickec,
    the change is written to file and the signal is sent to the parent window to update itself. 
    '''

class Start(QtGui.QWidget):
    
    edit_signal = QtCore.pyqtSignal()
    
    def __init__(self,filename, startINST, parent = None):
        super(Start, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        #instance variables and initialize the UI
        self.filename = filename
        self.AddressDict = INSTconfig.getResAds(self.filename)
        #we need 2 dictionaries. One with the connected instruments and their addresses ^^^ and one for the possible instruments and their callables vvv
        self.inDict = Instruments.instrumentDictionary
        self.ui.combo_name.addItems(self.AddressDict.keys())
        
        if startINST: #if there's an instrument to start with, show it. 
            index = self.ui.combo_name.findText(startINST)
            self.ui.combo_name.setCurrentIndex(index)
        
        self.valid = False # an easy way to see if our instrument is valid
        self.ui.text_display.setEnabled(True)
        self.ui.button_add.setEnabled(False)
        self.update_address()
        
        #signals and slots
        self.ui.edit_resAd.editingFinished.connect(self.update_display)
        self.ui.button_add.clicked.connect(self.edit_INST)
        self.ui.combo_name.currentIndexChanged.connect(self.update_address)
        
        
    def update_address(self):
        #update the address field with the instrument's current address
        currentINST = str(self.ui.combo_name.currentText())
        self.ui.edit_resAd.clear()
        self.ui.edit_resAd.insert(self.AddressDict[currentINST])
        self.update_display()
        
    def update_display(self):
        #update the central display with the information that has been enterered. 
        currentResAd = str(self.ui.edit_resAd.text())
        currentINST = str(self.ui.combo_name.currentText())
        self.ui.text_display.clear()
        if currentResAd :
            from pyvisa import visa_exceptions
            try:
                ref = self.inDict[currentINST](currentResAd)
            except visa_exceptions.VisaIOError: #actually doesn't check to see if the instrument is the correct type; I don't know how to go about that. 
                self.ui.text_display.insertPlainText('Not a valid address or instrument.')
                self.valid = False
            else:
                self.ui.text_display.insertPlainText(str(ref))
                self.valid = True
        self.check_done()
        
    def check_done(self):
        #this method sets the done button on or off depending on the validity of the addition of the instrument. 
        self.ui.button_add.setEnabled(self.valid) 
        
    def edit_INST(self):
        #write our new edit to file using the INSTconfig module
        INSTname = str(self.ui.combo_name.currentText())
        resAd = str(self.ui.edit_resAd.text())#.............vvv old address
        INSTconfig.editINST(self.filename, resAd, self.AddressDict[INSTname])
        self.edit_signal.emit()

def main(filename):
    app = QtGui.QApplication(sys.argv)
    ex = Start(filename)
    ex.show()
    sys.exit(app.exec_())
    
if __name__=='__main__':
    fname = 'C:\MeasurementConfig\config.txt'
    main(fname)