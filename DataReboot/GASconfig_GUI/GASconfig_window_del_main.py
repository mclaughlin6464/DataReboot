'''
6/28/2013
Sean McLaughlin
Companion module to window_del_main. Opens and runs the delete window for the configuration of the GAS file.
'''

if __name__ == '__main__':
    print ''' This module is a small dialog that allows the user to delete a GAS object in the file. When Del is clicked, it takes the relevant information from the GUI and 
    calls GASconfig's delGAS method, which writes the change to the file.
    '''

import sys
from PyQt4 import QtGui, QtCore
from GASconfig_window_del import Ui_window_del #extestgui contains pre-generated code from QtDesigner
import GASconfig
import getAndSet

class Start(QtGui.QWidget):
    
    del_signal = QtCore.pyqtSignal() #not sure why this is the case but this needs to be declared outside of the constructor. 
    
    def __init__(self, filename, startGAS = None, parent = None):
        super(Start, self).__init__(parent)
        self.ui = Ui_window_del()
        self.ui.setupUi(self)
        
        #instance variables and initialization
        self.filename = filename
        self.fill_combo()
        
        if startGAS: #if we have an instrument to start from. 
            index = self.ui.combo_name.findText(startGAS)
            self.ui.combo_name.setCurrentIndex(index)
        
        self.display_current()
        
        #signals and slots
        self.ui.combo_name.currentIndexChanged.connect(self.display_current)
        self.ui.button_del.clicked.connect(self.delete_GAS)
        
    def display_current(self): 
        #shows the current selected object. 
        topName = str(self.ui.combo_name.currentText())
        self.ui.text_display.clear()
        self.ui.text_display.insertPlainText(GASconfig.displayGAS(self.filename, topName))
        
    def delete_GAS(self):
        #deletes the selected object from the file and updates the main window as well. 
        name = str(self.ui.combo_name.currentText())
        GASconfig.delGas(self.filename, name)
        self.fill_combo()
        self.del_signal.emit()
        
    def fill_combo(self):
        #fills the combo box with the names of the objects from the file. 
        names = GASconfig.getGASNames(self.filename)
        self.ui.combo_name.clear()
        self.ui.combo_name.addItems(names)
        self.display_current()
        
def main(filename):
    app = QtGui.QApplication(sys.argv)
    ex = Start(filename)
    ex.show()
    app.exec_()
    
if __name__== '__main__':
    fname = 'C:\MeasurementConfig\GASconfig.txt'
    main(fname)