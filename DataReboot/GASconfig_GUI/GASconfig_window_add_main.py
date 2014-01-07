'''
6/27/2013
Sean Mclaughlin
This is the companion module to the auto-generated GASconfig_window_add module. It is called by the GASconfig_GUI_main module.
'''

if __name__ == '__main__':
    print ''' This module is a small dialog that allows the user to add a GAS object to the file. When Add is clicked, it takes the relevant information from the GUI and 
    calls GASconfig's addGAS method, which writes the change to the file. The window then closes itself, and emits a signal to the upper window to update itself with the changes. 
    '''

import sys
from PyQt4 import QtGui, QtCore
from GASconfig_window_add import Ui_window_add #extestgui contains pre-generated code from QtDesigner
import GASconfig
import getAndSet

class Start(QtGui.QWidget):
    
    add_signal = QtCore.pyqtSignal()
    
    def __init__(self,filename, parent = None):
        super(Start, self).__init__(parent)
        self.ui = Ui_window_add()
        self.ui.setupUi(self)

        #below are the instance variables for this widget
        #we also initialize the selection options
        self.GASfilename = filename
        
        junk,self.INSTfilename = GASconfig.readConfig(self.GASfilename) #get the Instrument config filename
        del(junk) #all the lines in the file; we don't need this. 
        
        self.GASFromFile, self.INSTdict = GASconfig.getsAndSetsFromConfig(self.GASfilename)#using that info get a dictionary of instruments and their names
        self.INSTlist = sorted(self.INSTdict.keys())
        
        self.GASlist = sorted(getAndSet.GASdictionary.keys()) #get a list of all GAS objects
        for name in self.GASlist:
            if name != 'getAndSet': #we don't want to show this one
                self.ui.combo_classType.addItem(name) #fill the combo box
        
        self.update_instruments()#now that the class dropdown is filled, we need to populate the others. 
        
        for key, value in self.GASFromFile.iteritems(): #for the getResistance method we need to use an existing getVoltage and getCurrent object
            if value.className == 'getVoltage':
                self.ui.combo_Voltage.addItem(key)
            elif value.className == 'getCurrent':
                self.ui.combo_current.addItem(key)
        
        #below are the signals and slots
        self.ui.combo_classType.currentIndexChanged.connect(self.update_instruments)
        self.ui.combo_classType.currentIndexChanged.connect(self.check_delay_2)
        self.ui.combo_classType.currentIndexChanged.connect(self.check_amplitude)
        self.ui.combo_instrumentType.currentIndexChanged.connect(self.update_addresses)
        self.ui.combo_instrumentType.currentIndexChanged.connect(self.update_measurementType)
        self.ui.combo_instrumentType.currentIndexChanged.connect(self.update_delay)
        self.ui.combo_measurementType.currentIndexChanged.connect(self.update_ports)
        self.ui.edit_name.textChanged.connect(self.toggle_add)
        self.ui.button_add.clicked.connect(self.add_obj)
        
    def add_obj(self):
        #adds a new object using GASconfig's addGas method, then closes the window.
        #pull everything from the options. If any of them are invalid or not useful, it will be screened out.
        name = str(self.ui.edit_name.text())
        classType = str(self.ui.combo_classType.currentText())
        InstrumentType = str(self.ui.combo_instrumentType.currentText())
        delay = str(self.ui.edit_delay.text())
        timeConstantMult = str(self.ui.combo_delay.currentText()) == 'Multiples of Time Constant' and self.ui.combo_delay.isEnabled()
        delay_2 = str(self.ui.edit_delay_2.text())
        timeConstantMult_2 = str(self.ui.combo_delay_2.currentText()) == 'Multiples of Time Constant' and self.ui.combo_delay_2.isEnabled()
        ttype = str(self.ui.combo_measurementType.currentText())
        port = int(self.ui.spin_port.cleanText())
        OCRtext = self.ui.edit_OCR.text()
        OCR = OCRtext
        currentText = str(self.ui.combo_current.currentText())
        voltText = str(self.ui.combo_Voltage.currentText())
        ampText = str(self.ui.edit_amplitude.text())
        ampUnit = str(self.ui.combo_amplitude.currentText())
        comment = str(self.ui.edit_comment.text())
        
        kwargs = {getAndSet.GASname: name}
        
        if ttype and (self.ui.combo_classType.isEnabled()): # if the box is off we don't want to use the text! Likewise if there is no text. 
            kwargs[getAndSet.measType] = ttype
        
        if port and ( self.ui.spin_port.isEnabled()):
            kwargs[getAndSet.port] = port
        
        if  OCR and ( self.ui.edit_OCR.isEnabled()):
            kwargs[getAndSet.OCR] =  float(OCR)
        
        if  delay:
            kwargs[getAndSet.delay] = delay
            kwargs[getAndSet.TCM]= timeConstantMult
        
        if  delay_2 and (self.ui.edit_delay_2.isEnabled()):
            kwargs[getAndSet.delay2]= delay_2
            kwargs[getAndSet.TCM2]= timeConstantMult_2
        
        if currentText and self.ui.combo_current.isEnabled():
            currentSource = self.GASFromFile[currentText]
            kwargs[getAndSet.gC]= currentSource
        
        if voltText and self.ui.combo_Voltage.isEnabled():
            voltSource = self.GASFromFile[voltText]
            kwargs[getAndSet.gV]= voltSource
        
        if ampText and self.ui.edit_amplitude.isEnabled():
            kwargs[getAndSet.amp] = ampText + ' '+ ampUnit # amp includes the info with the unit and the value
            
        if comment:
            kwargs[getAndSet.comment] = comment
            
        GASconfig.addGas(self.GASfilename, self.INSTfilename, classType, InstrumentType, **kwargs)
            
        self.add_signal.emit()
        self.close()
    
    def check_amplitude(self): 
        #if the classtype is a microwave source, turn on the amplitude options. Else, disable them. 
        classType = str(self.ui.combo_classType.currentText())
        on = classType == 'setMicrowaveSource'
        self.ui.combo_amplitude.setEnabled(on)
        self.ui.edit_amplitude.setEnabled(on)
    
    def check_delay_2(self): 
        #if the classtype is a setBField, turn on the second delay. Else, disable it. 
        classType = str(self.ui.combo_classType.currentText())
        on =  classType == 'setBField' # the one type that allows a second delay
        self.ui.edit_delay_2.setEnabled(on)
        self.ui.combo_delay_2.setEnabled(on)
    
    def toggle_add(self): 
        #turns the Add button on and off depending on whether or not there is text in the name field. 
        text = str(self.ui.edit_name.text())
        if text:
            self.ui.button_add.setEnabled(True)
        else:
            self.ui.button_add.setEnabled(False)
                        
    def update_instruments(self):
        #puts the correct instruments in the combo box depending on which Class is in the ClassType box. Also updates the boxes below it. 
        self.ui.combo_instrumentType.clear()
        self.ui.combo_instrumentType.setEnabled(True)
        topName = self.ui.combo_classType.currentText()
        
        for name, instrument in self.INSTdict.iteritems():
            if topName in instrument.validGetsAndSets: #if the className is a valid possibility for this instrument
                self.ui.combo_instrumentType.addItem(name)
                
        #update all others
        self.update_addresses()
        self.update_measurementType()
        self.update_ports()
        self.update_OCR()
        self.update_delay()
        self.update_resistance()
        
    def update_addresses(self):
        #inserts the correct address for the instrument in place
        self.ui.edit_address.clear()
        topInst = str(self.ui.combo_instrumentType.currentText()) # this returns a QString; we need a string. 
        if topInst != '':
            self.ui.edit_address.insert(self.INSTdict[topInst].address)
        
    def update_delay(self):
        #if the instrument is the lock-in and it's a getter, we add the option to use multiples of the time constant
        currentINST = str(self.ui.combo_instrumentType.currentText())
        currentClassType = str(self.ui.combo_classType.currentText())
        if currentINST == 'Lock-in Amplifier'  and currentClassType[:3] == 'get': #the lockin has another option for it's delay. 
            if -1 == self.ui.combo_delay.findText('Multiples of Time Constant'):
                self.ui.combo_delay.addItem('Multiples of Time Constant')
            if -1 == self.ui.combo_delay_2.findText('Multiples of Time Constant'):
                self.ui.combo_delay_2.addItem('Multiples of Time Constant')
        else:
            i = self.ui.combo_delay.findText('Multiples of Time Constant')
            if i != -1:
                self.ui.combo_delay.removeItem(i)
                
            i = self.ui.combo_delay_2.findText('Multiples of Time Constant')
            if i != -1:
                self.ui.combo_delay_2.removeItem(i)
        
    def update_measurementType(self):
        #inserts all the possible measurement types for the current instrument
        self.ui.combo_measurementType.clear()
        topInst = str(self.ui.combo_instrumentType.currentText())
        topClass = str(self.ui.combo_classType.currentText())
        if topInst and topClass: #neither is empty
            validTypes = self.INSTdict[topInst].validMeasurementTypes[topClass]
            if validTypes: # if this instrument has measurement types for this class
                self.ui.combo_measurementType.setEnabled(True)
                self.ui.combo_measurementType.addItems(validTypes)
            else:
                self.ui.combo_measurementType.setEnabled(False)
            
    
    def update_OCR(self):
        #turns OCR on and off depending on if the current class is a current getter or setter
        topClass = str(self.ui.combo_classType.currentText())
        if topClass[1:] == 'etCurrent': #a current method, either s_etCurrent or g_etCurrent. May be better to replace this with some other, clearer check.
            self.ui.edit_OCR.setEnabled(True) #this needs a name change!
        else:
            self.ui.edit_OCR.setEnabled(False)

    def update_ports(self):
        #turns the ports spinbox on and off depdning on what measurement type is selected. 
        topType = str(self.ui.combo_measurementType.currentText())
        if topType== 'AuxOut' or topType== 'AuxIn':
            self.ui.spin_port.setEnabled(True)
        else:
            self.ui.spin_port.setEnabled(False)
            
    def update_resistance(self):
        currentType = str(self.ui.combo_classType.currentText())
        if currentType == 'getResistance':
            self.ui.combo_current.setEnabled(True)
            self.ui.combo_Voltage.setEnabled(True)
        else:
            self.ui.combo_current.setEnabled(False)
            self.ui.combo_Voltage.setEnabled(False)
                
def main(filename): #like all the GUI classes this one can be run on it's own. 
    app = QtGui.QApplication(sys.argv)
    ex = Start(filename)
    ex.show()
    app.exec_()
    
if __name__== '__main__':
    fname = 'C:\MeasurementConfig\GASconfig.txt'
    main(fname)