'''
6/27/2013
Sean McLaughlin
this is the companion module to GASconfig_GUI. It imports the generated code from that module, makes some modifications, and runs it. It also calls 3 other windows, depending on
which buttons are pressed. 
'''

if __name__ == '__main__':
    print''' This is the hub for the configuration of the GASconfig file. This window solely shows a view of the objects currently in the file. There are 3 buttons which open the
    corresponding windows in this directory for the purposes of adding, editing and deleting. This module is accesses from either the MainWindow_main module or the 
    MeasurementGUI_main module. When this module is closed, it sends a signal back to it's parent window to apply the changes made. If a measurement is currently running,
    the window will pop up a dialog warning the user that their changes may not be applied if they close now. 
    '''

import sys
from PyQt4 import QtGui, QtCore
from GASconfig_GUI import Ui_window_GAS #extestgui contains pre-generated code from QtDesigner
import GASconfig

class Start(QtGui.QMainWindow):
    
    def __init__(self,filename = None, parent = None):
        super(Start, self).__init__(parent)
        self.ui = Ui_window_GAS()
        self.ui.setupUi(self)
        
        #below are the instance variables for this window.
        self.configFilename = str(filename)
        self.parent = parent
        
        from os.path import isfile
        if isfile(self.configFilename):
            self.ui.edit_filename.clear()
            self.ui.edit_filename.insert(self.configFilename)
            self.start()
            
        self.windows = [] #an array containing all the child window references for this window; allows them to be checked together easily.
        
        #Below are setup for the signals and slots
        self.ui.button_open.clicked.connect(self.file_dialog)
        self.ui.combo_GAS.currentIndexChanged.connect(self.display_current)
        self.ui.edit_filename.textChanged.connect(self.check_buttons)
        self.ui.button_add.clicked.connect(self.open_add)
        self.ui.button_del.clicked.connect(self.open_del)
        self.ui.button_INSTconfig.clicked.connect(self.INST_file_dialog)
        self.ui.button_edit.clicked.connect(self.open_edit)
        
    def closeEvent(self, event):
        #overwrites the close event so that a signal is sent back to the main window when editing is done. 
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
        #this is more likely than not obsolete, because there is only one config per machine, which is saved in the master config file that is in the repository with the program. 
        fd = QtGui.QFileDialog(self)
        fname = fd.getOpenFileName()
        from os.path import isfile
        if isfile(fname):
            self.configFilename = fname
            self.ui.edit_filename.clear()
            self.ui.edit_filename.insert(fname)
            self.start()
            
    def start(self):
        #simply intializes the window with the info from the file. 
        self.check_buttons()
        names = GASconfig.getGASNames(self.configFilename)
        self.ui.combo_GAS.clear()
        self.ui.combo_GAS.addItems(names)
        junk, filename = GASconfig.readConfig(self.configFilename) #readconfig returns both the INSTfilename and the lines in the file. We only need the filename here
        del(junk)
        self.ui.edit_INSTconfig.clear()
        self.ui.edit_INSTconfig.insert(filename)
        self.display_current()
        
    def display_current(self):
        #displays the selected name's attributes.
        name = self.ui.combo_GAS.currentText()
        self.ui.text_display.clear()
        self.ui.text_display.insertPlainText(GASconfig.displayGAS(self.configFilename, name))
        
    def check_buttons(self):
        #if the name in the filename line is valid turn on the buttons. 
        
        #It would be very possible to assign the result of isFile() to a boolean, and pass that boolean into the setEnabled function, halving the size of this method
        #it could make things a little less clear though
        from os.path import isfile
        if not isfile(self.ui.edit_filename.text()):
            self.ui.button_add.setEnabled(False)
            self.ui.button_del.setEnabled(False)
            self.ui.button_edit.setEnabled(False)
            self.ui.combo_GAS.setEnabled(False)
            self.ui.text_display.setEnabled(False)
            self.ui.edit_INSTconfig.setEnabled(False)
            self.ui.button_INSTconfig.setEnabled(False)
        else:
            self.ui.button_add.setEnabled(True)
            self.ui.button_del.setEnabled(True)
            self.ui.button_edit.setEnabled(True)
            self.ui.combo_GAS.setEnabled(True)
            self.ui.text_display.setEnabled(True)
            self.ui.edit_INSTconfig.setEnabled(True)
            self.ui.button_INSTconfig.setEnabled(True)
            
    def open_add(self):
        #this is the proper way to open a new window.
            import GASconfig_window_add_main
            from pyvisa import visa_exceptions
            try: #window_add_main has to connect to the instruments in order to work. If the wrong ones are connected, it will raise an error.
                self.window_add = GASconfig_window_add_main.Start(self.configFilename)
            except visa_exceptions.VisaIOError: #this error will cause the window to not open 
                self.statusBar().showMessage('The instruments specified in the config file are not connected. Add will not open.')
                from time import sleep
                sleep(1)
                self.statusBar().showMessage('')
                return
            except IOError: # The inst file isn't valid
                self.statusBar().showMessage('That Instrument Config File does not exist.')
                from time import sleep
                sleep(1)
                self.statusBar().showMessage('')
                return
            else: #all good; show the window. 
                self.windows.append(self.window_add)
                self.window_add.add_signal.connect(self.start)
                self.window_add.show()
                
    def open_del(self):
        #opens the del window object and maintains it's connection to this window
        if self.OpenWindow() == False:
            import GASconfig_window_del_main
            currentGAS = str(self.ui.combo_GAS.currentText())
            self.window_del = GASconfig_window_del_main.Start(self.configFilename,currentGAS)
            self.windows.append(self.window_del)
            self.window_del.del_signal.connect(self.start)
            self.window_del.show()
            
    def open_edit(self):
        #similar to the open_add fucntion. Opens the edit window and maintinas its connections
        if self.OpenWindow() == False:
            import GASconfig_window_edit_main
            currentGAS = str(self.ui.combo_GAS.currentText())
            from pyvisa import visa_exceptions
            try:
                self.window_edit = GASconfig_window_edit_main.Start(self.configFilename,currentGAS)
            except visa_exceptions.VisaIOError: #this error will cause the window to not open 
                self.statusBar().showMessage('The instruments specified in the config file are not connected. Edit will not open.')
                from time import sleep
                sleep(1)
                self.statusBar().showMessage('')
                return
            except IOError: # The inst file isn't valid
                self.statusBar().showMessage('That Instrument Config File does not exist.')
                from time import sleep
                sleep(1)
                self.statusBar().showMessage('')
                return
            else:
                self.windows.append(self.window_edit)
                self.window_edit.edit_signal.connect(self.start)
                self.window_edit.show()
                
    def OpenWindow(self):#returns true is any of the child windows are open. 
        return any(window.isVisible() for window in self.windows)
        
    def INST_file_dialog(self):
        #similar to the other file dialog, but this gets the config filename and also writes it to the file. 
        #also like the other dialog, probably obsolete in the current form of the code, but I see no good reason to delete it. 
        fd = QtGui.QFileDialog(self)
        fname = fd.getOpenFileName()
        from os.path import isfile
        if isfile(fname):
            self.ui.edit_INSTconfig.clear()
            self.ui.edit_INSTconfig.insert(fname)
            self.start()
            GASconfig.changeInstrumentConfigFilename(self.configFilename, fname)
            
def main(): #like all the GUI files in this program, they can be run on their own, separate from the main program. 
    app = QtGui.QApplication(sys.argv)
    ex = Start()
    ex.show()
    sys.exit(app.exec_())
    
if __name__== '__main__':
    main()