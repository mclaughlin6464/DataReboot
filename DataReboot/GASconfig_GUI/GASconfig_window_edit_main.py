'''
6/28/2013
Sean McLaughlin
Companion Module for the GASconfig_window_edit auto-generated module. Shows the window and controls the functions.
'''

import sys
from PyQt4 import QtGui, QtCore
from GASconfig_window_edit import Ui_Form #extestgui contains pre-generated code from QtDesigner
import GASconfig
import getAndSet

if __name__ == '__main__':
    print ''' This module is a small dialog that allows the user to edit a GAS object in the file. When Edit is clicked, it takes the relevant information from the GUI and 
    calls GASconfig's editGAS method, which deletes the existing object and writes the change to the file. The window then emits a signal to the upper window to update itself with the changes. 
    '''

class Start(QtGui.QWidget):
    
    edit_signal = QtCore.pyqtSignal()
    
    def __init__(self, filename,startGAS= None, parent = None):
        super(Start, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        #instance variables and initialzation
        self.GASfilename = filename
        
        junk,self.INSTfilename = GASconfig.readConfig(self.GASfilename) #get the Instrument config filename
        del(junk) #all the lines in the file; we don't need this. 
        
        self.GASFromFile, self.INSTdict = GASconfig.getsAndSetsFromConfig(self.GASfilename)#using that info get a dictionary of instruments and their names
        self.INSTlist = sorted(self.INSTdict.keys())
        
        self.GASlist =sorted( getAndSet.GASdictionary.keys() )#get a list of all GAS objects
        for name in self.GASlist:
            if name != 'getAndSet': #we don't want to show this one
                self.ui.combo_classType.addItem(name) #fill the combo box
        self.update_instruments()
        self.ui.button_done.setEnabled(True)
        self.fill_combo()
        
        for key, value in self.GASFromFile.iteritems(): #the getResistance object needs to use existing getVoltage and getCurrent objects. 
            if value.className == 'getVoltage':
                self.ui.combo_Voltage.addItem(key)
            elif value.className == 'getCurrent':
                self.ui.combo_current.addItem(key)
        
        if startGAS: # if we have one to start on we requite special initialization. 
            index = self.ui.combo_name.findText(startGAS)
            self.ui.combo_name.setCurrentIndex(index)
            self.display_current()
            self.update_instruments()
                    
        self.display_current() #for some reason display_current needs ot be called twice if there is a startGAS; wasn't able to figure out why . 
        
        #below are the signals and slots
        self.ui.combo_classType.currentIndexChanged.connect(self.update_instruments)
        self.ui.combo_classType.currentIndexChanged.connect(self.check_delay_2)
        self.ui.combo_classType.currentIndexChanged.connect(self.check_amplitude)
        self.ui.combo_instrumentType.currentIndexChanged.connect(self.update_addresses)
        self.ui.combo_instrumentType.currentIndexChanged.connect(self.update_measurementType)
        self.ui.combo_measurementType.currentIndexChanged.connect(self.update_ports)
        self.ui.combo_instrumentType.currentIndexChanged.connect(self.update_delay)
        self.ui.edit_name.textChanged.connect(self.toggle_done)
        self.ui.combo_name.currentIndexChanged.connect(self.display_current)
        self.ui.button_done.clicked.connect(self.edit_obj)
        
    def check_amplitude(self): 
        #if the object is the microwave shit, turon on the option to set the amplitude
        classType = str(self.ui.combo_classType.currentText())
        on = classType == 'setMicrowaveSource'
        self.ui.combo_amplitude.setEnabled(on)
        self.ui.edit_amplitude.setEnabled(on)
        
    def check_delay_2(self):
        #If it's a setBField object, turn on the option for the second delay
        classType = str(self.ui.combo_classType.currentText())
        on =  classType == 'setBField' # the one type that allows a second delay
        self.ui.edit_delay_2.setEnabled(on)
        self.ui.combo_delay_2.setEnabled(on)
        
    def display_current(self):
        #shows the current attributes of the selected object
        name = str(self.ui.combo_name.currentText())
        if not name:#sometimes the signals call this method unecessarily
            return
        attr = GASconfig.getGASattributes(self.GASfilename, name) # returns a dictionary of the attributes of the object
        self.ui.edit_name.clear()
        self.ui.edit_name.insert(name)
        
        classTypeIndex_combo = self.ui.combo_classType.findText(attr[getAndSet.classType])
        self.ui.combo_classType.setCurrentIndex(classTypeIndex_combo) 
        
        instTypeIndex_combo = self.ui.combo_instrumentType.findText(attr[getAndSet.instrument])
        self.ui.combo_instrumentType.setCurrentIndex(instTypeIndex_combo)
        
        self.update_addresses() #update the fields now that we have an instrument in place. 
        self.update_measurementType()
        
        if getAndSet.measType in attr: # we want to see if this object has these traits before we tru to set them
            measTypeIndex_combo = self.ui.combo_measurementType.findText(attr[getAndSet.measType])
            self.ui.combo_measurementType.setEnabled(True)
            self.ui.combo_measurementType.setCurrentIndex(measTypeIndex_combo)
            
        if getAndSet.port in attr: 
            self.ui.spin_port.setValue(int(attr[getAndSet.port]))
        else:
            self.ui.spin_port.setEnabled(False)
            
        self.ui.edit_OCR.clear()
        if getAndSet.OCR in attr:
                self.ui.edit_OCR.insert(attr[getAndSet.OCR].strip()[0])
                
        if getAndSet.delay in attr:
            self.ui.edit_delay.clear()
            self.ui.edit_delay.insert(attr[getAndSet.delay])
            
            if getAndSet.TCM in attr:
                if attr[getAndSet.TCM]:
                    self.ui.combo_delay.setCurrentIndex(self.ui.combo_delay.findText('Multiples of Time Constant'))
                else:
                    self.ui.combo_delay.setCurrentIndex(self.ui.combo_delay.findText('Seconds'))
                
        if getAndSet.delay2 in attr:
            self.ui.edit_delay_2.clear()
            self.ui.edit_delay_2.insert(attr[getAndSet.delay2])
            if getAndSet.TCM2 in attr:
                if attr[getAndSet.TCM2]:
                        self.ui.combo_delay_2.setCurrentIndex(self.ui.combo_delay_2.findText('Multiples of Time Constant'))
                else:
                    self.ui.combo_delay_2.setCurrentIndex(self.ui.combo_delay_2.findText('Seconds'))
                    
        if getAndSet.gC in attr:
            index = self.ui.combo_current.findText(attr[getAndSet.gC])
            if index != -1:
                self.ui.combo_current.setCurrentIndex(index)
                
        if getAndSet.gV in attr:
            index = self.ui.combo_Voltage.findText(attr[getAndSet.gV])
            if index != -1:
                self.ui.combo_Voltage.setCurrentIndex(index)
            
        if getAndSet.amp in attr:
            amp = attr[getAndSet.amp].split(' ')[0]
            self.ui.edit_amplitude.clear()
            self.ui.edit_amplitude.insert(amp)
            ampUnit = attr[getAndSet.amp].split(' ')[1]
            index = self.ui.combo_amplitude.findText(ampUnit)
            if index != -1:
                self.ui.combo_amplitude.setCurrentIndex(index)
            
        comment = attr[getAndSet.comment].strip()
        self.ui.edit_comment.clear()
        self.ui.edit_comment.insert(comment)
        #update some other things. 
        self.update_delay()
        self.check_amplitude()
        
    def edit_obj(self):
        #similar to adding an object , we call the edit function. Instead of closing, we simply re-updated the combo box and send a signal to the main window. 
        oldName = str(self.ui.combo_name.currentText())
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
        
        kwargs = {getAndSet.GASname: name} #add the pertinant objects to the initialization dictionary
        
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
            
        GASconfig.editGAS(self.GASfilename, self.INSTfilename,oldName, classType, InstrumentType,**kwargs)
            
        self.edit_signal.emit()
        self.fill_combo()
    
    def fill_combo(self):
        #fills the combo box with teh names of objects. 
        names = GASconfig.getGASNames(self.GASfilename)
        self.ui.combo_name.clear()
        self.ui.combo_name.addItems(names)
        self.display_current()
    
    def toggle_done(self):
        #turns the done button on or off depending on if there is text in the name field. 
        text = str(self.ui.edit_name.text())
        if text:
            self.ui.button_done.setEnabled(True)
        else:
            self.ui.button_done.setEnabled(False)
                        
    def update_instruments(self):
        #puts the correct instruments in the combo box depending on which Class is in the ClassType box. Also updates the boxes below it. 
        self.ui.combo_instrumentType.clear()
        topName = self.ui.combo_classType.currentText()

        for instrument in self.INSTlist:
            if topName in self.INSTdict[instrument].validGetsAndSets: #if the className is a valid possibility for this instrument
                self.ui.combo_instrumentType.addItem(instrument)
        #update all others
        self.update_addresses()
        self.update_measurementType()
        self.update_ports()
        self.update_OCR()
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
        if currentINST == 'Lock-in Amplifier'  and currentClassType[:3] == 'get':
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
            if self.INSTdict[topInst].validMeasurementTypes[topClass]: # if this instrument has measurement types for this class
                self.ui.combo_measurementType.setEnabled(True)
                self.ui.combo_measurementType.addItems(self.INSTdict[topInst].validMeasurementTypes[topClass])
            else:
                self.ui.combo_measurementType.setEnabled(False)
            
    
    def update_OCR(self):
        #turns OCR on and off depending on if the current class is a current getter or setter
        topClass = str(self.ui.combo_classType.currentText())
        if topClass[1:] == 'etCurrent': #a current method
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
        
            
def main(filename): #like all GUI modules, this one can be run on it's own. 
    app = QtGui.QApplication(sys.argv)
    ex = Start(filename)
    ex.show()
    app.exec_()
    
if __name__== '__main__':
    fname = 'C:\MeasurementConfig\GASconfig.txt'
    main(fname)