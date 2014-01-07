'''
7/1/2013
Sean McLaughlin
COmpanion module to INStconfig_window_add
'''

import sys
from PyQt4 import QtGui, QtCore
from INSTconfig_window_add import Ui_Form
import INSTconfig
import Instruments

if __name__ == '__main__':
    print '''This small dialog allows the user to add an instrument. The user simply selects a type and types in a resource address and the gui attempts to connect. When Add is clickec,
    the window closes itself, and the change is written to file. 
    '''

class Start(QtGui.QWidget):
    
    add_signal = QtCore.pyqtSignal()
    
    def __init__(self,filename,  parent = None):
        super(Start, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        #instance variables and initialize the UI
        self.filename = filename
        self.inDict = Instruments.instrumentDictionary
        self.ui.combo_name.addItems(self.inDict.keys())#add all the possible, addable isntruments
        
        self.valid = False # an easy way to see if our instrument is valid
        self.ui.text_display.setEnabled(True)
        self.ui.button_add.setEnabled(False)
        
        #signals and slots
        self.ui.edit_resAd.editingFinished.connect(self.update_display)
        self.ui.button_add.clicked.connect(self.add_INST)
        self.ui.combo_name.currentIndexChanged.connect(self.update_display)
        
        
    def update_display(self):
        #update the central display with the information that has been enterered. 
        currentResAd = str(self.ui.edit_resAd.text())
        currentINST = str(self.ui.combo_name.currentText())
        self.ui.text_display.clear()
        if currentResAd:
            from pyvisa import visa_exceptions
            try: #try to connect to the instrument
                ref = self.inDict[currentINST](currentResAd)
            except visa_exceptions.VisaIOError: #actually doesn't check to see if the instrument is the correct type; I don't know how to go about that. 
                self.ui.text_display.insertPlainText('Not a valid address or instrument.')
                self.valid = False
            else: #instrument was valid; display it's info. 
                self.ui.text_display.insertPlainText(str(ref))
                self.valid = True
        self.check_add()
        
    def check_add(self):
        #this method sets the add button on or off depending on the validity of the addition of the instrument. 
        self.ui.button_add.setEnabled(self.valid) 
        
    def add_INST(self):
        #adds the instrument to the file. 
        ttype = str(self.ui.combo_name.currentText())
        resAd = str(self.ui.edit_resAd.text())
        INSTconfig.addINST(self.filename, resAd, ttype)
        self.add_signal.emit()
        self.close()

def main(filename):
    app = QtGui.QApplication(sys.argv)
    ex = Start(filename)
    ex.show()
    sys.exit(app.exec_())
    
if __name__=='__main__':
    fname = 'C:/Python27/Scripts/MeasureProgram/trunk/config&data/config.txt'
    main(fname)