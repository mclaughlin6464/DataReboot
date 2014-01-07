'''
7/1/2013
Sean McLaughlin
Companion module to INSTconfig_window_del
'''

import sys
from PyQt4 import QtGui, QtCore
from INSTconfig_window_del import Ui_window_del #extestgui contains pre-generated code from QtDesigner
import INSTconfig

if __name__ == '__main__':
    print ''' A small dialog that allows the user to delete an instrument from the file. The changes are changed to the file and a signal is sent to the parent window to update itself.
    '''

class Start(QtGui.QWidget):
    
    del_signal = QtCore.pyqtSignal() #not sure why this is the case but this needs to be declared outside of the constructor. 
    
    def __init__(self, filename, startINST, parent = None):
        
        super(Start, self).__init__(parent)
        self.ui = Ui_window_del()
        self.ui.setupUi(self)
        
        #instance variables and initialization
        self.filename = filename
        self.fill_combo()
        
        if startINST:# if we have an instrument to begin with, show it. 
            index = self.ui.combo_name.findText(startINST)
            self.ui.combo_name.setCurrentIndex(index)
            
        self.display_current()
        
        #signals and slots
        self.ui.combo_name.currentIndexChanged.connect(self.display_current)
        self.ui.button_del.clicked.connect(self.delete_INST)
        
    def display_current(self): 
        #shows the current selected object. 
        topName = str(self.ui.combo_name.currentText())
        if not topName:
            return
        addDict = INSTconfig.getResAds(self.filename)
        self.ui.text_display.clear()
        self.ui.text_display.insertPlainText(INSTconfig.displayINST(self.filename, addDict[topName]))
        
    def delete_INST(self):
        #deletes the selected object from the file and updates the main window as well. 
        name = str(self.ui.combo_name.currentText())
        inDict = INSTconfig.getResAds(self.filename)
        INSTconfig.delINST(self.filename, inDict[name])
        self.fill_combo()
        self.del_signal.emit()
        
    def fill_combo(self):
        #fills the combo box with the names of the objects from the file. 
        names = INSTconfig.getINSTnames(self.filename)
        self.ui.combo_name.clear()
        self.ui.combo_name.addItems(names)
        self.display_current()
        
def main(filename):
    app = QtGui.QApplication(sys.argv)
    ex = Start(filename)
    ex.show()
    app.exec_()
    
if __name__== '__main__':
    fname = 'C:\MeasurementConfig\config.txt'
    main(fname)