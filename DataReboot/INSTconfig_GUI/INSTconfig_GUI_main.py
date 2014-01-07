'''
7/1/2013
Sean McLaughlin
Companion module to the INSTconfig_GUI module. It is now name-based, but I don't know if it should be GPIB-address based. 
'''

if __name__ == '__main__':
    print '''This is the hub for the configuration of the INSTconfig file. This window solely shows a view of the objects currently in the file. There are 3 buttons which open the
    corresponding windows in this directory for the purposes of adding, editing and deleting. This module is accesses from either the MainWindow_main module or the 
    MeasurementGUI_main module. This file, like the GASconfig, sends a signal to the mainwindow when an update is made. For the same reason, 
    changes cannot be updated to the measurement windows when a measurement is running. 
    '''

import sys
from PyQt4 import QtGui, QtCore
from INSTconfig_GUI import Ui_window_INST #extestgui contains pre-generated code from QtDesigner
import INSTconfig

class Start(QtGui.QMainWindow):
    
    def __init__(self,filename = None, parent = None):
        super(Start, self).__init__()
        self.ui = Ui_window_INST()
        self.ui.setupUi(self) #setupUi takes 2 arguments, both are self.

        
        #below are the instance variables for this window.
        self.configFilename = str(filename)
        self.parent = parent
        from os.path import isfile
        if isfile(self.configFilename):
            self.ui.edit_INSTconfig.clear()
            self.ui.edit_INSTconfig.insert(self.configFilename)
            self.start()
        
        self.windows = [] #an array containing all the child window references for this window; allows them to be checked together easily.
        
        #Below are setup for the signals and slots
        self.ui.combo_INST.currentIndexChanged.connect(self.display_current)
        self.ui.edit_INSTconfig.textChanged.connect(self.check_buttons)
        self.ui.button_add.clicked.connect(self.open_add)
        self.ui.button_del.clicked.connect(self.open_del)
        self.ui.button_INSTconfig.clicked.connect(self.file_dialog)
        self.ui.button_edit.clicked.connect(self.open_edit)
        
    def closeEvent(self, event):
        #overwrites the close event so thata signal is sent back to the main window when editing is done. 
        if self.parent is None:
            event.accept()
        elif self.parent.any_running(): #if there is a measurement running we don't want to update the other objects. 
            message = '''The config window cannot be closed while a measurement is running.
            You may choose to
            1) Close anyway and not update the current windows with the changes made. The changes are saved to file.
            2) Cancel, and wait until the measurement is finished to close.'''
            response = QtGui.QMessageBox.warning(self, 'Warning!', message
                            , QtGui.QMessageBox.Close | QtGui.QMessageBox.Cancel, defaultButton=QtGui.QMessageBox.Cancel)
            if response == QtGui.QMessageBox.Close:
                event.accept()
            else:
                event.ignore()
        else:
            self.parent.update_GAS_INST()
            event.accept()
        
    def file_dialog(self):
        #opens a file dialog and also calls start, which initializes the whole window. 
        fd = QtGui.QFileDialog(self)
        fname = fd.getOpenFileName()
        from os.path import isfile
        if isfile(fname):
            self.configFilename = fname
            self.ui.edit_INSTconfig.clear()
            self.ui.edit_INSTconfig.insert(fname)
            self.start()
            
    def start(self):
        #simply intializes the window with the info from the file. 
        self.check_buttons()
        names = INSTconfig.getINSTnames(self.configFilename)
        self.ui.combo_INST.clear()
        self.ui.combo_INST.addItems(names)
        self.display_current()
        
    def display_current(self):
        #displays the selected name's attributes.
        name = str(self.ui.combo_INST.currentText())
        if not name:
            return
        resAd = INSTconfig.getResAds(self.configFilename)[name]
        self.ui.text_display.clear()
        self.ui.text_display.insertPlainText(INSTconfig.displayINST(self.configFilename, resAd))
        
    def check_buttons(self):
        #if the name in the filename line is valid turn on the buttons. 
        from os.path import isfile
        if not isfile(self.ui.edit_INSTconfig.text()): #it is possible to assign the isfile check to a boolean and put that into the setEnabled() function. It saves space but is less clear
            self.ui.button_add.setEnabled(False)
            self.ui.button_del.setEnabled(False)
            self.ui.button_edit.setEnabled(False)
            self.ui.combo_INST.setEnabled(False)
            self.ui.text_display.setEnabled(False)
        else:
            self.ui.button_add.setEnabled(True)
            self.ui.button_del.setEnabled(True)
            self.ui.button_edit.setEnabled(True)
            self.ui.combo_INST.setEnabled(True)
            self.ui.text_display.setEnabled(True)

            
    def open_add(self):
        #this is the proper way to open a new window. keep that in mind for the future.
        if not self.OpenWindow():
            import INSTconfig_window_add_main
            from pyvisa import visa_exceptions
            try: #window_add_main has to connect to the instruments in order to work. If the wrong ones are connected, it will raise an error.
                self.window_add = INSTconfig_window_add_main.Start(self.configFilename)
            except visa_exceptions.VisaIOError: #this error will cause the window to not open 
                self.statusBar().showMessage('The instruments specified in the config file are not connected. Add will not open.')
                from time import sleep
                sleep(1)
                self.statusBar().showMessage('') #this is to make sure that the message goes away after a short period. 
                return
            else:
                self.windows.append(self.window_add)
                self.window_add.add_signal.connect(self.start)
                self.window_add.show()
                
    def open_del(self):
        #opens the del window object and maintains it's connection to this window
        if not self.OpenWindow():
            import INSTconfig_window_del_main
            currentINST = str(self.ui.combo_INST.currentText())
            self.window_del = INSTconfig_window_del_main.Start(self.configFilename, currentINST)
            self.windows.append(self.window_del)
            self.window_del.del_signal.connect(self.start)
            self.window_del.show()
            
    def open_edit(self):
        #similar to the open_add fucntion. Opens the edit window and maintinas its connections
        if not self.OpenWindow() :
            import INSTconfig_window_edit_main
            currentINST = str(self.ui.combo_INST.currentText())
            from pyvisa import visa_exceptions
            try:
                self.window_edit = INSTconfig_window_edit_main.Start(self.configFilename, currentINST)
            except visa_exceptions.VisaIOError: #this error will cause the window to not open 
                self.statusBar().showMessage('The instruments specified in the config file are not connected. Edit will not open.')
                from time import sleep
                sleep(1)
                self.statusBar().showMessage('')
                return
            else:
                self.windows.append(self.window_edit)
                self.window_edit.edit_signal.connect(self.start) #when and edit window is updated we update to reflect the changes. 
                self.window_edit.show()
                
    def OpenWindow(self): #returns true if any of the child windows are open
        return any(window.isVisible() for window in self.windows)
            
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Start()
    ex.show()
    sys.exit(app.exec_())
    
if __name__== '__main__':
    main()