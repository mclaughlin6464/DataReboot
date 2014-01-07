'''
7/19/2013
Sean McLaughlin
Companion file to the auto-generated calibrateBfield.py. Opens a dialog which allows the user to select a getter and setter to create a B-field 
calibration, then writes that change to file in the setter. Requires that the GAS config file already have been opened in MeasurementGUI_main.py
'''

if __name__ == '__main__':
    print ''' This small widget calibrates the bfield. The user specifies a getBField object and a setBField object to use. The file sets the voltage 4 times, from 0 to 2V,
    and reads the field. It then takes the average slope between points and assigns the calibration to the setField object and writes the change to file. 
    '''

import sys
from PyQt4 import QtGui, QtCore
from calibrateBfield import Ui_widget_calibrateBField
import GASconfig
import getAndSet


voltages = [.4, .8, 1.2, 1.6, 2] # voltages to step over.

class Start(QtGui.QWidget):
    
    class calibrateBFieldError(Exception):  # an error for this widget to return if there is a problem . 
        
        def __init__(self, value = None):
            self.value = value
            
        def __str__(self):
            if self.value != None:
                return str(self.value)
            return 'There was a problem calibrating the B-Field.'
    
    def __init__(self, filename, setters, getters,parent = None):
        #the initialization includes a dict of getters and one of setters. 
        super(Start, self).__init__(parent)
        self.ui = Ui_widget_calibrateBField()
        self.ui.setupUi(self)
        
        self.configFilename = filename
        
        self.getters = getters
        self.setters = setters
            
        if not (self.setters or self.getters): # if one of them is empty, raise an error. We need a getter and a setter to configure

            self.close()
            if self.setters:
                value = 'getters'
            else:
                value = 'setters'
            
            raise self.calibrateBFieldError, 'There are no %s configured.' %value
        
        self.ui.combo_getBField.addItems(self.getters.keys())
        self.ui.combo_setBField.addItems(self.setters.keys())
        
        self.ui.button_confirm.setEnabled(False)#will turn it on when the text field has a valid value in it
        self.display_current()
        
        #setup the signals and slots
        self.ui.button_calibrate.clicked.connect(self.calibrate)
        self.ui.button_confirm.clicked.connect(self.confirm)
        self.ui.edit_calibration.textChanged.connect(self.check_confirm)
        self.ui.combo_setBField.currentIndexChanged.connect(self.display_current)
        
    def calibrate(self):
        from time import sleep
        getterName = str(self.ui.combo_getBField.currentText())
        setterName = str(self.ui.combo_setBField.currentText())
        
        getter = self.getters[getterName]
        setter = self.setters[setterName]
        
        self.ui.edit_calibration.clear() #this doens't seem to work...
        self.ui.edit_calibration.insert('Calibrating...')
        
        fields = []
        
        #this seems to lock up the GUI while this is happening. If this is a problem it would need to be run in another thread. 
        for v in voltages:
            setter.setVoltage(v)
            sleep(1) #give the field a bit of time to catch up. 
            fields.append(getter.get())
            
        setter.off()
            
        slopes = []
        #could be changed to not use indicies, and instead use a most recent holder. probably unecessary. 
        for i in xrange(len(voltages)-1): #calculate a the slopes between each step
            rise = (fields[i+1]-fields[i])
            run = (voltages[i+1] - voltages[i])
            slopes.append(rise/run)
        
        calibrationFactor = sum(slopes)/len(slopes) #average the slopes. 
        
        self.ui.edit_calibration.clear()
        self.ui.edit_calibration.insert(str(calibrationFactor))
        
    def check_confirm(self): #check to turn on the confirm button
        cal = str(self.ui.edit_calibration.text())
        try:
            float(cal)
            if cal == 0: #this will cause a problem is this gets through. 
                raise ValueError
        except ValueError:
            self.ui.button_confirm.setEnabled(False)
        else:
            self.ui.button_confirm.setEnabled(True)
            
    def confirm(self):
        #assign the new calibration to the set BField object and write the change to file.
        calibrationFactor = float(self.ui.edit_calibration.text())
        setterName = str(self.ui.combo_setBField.currentText())
        setter = self.setters[setterName]
        setter.calibrationFactor = calibrationFactor #assign the new calibration factor to the object; this will carry back to the measurement window. 
        setterAttr = GASconfig.getGASattributes(self.configFilename, setterName)
        junk, INSTfilename = GASconfig.readConfig(self.configFilename)
        del(junk)
        setterAttr[getAndSet.cal] = calibrationFactor
        GASconfig.editGAS(self.configFilename, INSTfilename, setterName, setter.className, setter.InstrumentType, **setterAttr) #also write the change to file. 
        self.close()
        
    def display_current(self):
        #show the calibration set for the current one . 
        self.ui.edit_calibration.clear()
        currentSet = self.setters[str(self.ui.combo_setBField.currentText())]
        
        self.ui.edit_calibration.insert(str(currentSet.calibrationFactor))
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Start('C:\MeasurementConfig\GASconfig.txt')
    ex.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()