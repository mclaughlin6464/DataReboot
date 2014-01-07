'''
6/18/2013
created by Sean McLaughlin

This module contains the code to start the GUI for ExTest_3.py
'''

import sys
from PyQt4 import QtGui, QtCore
from extestgui import Ui_ExTestGUI #extestgui contains pre-generated code from QtDesigner
import ExTest_3_Gui
import thread

class Start(QtGui.QMainWindow):
    
    def __init__(self, parent = None):
        super(Start, self).__init__()
        self.ui = Ui_ExTestGUI()
        self.ui.setupUi(self) #setupUi takes 2 arguements, both of which are self. 
        self.filenames = ['',''] #the filenames for the config and data file respectively
        self.abort = False
        self.data = [[],[],[],[]] #this will be how I will pass data from the measurement thread back to the GUI thread
        self.timer = QtCore.QTimer() #a timer for live plotting.
        #set defaults for some of the fields.
        self.ui.edit_maxF.insert('0')
        self.ui.edit_minF.insert('0')
        self.ui.edit_dataPoints.insert('100')
        
        #Below is the setup from signals to slots
        self.ui.button_config.clicked.connect(self.file_dialog_config)
        self.ui.button_data.clicked.connect(self.file_dialog_data)
        self.ui.button_go.clicked.connect(self.run_measurement)
        self.ui.button_abort.clicked.connect(self.set_abort)
        self.ui.edit_config.textChanged.connect(self.activate_go)
        self.ui.edit_data.textChanged.connect(self.activate_go)
        
    def file_dialog(self, n):
        #this function takes an integer. 0 coincides with the config file and 1 coincides with the data file. This will determine where the result is written to. 
        #the file I/O takes place here, and then the other modules do the specific writing. 
        fd = QtGui.QFileDialog(self)
        fname = fd.getOpenFileName()
        from os.path import isfile
        if isfile(fname):
            self.filenames[n] = fname
        
    def file_dialog_config(self):
        #the code for this function and file_dialog_data will be nearly identical. Only difference is what button was pressed and where the result is written. 
        self.file_dialog(0)
        self.ui.edit_config.insert(self.filenames[0])
        
    def file_dialog_data(self):
        self.file_dialog(1)
        self.ui.edit_data.insert(self.filenames[1])
        
    def run_measurement(self):
        #this module runs when go is pressed. 
        
        #first, get all the data we need to start the measurement
        configFilename = self.ui.edit_config.text()
        dataFilename = self.ui.edit_data.text()
        lockinForV = self.ui.comboBox.currentIndex()==0
        maxF = float(self.ui.edit_maxF.text())
        minF = float(self.ui.edit_minF.text())
        dataPoints = int(self.ui.edit_dataPoints.text())
        arguments = (self, configFilename, dataFilename, lockinForV, maxF, minF, dataPoints)
        
        
        self.ui.button_abort.setEnabled(True) #we can abort now that the measurement's begun. 
        self.statusBar().showMessage('Measuring...')#update the status bar
        thread.start_new_thread(ExTest_3_Gui.main, arguments)
        self.run_plot()
            
    def run_plot(self):
        #this module plots the data from the measurement. It calls self.update repeatedly to 
        self.curve = self.ui.plot_widget.plot(pen = 'g')
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        
    def update(self):
        #this module is called repeatedly to update the plot
        if self.data[1]: #if not empty
            self.curve.setData(self.data[1])
            
    def set_abort(self):
        self.abort = True
        
    def activate_go(self):
        if self.ui.edit_config.text() and self.ui.edit_data.text(): #if both text boxes are non-empty turn on go. 
            self.ui.button_go.setEnabled(True)
            
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Start()
    ex.show()
    sys.exit(app.exec_())
    
if __name__ =='__main__':
    main()
    