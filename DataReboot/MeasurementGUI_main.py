'''
7/2/2013
Sean McLaughlin
This is the companion module to the MeasurementGUI.py autognerated module. This module opens the window and calls the measurement.
'''

import sys
from PyQt4 import QtGui, QtCore
from MeasurementGUI import Ui_MainWindow
import GASconfig
import pyqtgraph as pg
from time import time
import LabData
import numpy as np
from itertools import izip

def lineNo():
    import inspect
    return 'Line '+str(inspect.currentframe().f_back.f_lineno)

def parseKeyValue(line):
    # a funciton that will take a line and split it along the equals sign and make a tuple
    splitLine = line.split('=')
    if len(splitLine) != 2:
        return None #if the length is not 2, this line may be blank, or not have a key value
    return (splitLine[0].strip(), splitLine[1].strip())

class Start(QtGui.QMainWindow):
    
    #signals need to be declared out here.
    plot_signal = QtCore.pyqtSignal()
    abort_signal = QtCore.pyqtSignal()
    done_signal = QtCore.pyqtSignal()
    write_signal = QtCore.pyqtSignal()
    check_run_signal = QtCore.pyqtSignal()
    plot_noise_signal = QtCore.pyqtSignal()
    update_GAS_INST_signal = QtCore.pyqtSignal()
    
    def __init__(self,fileDict,preset,GASdict, INSTdict, parent = None):
        super(Start, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.parent = parent
        #instance variables and initialization
        self.GASFilename = fileDict['GAS']
        self.INSTFilename = fileDict['INST']
        self.PRESETFilename = fileDict['PRESET']
        self.GASdict = GASdict
        self.INSTdict = INSTdict
        
        self.dataFilename = ''
        self.lastDirectory = ''
        self.abort = False
        self.isRunning = False
        
        self.__data__ = None
        
        self.signals = {'Plot': self.plot_signal, 'Abort' : self.abort_signal, 'Done' :self.done_signal, 'Write': self.write_signal, 
                        'Check Run' : self.check_run_signal, 'Plot Noise': self.plot_noise_signal, 'Update GAS INST': self.update_GAS_INST_signal}
        self.colors = ('b', 'g', 'r', 'c', 'm', 'y', 'w') # a tuple of the valid colors to use for plotting lines
        
        #create an imageview widget to put in the center of the screen
        #NOTE this code is copied from the code that creates the plot widget; if the dimensions and code for the plot widget change, this code will no longer work. 
        self.ui.imv = pg.ImageView(self.ui.centralwidget)
        self.add_graph(self.ui.imv, 'imv')
        self.ui.imv.hide()
        
        self.plots = [pg.PlotWidget()] # a list of all the plots in the layout
        self.ui.pqlayout.addWidget(self.plots[0])
        
        #signals and slot connections below
        self.ui.action_Open_GASFile.triggered.connect(self.open_GASFile)
        self.ui.button_openDataFile.clicked.connect(self.open_dataFile)
        self.ui.combo_sweep2_1.currentIndexChanged.connect(self.check_sweep_2)
        self.ui.combo_sweep3_1.currentIndexChanged.connect(self.check_sweep_3)
        
        self.ui.actionOpen_GASEdit.triggered.connect(self.open_GASconfig)
        self.ui.actionOpen_INSTEdit.triggered.connect(self.open_INSTconfig)
        
        self.ui.combo_sweep1_1.currentIndexChanged.connect(self.set_read_1)
        self.ui.combo_sweep2_1.currentIndexChanged.connect(self.set_read_2)
        self.ui.combo_sweep3_1.currentIndexChanged.connect(self.set_read_3)
        
        self.ui.combo_read_1.currentIndexChanged.connect(self.set_plot_axes)
        self.ui.combo_sweep1_1.currentIndexChanged.connect(self.set_plot_axes)
        self.ui.combo_sweep2_1.currentIndexChanged.connect(self.set_plot_axes)
        self.ui.combo_sweep3_1.currentIndexChanged.connect(self.set_plot_axes)
        
        self.ui.combo_plotType.currentIndexChanged.connect(self.change_plotType)
        self.ui.combo_sweep2_1.currentIndexChanged.connect(self.change_plotType)
        
        self.ui.combo_sweep1_1.currentIndexChanged.connect(self.set_units_1)
        self.ui.combo_sweep2_1.currentIndexChanged.connect(self.set_units_2)
        self.ui.combo_sweep3_1.currentIndexChanged.connect(self.set_units_3)
        
        self.ui.combo_sweep1_1.currentIndexChanged.connect(self.check_GAPSD)
        
        self.ui.edit_sweep1_dataPoints.editingFinished.connect(self.write_stepSize_1)
        self.ui.edit_sweep1_stepSize.editingFinished.connect(self.write_dataPoints_1)
        self.ui.edit_sweep2_dataPoints.editingFinished.connect(self.write_stepSize_2)
        self.ui.edit_sweep2_stepSize.editingFinished.connect(self.write_dataPoints_2)
        self.ui.edit_sweep3_dataPoints.editingFinished.connect(self.write_stepSize_3)
        self.ui.edit_sweep3_stepSize.editingFinished.connect(self.write_dataPoints_3)
        
        self.ui.combo_sweep1_stepSizeUnit.currentIndexChanged.connect(self.write_dataPoints_1)
        self.ui.combo_sweep2_stepSizeUnit.currentIndexChanged.connect(self.write_dataPoints_2)
        self.ui.combo_sweep3_stepSizeUnit.currentIndexChanged.connect(self.write_dataPoints_3)
        
        self.ui.check_sweep1_loop.stateChanged.connect(self.write_dataPoints_1)
        self.ui.check_sweep2_loop.stateChanged.connect(self.write_dataPoints_2)
        self.ui.check_sweep3_loop.stateChanged.connect(self.write_dataPoints_3)
        
        self.ui.edit_sweep1_start.textEdited.connect(self.write_dataPoints_1)
        self.ui.edit_sweep1_end.textEdited.connect(self.write_dataPoints_1)
        self.ui.edit_sweep2_start.textEdited.connect(self.write_dataPoints_2)
        self.ui.edit_sweep2_end.textEdited.connect(self.write_dataPoints_2)
        self.ui.edit_sweep3_start.textEdited.connect(self.write_dataPoints_3)
        self.ui.edit_sweep3_end.textEdited.connect(self.write_dataPoints_3)
        
        self.ui.edit_dataFile.textChanged.connect(self.check_run)
        self.ui.edit_dataFile.editingFinished.connect(self.change_dataFile)
        self.ui.edit_sweep1_start.textChanged.connect(self.check_run)
        self.ui.edit_sweep1_end.textChanged.connect(self.check_run)
        self.ui.edit_sweep1_dataPoints.textChanged.connect(self.check_run)
        self.ui.edit_sweep1_stepSize.textChanged.connect(self.check_run)
        self.ui.edit_sweep2_start.textChanged.connect(self.check_run)
        self.ui.edit_sweep2_end.textChanged.connect(self.check_run)
        self.ui.edit_sweep2_dataPoints.textChanged.connect(self.check_run)
        self.ui.edit_sweep2_stepSize.textChanged.connect(self.check_run)
        self.ui.edit_sweep3_start.textChanged.connect(self.check_run)
        self.ui.edit_sweep3_end.textChanged.connect(self.check_run)
        self.ui.edit_sweep3_dataPoints.textChanged.connect(self.check_run)
        self.ui.edit_sweep3_stepSize.textChanged.connect(self.check_run)
        self.ui.combo_sweep2_1.currentIndexChanged.connect(self.check_run)
        self.ui.combo_sweep3_1.currentIndexChanged.connect(self.check_run)
        self.ui.combo_sweep1_2.currentIndexChanged.connect(self.check_run)
        self.ui.combo_sweep1_1.currentIndexChanged.connect(self.check_run)
        self.check_run_signal.connect(self.check_run)
        
        self.ui.button_run.clicked.connect(self.run_measurement)
        self.ui.button_abort.clicked.connect(self.abort_measurement)
        
        self.ui.action_Calibrate_B_Field.triggered.connect(self.calibrateBField)
        self.ui.action_Get_Background_Subtract.triggered.connect(self.getBackgroundSub)
        self.ui.action_Set_Microwave_Amplitude.triggered.connect(self.set_microwave_amp)
        
        self.ui.combo_read_1.currentIndexChanged.connect(self.set_toolTip_read1)
        self.ui.combo_sweep1_1.currentIndexChanged.connect(self.set_toolTip_sweep11)
        self.ui.combo_sweep1_2.currentIndexChanged.connect(self.set_toolTip_sweep12)
        self.ui.combo_sweep2_1.currentIndexChanged.connect(self.set_toolTip_sweep21)
        self.ui.combo_sweep2_2.currentIndexChanged.connect(self.set_toolTip_sweep22)
        self.ui.combo_sweep3_1.currentIndexChanged.connect(self.set_toolTip_sweep31)
        self.ui.combo_sweep3_2.currentIndexChanged.connect(self.set_toolTip_sweep32)
        
        self.ui.action_Open_Preset.triggered.connect(self.open_preset)
        self.ui.action_Save_as_Preset.triggered.connect(self.save_as_preset)
        self.ui.actionEdit_Delete_Presets.triggered.connect(self.del_preset)
        
        self.done_signal.connect(self.finish_measurement)
        self.plot_signal.connect(self.plot_data)
        self.write_signal.connect(self.write_data)
        self.plot_noise_signal.connect(self.plot_noise)
        
        self.ui.button_refresh_plot.clicked.connect(self.plot_data)
        self.ui.button_check_run.clicked.connect(self.check_run_dialog)
        
        if __name__ == '__main__':
            self.initialize()
        else:
            self.open_GASFile()
            if preset is not None:
                self.open_preset(preset)
                
    def abort_measurement(self):
        #aborts a running measurement
        self.abort = True
        
    def add_graph(self, item , name): 
        #Adds a plot item in the place of thte main plot widget. Used to recreate the plot or add imageview
        item.setEnabled(True)
        item.setMinimumSize(QtCore.QSize(850, 500))
        item.setObjectName(name)
        self.ui.gridLayout.addWidget(item, 3, 0, 1, 1)
        
    def any_running(self):
        if self.parent is not None:
            return self.parent.any_running()
        else:
            return self.isRunning
        
    def calibrateBField(self):
        #opens calibrateBField and gets a calibration.
        import calibrateBfield_main
        
        getters = []
        setters = []
        
        for item in self.GASdict.iteritems():
            if item[1].className == 'getBField':
                getters.append(item)
            elif item[1].className == 'setBField':
                setters.append(item)
        
        getters = dict(getters)#make a dict of the getters and setters we presently have. 
        setters = dict(setters)
        try:
            self.calBField_window = calibrateBfield_main.Start(self.GASFilename, setters, getters)
        except calibrateBfield_main.Start.calibrateBFieldError, value:
            self.ui.statusbar().showMessage(value)
        self.calBField_window.show()
        
    def change_dataFile(self):
        #runs when the datafile field is manually changed. Saves the new name to self.dataFile
        name = str(self.ui.edit_dataFile.text())
        self.open_dataFile(name) 
        
    def change_plotType(self):
        #based on what plot type is chosen, turn on the buttons for that plot. 
        plotType = str(self.ui.combo_plotType.currentText())
        self.statusBar().showMessage('')
        if plotType == '':
            return 
        elif plotType == 'Line':
            self.ui.combo_xAxis.setEnabled(True)
            self.ui.combo_xScale.setEnabled(True)
            self.ui.combo_yScale.setEnabled(True)
            self.ui.combo_image_x.setEnabled(False)
            self.ui.combo_image_y.setEnabled(False)
            self.ui.combo_image_z.setEnabled(False)
            
            if not self.ui.pqlayout.isVisible():
                self.ui.pqlayout.show()
                self.ui.imv.hide()
            
        elif plotType == 'Image':
            self.ui.combo_xAxis.setEnabled(False)
            self.ui.combo_xScale.setEnabled(False)
            self.ui.combo_yScale.setEnabled(False)
            if str(self.ui.combo_sweep2_1.currentText()) != 'None': # need 2 sweeps to make an image
                self.ui.combo_image_x.setEnabled(True)
                self.ui.combo_image_y.setEnabled(True)
                self.ui.combo_image_z.setEnabled(True)
            else: 
                self.statusBar().showMessage('There must be a second sweep selected to do an image')
            if not self.ui.imv.isVisible():
                self.ui.imv.show()
                self.ui.pqlayout.hide()
            
    def check_abort(self):
        # in order to check the boolean in anotehr thread, it needs to be called from here. 
        return self.abort
        
    def check_GAPSD(self):
        #if the selected name for sweep1 is a spectrum analyzer, the read value is changed. 
        sweep1Name = str(self.ui.combo_sweep1_1.currentText())
        if not sweep1Name:
            return
        if self.GASdict[sweep1Name].isGASPSD():
            self.ui.edit_sweep1_stepSize.setEnabled(False)
            i = self.ui.combo_read_1.findText('SpecAnalyzerOut')
            if i == -1:
                self.ui.combo_read_1.addItem('SpecAnalyzerOut')
                i = self.ui.combo_read_1.findText('SpecAnalyzerOut')
                self.ui.combo_read_1.setCurrentIndex(i)
            else:
                self.ui.combo_read_1.setCurrentIndex(i)
                
            i = self.ui.combo_image_z.findText('SpecAnalyzerOut')
            if i==-1:
                self.ui.combo_image_z.addItem('SpecAnalyzerOut')
        else:
            self.ui.edit_sweep1_stepSize.setEnabled(True)
            i = self.ui.combo_read_1.findText('SpecAnalyzerOut')
            if i != -1:
                self.ui.combo_read_1.removeItem(i)
            i = self.ui.combo_image_z.findText('SpecAnalyzerOut')
            if i != -1:
                self.ui.combo_image_z.removeItem(i)
        
    def check_run(self):
        #turns on the run button if certain conditions are met 
        #does not open the dialog
        return self.check_run_main(False)
    
    def check_run_dialog(self): 
    #calls the check_run function, but with the arguement to open a dialog showing all the errors, not just one
        self.check_run_main(True)
        
    def check_run_main(self, showDialog = False):
        #main method of the check run family of functions. 
        enabled = True
        messages = []
        datapoints = [] #a list of all the data points; will be used to estimate the time. 
        
        dataFile = str(self.ui.edit_dataFile.text())
        if not dataFile:
            enabled = False
            messages.append('There is no dataFile selected')
        
        if self.parent is not None:
            runEnabled, message =  self.parent.allow_run()
            if enabled:
                enabled = runEnabled
            if message:
                messages.append(message)
        
        #check to see if all the fields for sweep 1 are filled in a valid manner
        sweep1Start = str(self.ui.edit_sweep1_start.text())
        sweep1End = str(self.ui.edit_sweep1_end.text())
        sweep1dp = str(self.ui.edit_sweep1_dataPoints.text())
        sweep1ss = str(self.ui.edit_sweep1_stepSize.text())
        sweep1Name = str(self.ui.combo_sweep1_1.currentText())
        if not sweep1Name: # in between states
            return
        sweep1 = self.GASdict[sweep1Name]
        try:
            sweep1Start = float(sweep1Start)
            sweep1End = float(sweep1End)
            sweep1dp = int(float(sweep1dp))
            sweep1ss = float(sweep1ss)
            if sweep1dp*sweep1ss==0 : # if any of them is 0, this will equal 0
                raise ZeroDivisionError
            if sweep1Start-sweep1End == 0:
                raise ZeroDivisionError
            
            if sweep1.isGASPSD() and (sweep1Start<0 or sweep1End <0):# negative frequencies are nonsense
                raise ZeroDivisionError
            
            datapoints.append(sweep1dp)
        except: #exit if any of them are not valid numbers or if the other if's above are satisfied
            messages.append('There is a problem with the Sweep 1 Inputs')
            enabled = False
        if self.check_sweep_2(): #returns true if sweep 2 is on
            sweep2Start = str(self.ui.edit_sweep2_start.text())
            sweep2End = str(self.ui.edit_sweep2_end.text())
            sweep2dp = str(self.ui.edit_sweep2_dataPoints.text())
            sweep2ss = str(self.ui.edit_sweep2_stepSize.text())
            try:
                sweep2Start = float(sweep2Start)
                sweep2End = float(sweep2End)
                sweep2dp = int(float(sweep2dp))
                sweep2ss = float(sweep2ss)
                if sweep2dp*sweep2ss==0 : # if any of them is 0, this will equal 0
                    raise ZeroDivisionError
                if sweep2Start-sweep2End == 0:
                    raise ZeroDivisionError
                datapoints.append(sweep2dp)
            except: #exit if any of them are not valid numbers or if the other if's above are satisfied
                messages.append('There is a problem with the Sweep 2 Inputs')
                enabled = False
            
        if self.check_sweep_3(): #valid if sweep 3 is on
            sweep3Start = str(self.ui.edit_sweep3_start.text())
            sweep3End = str(self.ui.edit_sweep3_end.text())
            sweep3dp = str(self.ui.edit_sweep3_dataPoints.text())
            sweep3ss = str(self.ui.edit_sweep3_stepSize.text())
            try:
                sweep3Start = float(sweep3Start)
                sweep3End = float(sweep3End)
                sweep3dp = int(float(sweep3dp))
                sweep3ss = float(sweep3ss)
                if sweep3dp*sweep3ss==0 : # if any of them is 0, this will equal 0
                    raise ZeroDivisionError
                if sweep3Start-sweep3End == 0:
                    raise ZeroDivisionError
                datapoints.append(sweep3dp)
            except: #exit if any of them are not valid numbers or if the other if's above are satisfied
                messages.append('There is a problem with the Sweep 3 Inputs')
                enabled = False
                
        sweep1_2_name = str(self.ui.combo_sweep1_2.currentText())
        if sweep1_2_name != 'Set Point' and sweep1_2_name != '' and self.GASdict[sweep1_2_name].isNoiseSubtract():
            #if a noise subtract is selected we have more checks to do. 
            NSobj = self.GASdict[sweep1_2_name]
            backgroundStart = NSobj.freqRange[0]
            backgroundStop = NSobj.freqRange[1]
            backgroundPoints = NSobj.points
            
            sweep1StartUnit = str(self.ui.combo_sweep1_startUnit.currentText())
            sweep1_name = str(self.ui.combo_sweep1_1.currentText())
            unitR = self.GASdict[sweep1_name].unitDictionary[sweep1StartUnit]
            sweep1Start = sweep1Start*unitR
            sweep1End = sweep1End*unitR
            
            #if anything doesn't match up
            if sweep1Start != backgroundStart: 
                enabled = False
                messages.append('The specified start frequency does not match the frequency of the selected background subtract.')
                
            elif sweep1End != backgroundStop:
                enabled = False
                messages.append('The specified end frequency does not match the frequency of the selected background subtract.')
                
            elif sweep1dp != backgroundPoints:
                enabled = False
                messages.append('The specified number of data points does not match the number for the selected background subtract.')
                
                
        #the microwave source also requires special initialization
        sweeperNames = (str(self.ui.combo_sweep1_1.currentText()), str(self.ui.combo_sweep2_1.currentText()), str(self.ui.combo_sweep3_1.currentText()))
        sweepers = {}
        for name in sweeperNames:
            if name in self.GASdict:
                sweepers[name] = self.GASdict[name]
            
        for name, sweeper in sweepers.iteritems():
            if sweeper.className == 'setMicrowaveSource' and sweeper.amp == -1:
                enabled = False
                messages.append('The amplitude of %s has not been set.'%name)
                break
                
        if showDialog  and messages:
            reply = QtGui.QMessageBox.information(self, 'Check Run', '\n'.join(messages), 
                                              QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        elif messages:
            self.ui.statusbar.showMessage(messages[0])
        else:
            self.ui.statusbar.showMessage('')
            
        #if we've made it this far, we can turn on the button
        self.ui.button_run.setEnabled(enabled)
        
        if enabled:
            readerNames = (str(self.ui.combo_sweep1_2.currentText()), str(self.ui.combo_sweep2_2.currentText()), str(self.ui.combo_sweep3_2.currentText()),str(self.ui.combo_read_1.currentText()))
        
            readers = []
            for sweep, readerName in izip(sweepers, readerNames):
                if readerName not in self.GASdict:
                    readers.append(None)
                else:
                    readers.append(self.GASdict[readerName])
                    
            if readerNames[-1] in self.GASdict:
                readers.append(self.GASdict[readerNames[-1]])
            else:
                readers.append(None)
                
            self.estimate_time(sweepers.values(), readers, datapoints) #estimate how long the measurement will take
        else:
            self.ui.label_timeEstimate.setText('0h0m0s')
        
        return enabled
    
    def check_sweep_2(self):
        #this and the one below for sweep 3 check that if the first attribute of sweep 2 and 3 is not none and turns everything on.
        #returns a boolean indicating if everything was turned on or not. 
        ctext = str(self.ui.combo_sweep2_1.currentText())
        on = ('None' != ctext) and (ctext != self.ui.combo_sweep1_1.currentText()) # true if this text is not none or the same as the first. 
        self.ui.combo_sweep2_2.setEnabled(on)
        self.ui.edit_sweep2_start.setEnabled(on)
        self.ui.edit_sweep2_end.setEnabled(on)
        self.ui.edit_sweep2_dataPoints.setEnabled(on)
        self.ui.edit_sweep2_stepSize.setEnabled(on)
        self.ui.check_sweep2_loop.setEnabled(on)
        self.ui.combo_sweep2_startUnit.setEnabled(on)
        self.ui.combo_sweep2_endUnit.setEnabled(on)
        self.ui.combo_sweep2_stepSizeUnit.setEnabled(on)
        self.ui.combo_sweep3_1.setEnabled(on) # you can start the 3rd one once thesecond is set. 
        self.check_sweep_3()
        return on
        
    def check_sweep_3(self):
        ctext = self.ui.combo_sweep3_1.currentText()
        on = ('None' != ctext) and (ctext != self.ui.combo_sweep1_1.currentText()) and (ctext != self.ui.combo_sweep2_1.currentText()) and ('None' != self.ui.combo_sweep2_1.currentText())
        self.ui.combo_sweep3_2.setEnabled(on)
        self.ui.edit_sweep3_start.setEnabled(on)
        self.ui.edit_sweep3_end.setEnabled(on)
        self.ui.edit_sweep3_dataPoints.setEnabled(on)
        self.ui.edit_sweep3_stepSize.setEnabled(on)
        self.ui.check_sweep3_loop.setEnabled(on)
        self.ui.combo_sweep3_startUnit.setEnabled(on)
        self.ui.combo_sweep3_endUnit.setEnabled(on)
        self.ui.combo_sweep3_stepSizeUnit.setEnabled(on)
        
        if not on:
            self.ui.combo_sweep3_1.setCurrentIndex(0)
        
        return on
        
    def closeEvent(self, event):
        
        if self.parent is None or not self.parent.any_running(): # if there aren't any running, turn them off. 
            for GAS in self.GASdict.itervalues():
                GAS.off() #turn each GAS off on a close
            
        if self.parent is not None:
            self.parent.remove_window(self)
        else:
            event.accept()
        
    def data_to_array(self, xCol, yCol, dataCol, **slices):
        #turns self.data to an array
        #REMEMBER: THE FIRST INDEX IS THE COLUMN (X) THE SECOND IS THE ROW (Y)\
        #note that imv transposes the image when it displays it. 
        self. arr = self.__data__.data_to_array(xCol, yCol, dataCol, **slices)

    def del_preset(self):
        import deletePreset_main
        self.del_preset_window = deletePreset_main.deletePreset(self.PRESETFilename)
        self.del_preset_window.show()
            
    def emitter(self, n):
        #this is a centralized function for all my self-made signals. 
        # i'm considering making it a dictionary and n a string. 
        #n == 'Plot': plot_signal
        #n == 'Abort': abort_signal
        #n == 'Done': done_signal
        self.signals[n].emit()

    def estimate_time(self, sweepers, readers, datapoints):
        #estimate the amount of time a measurement will take
        #I would like to reexamine this method and test it for accuracy.
        def product(arr): #a function to take the product of all the values in a list. 
            prod = 1
            for val in arr:
                prod *= val
            return prod
        
        time = 0
        index = 0
        for sweep, read in izip(sweepers, readers):
            delay = sweep.delay #ignoring the possibility of the sweeper having 2 delays. Won't be significant on the large scale
            if read is not None:
                delay+= read.delay
            delay += .2 #adjust for all other possible delays aside from preset ones. 
            if sweep.isGASPSD():
                if index == len(datapoints):
                    time+=delay
                else:
                    time+= delay*product(datapoints[index+1:])
            else:
                time+=delay * product(datapoints[index:]) #multiply by the product of all the datapoints for overhead loops
            index +=1
        if readers[-1] is not None:
            time +=readers[-1].delay*product(datapoints)
            
        seconds = int(time%60)
        time = time/60
        minutes = int(time%60)
        hours = int(time/60)
        self.ui.label_timeEstimate.setText('%ih%im%is'%(hours, minutes,seconds))
        
    def initialize(self):
        #used for debugging only, fills in my standard inputs to save me time. 
        self.dataFilename = 'config&data\data.txt'
        self.ui.edit_dataFile.clear()
        self.ui.edit_dataFile.insert(self.dataFilename)
        
        self.open_GASFile()
        
#         self.ui.combo_plotType.setCurrentIndex(0)
#         self.ui.combo_sweep1_1.setCurrentIndex(0)
#         self.ui.combo_read_1.setCurrentIndex(0)
#         
#         self.ui.edit_sweep1_start.insert('12')
#         self.ui.edit_sweep1_end.insert('14')
#         self.ui.edit_sweep1_stepSize.insert('.008')
#         self.ui.edit_sweep1_stepSize.editingFinished.emit()
#         #self.ui.check_sweep1_loop.click()
#         self.set_read_1()
        
#         self.ui.combo_sweep2_1.setCurrentIndex(2)
#         self.ui.edit_sweep2_start.insert('1')
#         self.ui.edit_sweep2_end.insert('0')
#         self.ui.edit_sweep2_stepSize.insert('.1')
#         self.ui.edit_sweep2_stepSize.editingFinished.emit()
        
    def file_dialog(self):
        #a generic file dialog that r
        fd = QtGui.QFileDialog(self)
        fname = fd.getOpenFileName()
        from os.path import isfile
        if isfile(fname):
            self.statusBar().showMessage('Opening %s'%fname)
            return fname
        
    def finish_measurement(self):
        # this command undoes some of the things the run_measurement thread does.
        self.ui.button_run.setEnabled(True)
        self.ui.button_abort.setEnabled(False)
        self.ui.button_run.setText('Run')
        self.ui.button_check_run.setEnabled(True)
        self.abort = False
        self.isRunning = False
        self.emitter('Write')
        self.emitter('Plot')
        if self.parent:
            self.parent.check_runs(self) #this functions runs check run for all measurement windows. Some may have been waiting for this one to finish.
        
    def getBackgroundSub(self):
        #opens noiseSubtract_main and takes a background spectrum
        import noiseSubtract_main
        
        NSobjsDict = []
        for item in self.GASdict.items():
            if item[1].isNoiseSubtract():
                NSobjsDict.append(item)
        NSobjsDict = dict(NSobjsDict)
        
        if self.GASdict[str(self.ui.combo_sweep1_1.currentText())].isGASPSD():
            startFreq = float(self.ui.edit_sweep1_start.text())
            stopFreq = float(self.ui.edit_sweep1_end.text())
            points = int(self.ui.edit_sweep1_dataPoints.text())
            stepSize = float(self.ui.edit_sweep1_stepSize.text())
            
            args = (startFreq, stopFreq, points, stepSize)
        else:
            args = ('', '', '' ,'')
        
        try:
            self.NS_window = noiseSubtract_main.Start(NSobjsDict, self.emitter, args)
        except noiseSubtract_main.Start.noiseSubtractException, value:
            self.statusBar().showMessage(value)
            return
        self.NS_window.show()   
    
    def open_dataFile(self, fname = None):
        #gets the datafile for the user to write to
        if fname is None or fname==False:
            fd = QtGui.QFileDialog(self)
            if self.lastDirectory:
                fd.setDirectory(self.lastDirectory)
            fname = str(fd.getSaveFileName(filter = '*.txt;;*.dat;;*.csv;;*.*', selectedFilter = '*.dat'))#set the default filetype to save. 
            
        if fname:
            self.dataFilename = fname
            self.lastDirectory = fname[:fname.rfind('/')]
            self.ui.edit_dataFile.clear()
            self.ui.edit_dataFile.insert(self.dataFilename.replace('/', '\\' ))
            
    def open_INSTconfig(self):
        # open the INSt file config window
        import INSTconfig_GUI_main
        self.INSTconfig = INSTconfig_GUI_main.Start(parent =self, filename =self.INSTFilename)
        self.INSTconfig.show()
    
    def open_GASconfig(self):
        #open the GASconfig window
        import Gasconfig_GUI_main
        self.GASconfig = Gasconfig_GUI_main.Start( parent = self, filename = self.GASFilename)
        self.GASconfig.show()
        
    def open_GASFile(self):
        #this module may be unecessary now that the master config has been implemented. 
        #opens the Get and Set file and uses it to populate the fields. 
        
        junk, self.INSTFilename = GASconfig.readConfig(self.GASFilename)
        del(junk)
        self.ui.combo_sweep1_1.clear()
        self.ui.combo_sweep2_1.clear()
        self.ui.combo_sweep3_1.clear()
        self.ui.combo_read_1.clear()
        self.ui.combo_sweep2_1.addItem('None')
        self.ui.combo_sweep3_1.addItem('None')
        for name in self.GASdict:
            
            attr = GASconfig.getGASattributes(self.GASFilename, name)
            if attr['Class Type'][:3] == 'get': #if this name corresponds to a getter
                self.ui.combo_read_1.addItem(name)
                #self.ui.combo_sweep1_2.addItem(name)
                #self.ui.combo_sweep2_2.addItem(name)
                #self.ui.combo_sweep3_2.addItem(name)
            else: #it's a setter
                self.ui.combo_sweep1_1.addItem(name)
                if not self.GASdict[name].isGASPSD(): #the power spectrum can only be in the lowest loop
                    self.ui.combo_sweep2_1.addItem(name)
                    self.ui.combo_sweep3_1.addItem(name)
       
        for value in self.GASdict.itervalues():
            if value.isGASPSD(): #if we have a spectrum analyzer, we need to add a noise subtract for it.
                from getAndSet import NoiseSubtract
                kwargs = {'Name' : 'Noise Subtract', 'Instrument' : value.LIRef}
                self.GASdict['Noise Subtract'] = NoiseSubtract(**kwargs)
                break
                
        self.ui.combo_read_1.setEnabled(True)
        self.ui.button_check_run.setEnabled(True)
        self.start_sweep_1()
        
    def open_preset(self, preset = None):
        #opens a dialog where the user can select a preset to open
        presetNames = []
        presetFile = open(self.PRESETFilename, 'r') 
        for line in presetFile: #gather all the names from the preset file
            values = parseKeyValue(line)
            if values is not None and values[0] == 'Name':
                presetNames.append(values[1])
        presetFile.close()
        if not preset:
            import preset_dialog_main
            
            self.presetDialog = preset_dialog_main.PresetDialog(presetNames)
            if not self.presetDialog.exec_():
                return
            else:
                presetName = self.presetDialog.getChoice()
        else:
            presetName = preset
        
        presetFile = open(self.PRESETFilename, 'r')
        lines = []
        for line in presetFile:
            lines.append(line)
            
        for index, line in enumerate(lines):
            values = parseKeyValue(line)
            if values is not None and values[1] == presetName:
                break
            
        presetDict = {}
        for line in lines[index+1:]:
            if line == 'END\n':
                break
            values = parseKeyValue(line)
            if values is not None:
                presetDict[values[0]] = values[1]
                
        #now that I have a dictionary of the preset values, go through it and put the values in the appropriate places. 
        if 'Reader' in presetDict:
            i = self.ui.combo_read_1.findText(presetDict['Reader'])
            self.ui.combo_read_1.setCurrentIndex(i)
            
        if 'Sweep 1' in presetDict:
            i = self.ui.combo_sweep1_1.findText(presetDict['Sweep 1'])
            self.ui.combo_sweep1_1.setCurrentIndex(i)
            
            i = self.ui.combo_sweep1_2.findText(presetDict['Sweep 1 Read'])
            self.ui.combo_sweep1_2.setCurrentIndex(i)
            
            if presetDict['Sweep 1 Loop'] == 'True':
                self.ui.check_sweep1_loop.setChecked(True)
            else:
                self.ui.check_sweep1_loop.setChecked(False)
            
            if 'Sweep 1 Range' in presetDict:
                range = presetDict['Sweep 1 Range']
                start = range[range.find('(')+1: range.find(',')].strip()
                end = range[range.find(',') + 1: range.find(')')].strip()
                unit = range[range.find(')')+ 1:].strip()
                
                self.ui.edit_sweep1_start.clear()
                self.ui.edit_sweep1_start.insert(start)
                self.ui.edit_sweep1_end.clear()
                self.ui.edit_sweep1_end.insert(end)
                i = self.ui.combo_sweep1_startUnit.findText(unit)
                self.ui.combo_sweep1_startUnit.setCurrentIndex(i)
                
                if 'Sweep 1 Step Size' in presetDict:
                    stepAndUnit = presetDict['Sweep 1 Step Size']
                    stepSize = stepAndUnit[:stepAndUnit.find(' ')]
                    unit = stepAndUnit[stepAndUnit.find(' ') +1 :].strip()
                    
                    self.ui.edit_sweep1_stepSize.clear()
                    self.ui.edit_sweep1_stepSize.insert(stepSize)
                    i = self.ui.combo_sweep1_stepSizeUnit.findText(unit)
                    self.ui.combo_sweep1_stepSizeUnit.setCurrentIndex(i)
                    
                if 'Sweep 1 Data Points' in presetDict:
                    self.ui.edit_sweep1_dataPoints.clear()
                    self.ui.edit_sweep1_dataPoints.insert(presetDict['Sweep 1 Data Points'])
                    
        if 'Sweep 2' in presetDict:
            i = self.ui.combo_sweep2_1.findText(presetDict['Sweep 2'])
            self.ui.combo_sweep2_1.setCurrentIndex(i)
            
            i = self.ui.combo_sweep2_2.findText(presetDict['Sweep 2 Read'])
            self.ui.combo_sweep2_2.setCurrentIndex(i)
            
            if presetDict['Sweep 2 Loop'] == 'True':
                self.ui.check_sweep2_loop.setChecked(True)
            else:
                self.ui.check_sweep2_loop.setChecked(False)
            
            if 'Sweep 2 Range' in presetDict:
                range = presetDict['Sweep 2 Range']
                start = range[range.find('(')+1: range.find(',')].strip()
                end = range[range.find(',') + 1: range.find(')')].strip()
                unit = range[range.find(')')+ 1:].strip()
                
                self.ui.edit_sweep2_start.clear()
                self.ui.edit_sweep2_start.insert(start)
                self.ui.edit_sweep2_end.clear()
                self.ui.edit_sweep2_end.insert(end)
                i = self.ui.combo_sweep2_startUnit.findText(unit)
                self.ui.combo_sweep2_startUnit.setCurrentIndex(i)
                
                if 'Sweep 2 Step Size' in presetDict:
                    stepAndUnit = presetDict['Sweep 2 Step Size']
                    stepSize = stepAndUnit[:stepAndUnit.find(' ')]
                    unit = stepAndUnit[stepAndUnit.find(' ') +1 :].strip()
                    
                    self.ui.edit_sweep2_stepSize.clear()
                    self.ui.edit_sweep2_stepSize.insert(stepSize)
                    i = self.ui.combo_sweep2_stepSizeUnit.findText(unit)
                    self.ui.combo_sweep2_stepSizeUnit.setCurrentIndex(i)
                    
                if 'Sweep 2 Data Points' in presetDict:
                    self.ui.edit_sweep2_dataPoints.clear()
                    self.ui.edit_sweep2_dataPoints.insert(presetDict['Sweep 2 Data Points'])
                    
        if 'Sweep 3' in presetDict:
            i = self.ui.combo_sweep3_1.findText(presetDict['Sweep 3'])
            self.ui.combo_sweep3_1.setCurrentIndex(i)
            
            i = self.ui.combo_sweep3_2.findText(presetDict['Sweep 3 Read'])
            self.ui.combo_sweep3_2.setCurrentIndex(i)
            
            if presetDict['Sweep 3 Loop'] == 'True':
                self.ui.check_sweep3_loop.setChecked(True)
            else:
                self.ui.check_sweep3_loop.setChecked(False)
            
            if 'Sweep 3 Range' in presetDict:
                range = presetDict['Sweep 3 Range']
                start = range[range.find('(')+1: range.find(',')].strip()
                end = range[range.find(',') + 1: range.find(')')].strip()
                unit = range[range.find(')')+ 1:].strip()
                
                self.ui.edit_sweep3_start.clear()
                self.ui.edit_sweep3_start.insert(start)
                self.ui.edit_sweep3_end.clear()
                self.ui.edit_sweep3_end.insert(end)
                i = self.ui.combo_sweep3_startUnit.findText(unit)
                self.ui.combo_sweep3_startUnit.setCurrentIndex(i)
                
                if 'Sweep 3 Step Size' in presetDict:
                    stepAndUnit = presetDict['Sweep 3 Step Size']
                    stepSize = stepAndUnit[:stepAndUnit.find(' ')]
                    unit = stepAndUnit[stepAndUnit.find(' ') +1 :].strip()
                    
                    self.ui.edit_sweep3_stepSize.clear()
                    self.ui.edit_sweep3_stepSize.insert(stepSize)
                    i = self.ui.combo_sweep3_stepSizeUnit.findText(unit)
                    self.ui.combo_sweep3_stepSizeUnit.setCurrentIndex(i)
                    
                if 'Sweep 3 Data Points' in presetDict:
                    self.ui.edit_sweep3_dataPoints.clear()
                    self.ui.edit_sweep3_dataPoints.insert(presetDict['Sweep 3 Data Points'])
                
    def parse_data(self, **kwargs ):
        #takes the self.data array and breaks it up based on specified input; returns the split array
        #for the key word arguements, the key indicates which sweep, and the value is value in that sweep that should be isolated
        #for example, to find where sweep 2 was .2, kwargs should be {'2': .2} Note that the key must be a string. 
        
        #return self.__data__.parse_data_search
        if self.__data__ is None: #before the measurement begins, the data object is Null
            return
        return self.__data__.parse_data_map(**kwargs)
                        
    def plot_data(self):
        #plots the data in self.data
        #t0 = time()
        for plot in self.plots:
            plot.clear()
        plotType = str(self.ui.combo_plotType.currentText())
        
        if not plotType or not self.__data__:
            return
        
        slice1 = str(self.ui.edit_slice1.text())
        slice1Unit = str(self.ui.combo_slice1.currentText())
        slice2 = str(self.ui.edit_slice2.text())
        slice2Unit = str(self.ui.combo_slice2.currentText())
        slice3 = str(self.ui.edit_slice3.text())
        slice3Unit = str(self.ui.combo_slice3.currentText())
        
        slices = {}
        try:
            
            if self.ui.check_sweep1_slice.isChecked():
                raise ZeroDivisionError 
            
            slice1 = float(slice1)
            name = str(self.ui.combo_sweep1_1.currentText())
            slice1SI = slice1 * self.GASdict[name].unitDictionary[slice1Unit]

            slices['1'] = slice1SI
        except:
            pass
        
        try:
            
            if self.ui.check_sweep2_slice.isChecked():
                raise ZeroDivisionError 
            
            slice2 = float(slice2)
            name = str(self.ui.combo_sweep2_1.currentText())
            slice2SI = slice2 * self.GASdict[name].unitDictionary[slice2Unit]

            slices['2'] = slice2SI
            
        except:
            pass
        
        try:
            
            if self.ui.check_sweep3_slice.isChecked():
                raise ZeroDivisionError 
            
            slice3 = float(slice3)
            name = str(self.ui.combo_sweep3_1.currentText())
            slice3SI = slice3 * self.GASdict[name].unitDictionary[slice3Unit]

            slices['3'] = slice3SI
            
        except:
            pass
        
        
        if plotType == 'Line':
            data = self.parse_data(**slices)
            
            xScale = str(self.ui.combo_xScale.currentText())
            yScale = str(self.ui.combo_yScale.currentText())
            xAxis = str(self.ui.combo_xAxis.currentText())

            nData = self.__data__.nData
            
            if xAxis == '':
                return # called in between cycles.
        
            if xScale == 'Linear':
                xLog = False
            else:
                xLog = True
                
            if yScale == 'Linear':
                yLog = False
            else:
                yLog = True
                
            for plot in self.plots:
                plot.setLogMode(x = xLog, y= yLog) #set the scales. 
            
            xDataIndex = -1
            
            if xAxis == str(self.ui.combo_read_1.currentText()) or xAxis == 'SpecAnalyzerOut': # need to relate the selected axis to where it is Stored in self.data
                xDataIndex =  0
            elif xAxis == str(self.ui.combo_sweep1_1.currentText()):
                xDataIndex = nData
                name = str(self.ui.combo_sweep1_1.currentText())
            elif xAxis == str(self.ui.combo_sweep2_1.currentText()):
                xDataIndex = nData+1
                name = str(self.ui.combo_sweep2_1.currentText())
            else:
                xDataIndex = nData+2
                name = str(self.ui.combo_sweep3_1.currentText())
                
            if xAxis != 'SpecAnalyzerOut':
                if self.GASdict[name].isGASPSD(): #the standUnit of the GASPSD currently is GHz. However, I don't know if I should have the special case here or in the combo boxes.
                    xUnit = 'Hz'
                else:
                    xUnit = self.GASdict[xAxis].standUnit()
            else:
                if self.GASdict[name].isGASPSD():
                    xUnit = self.GASdict[name].standUnit(reader = True) #spcial case 
                else:
                    xUnit = self.GASdict[str(self.ui.combo_sweep1_1.currentText())].standUnit(reader = True) #special case
                
            yLabels = []
            reader_name = str(self.ui.combo_read_1.currentText())
            if reader_name == 'SpecAnalyzerOut':
                reader = None
            else:
                reader = self.GASdict[reader_name]
            sweep1_name = str(self.ui.combo_sweep1_1.currentText())
            sweep1 = self.GASdict[sweep1_name]
            if reader is not None:
                if reader.type == 'RT':
                    unitR, unitT = reader.standUnit()
                    labelR = reader_name + 'R' 
                    unitR = '%s'%unitR
                    labelT = reader_name + 'T'  
                    unitT = '%s'%unitT
                    yLabels.extend([(labelR, unitR), (labelT, unitT)])
                else:
                    unit = reader.standUnit()
                    yLabels.append((reader_name,'%s'%unit))
            if  sweep1.isGASPSD():
                yLabels.append( (sweep1_name, '%s'%sweep1.standUnit(reader = True)))
                
            if len(self.plots) > nData: #pyqtgraph sucks. This module doens't have a remove, so I need to recreate the whole widget from scratch
                from pyqtgraph import LayoutWidget
                self.ui.pqlayout.hide()
                self.ui.pqlayout = LayoutWidget(self.ui.centralwidget)
                self.add_graph(self.ui.pqlayout, 'pqlayout')
                self.plots = [pg.PlotWidget()] # a list of all the plots in the layout
                self.ui.pqlayout.addWidget(self.plots[0])
                
            while len(self.plots) < nData:
                self.plots.append(pg.PlotWidget())
                self.ui.pqlayout.addWidget(self.plots[-1], row = 'next')
                
            for plot,dataCol,  label, color in izip(self.plots,data, yLabels, self.colors):
                plot.showGrid(True, True, .5)# set the axes on; .5 is the transparency of the lines from 0-1
                plot.plot(x = data[xDataIndex], y = dataCol, pen = pg.mkPen(color, width = 2))
                plot.setLabel('left', label[0], label[1])#the label and then the Unit
                plot.showLabel('left')
                plot.setLabel('bottom', xAxis, '%s'%xUnit)
                plot.showLabel('bottom')
            
        elif plotType == 'Image': # a 3-D representation
            nData = self.__data__.nData
            
            xAxis = str(self.ui.combo_image_x.currentText())
            yAxis = str(self.ui.combo_image_y.currentText())
            zAxis = str(self.ui.combo_image_z.currentText())
            
            #get xCol and yCol, the columns to turn into the x and y axes of the image.
            if xAxis == str(self.ui.combo_sweep1_1.currentText()):
                xCol = 0
            elif xAxis == str(self.ui.combo_sweep2_1.currentText()):
                xCol =  1
            else:
                xCol =  2 
                
            if yAxis == str(self.ui.combo_sweep1_1.currentText()):
                yCol = 0
            elif yAxis == str(self.ui.combo_sweep2_1.currentText()):
                yCol = 1
            else:
                yCol = 2
            
            #this would be a great place ot have a dictionary in the data object. 
            if zAxis in self.GASdict:
                dataCol =0
            elif zAxis == 'SpecAnalyzerOut':
                readText = str(self.ui.combo_read_1.currentText())
                if 'SpecAnalyzerOut' == readText: #if there is no other reader
                    dataCol = 0
                elif readText[:-1] in self.GASdict: #both the RT options are he name of their getter with either R or T on the end.
                    dataCol = 2
                else:
                    dataCol = 1
            else: #an RT measurement
                if zAxis[-1] == 'R':
                    dataCol = 0
                else:
                    dataCol = 1
                    
            self.data_to_array( xCol, yCol, dataCol, **slices)
            
            if len(self.arr) != 0: #if it's non-empty
                self.ui.imv.setImage(self.arr, scale = (len(self.arr[0]),len(self.arr)) ) #this scale makes sure the image is always square. 
        
        #Progress Bar
        
        data = self.parse_data()
        
        if not self.isRunning:
            self.ui.progressBar_1.setValue(0) # if a measurement isn't running don't bother with the progress bar. 
            self.ui.progressBar_2.setValue(0)
            self.ui.progressBar_3.setValue(0)
            self.ui.label_sweep1.setText('0')
            self.ui.label_sweep2.setText('0')
            self.ui.label_sweep3.setText('0')
        else:
            dataPointsText = self.ui.edit_sweep1_dataPoints.text()
            if not dataPointsText: #blank string in between cycles.
                self.ui.progressBar_1.setValue(0) # if a measurement isn't running don't bother with the progress bar. 
                self.ui.progressBar_2.setValue(0)
                self.ui.progressBar_3.setValue(0)
                self.ui.label_sweep1.setText('0')
                self.ui.label_sweep2.setText('0')
                self.ui.label_sweep3.setText('0')
                return
            
            dataPoints1 = int(dataPointsText) #we calculate these so we can use modular division to get how many points are along each sweep
            self.ui.progressBar_1.setValue(len(data[0])%dataPoints1)
            self.ui.label_sweep1.setText(str(data[nData][-1]))
            if self.ui.edit_sweep2_dataPoints.isEnabled():
                dataPoints2 = int(self.ui.edit_sweep2_dataPoints.text())
                self.ui.progressBar_2.setValue(int(len(data[0])/dataPoints1)%dataPoints2)
                self.ui.label_sweep2.setText(str(data[nData+1][-1]))
                
                if self.ui.edit_sweep3_dataPoints.isEnabled():
                    self.ui.progressBar_3.setValue(len(data[0])/(dataPoints1*dataPoints2))
                    self.ui.label_sweep3.setText(str(data[nData+2][-1]))
                else:
                    self.ui.progressBar_3.setValue(0)
                    self.ui.label_sweep3.setText('0')
            else:
                self.ui.progressBar_2.setValue(0)
                self.ui.label_sweep2.setText('0')
                self.ui.progressBar_3.setValue(0)
                self.ui.label_sweep3.setText('0')
        
    def plot_noise(self):
        #called when a spectrum is taken, plots the spectrum.
        for value in self.GASdict.values():
            if value.isNoiseSubtract():
                NSobj = value
                break
        import numpy as np
        if not self.ui.pqlayout.isVisible():
            self.ui.pqlayout.show()
            self.ui.imv.hide()
            
        self.ui.combo_plotType.setCurrentIndex(self.ui.combo_plotType.findText('Line')) # set the plot to line 
        
        xUnit = NSobj.standUnit()
        if len(self.plots) > 1: #pyqtgraph sucks. This module doens't have a remove, so I need to recreate the whole widget from scratch
            from pyqtgraph import LayoutWidget
            self.ui.pqlayout.hide()
            self.ui.pqlayout = LayoutWidget(self.ui.centralwidget)
            self.add_graph(self.ui.pqlayout, 'pqlayout')
            self.plots = [pg.PlotWidget()] # a list of all the plots in the layout
            self.ui.pqlayout.addWidget(self.plots[0])
            
        self.plots[0].clear()
        self.plots[0].enableAutoScale()
        self.plots[0].plot(x = np.linspace(NSobj.freqRange[0], NSobj.freqRange[1], NSobj.points, True) , y = NSobj.spectrum)
        self.plots[0].setLabel('left', 'Power' + ' (W)')
        self.plots[0].showLabel('left')
        self.plots[0].setLabel('bottom', 'Frequency' + ' (%s)'%xUnit)
        self.plots[0].showLabel('bottom')
        
    def run_measurement(self):
        # this is called when the run button is pressed and runs the measurement proper. 
        
        ##Check all the things that ensure the measurement will run ok
        if not self.check_run(): #double check that's it's ok to run a measurement
            return
        
        #first thing to do is check that the dataFile isn't one that already exists; it'd be bad to overwrite data!
        self.dataFilename = str(self.ui.edit_dataFile.text())
        from os.path import isfile
        while isfile(self.dataFilename): # this file already exists; we want to check with the user that this is what they want. 
            reply = QtGui.QMessageBox.warning(self, 'Overwrite?', 'This file already exists; are you sure you want to overwrite it?', 
                                              QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Open, QtGui.QMessageBox.No)
            
            if reply == QtGui.QMessageBox.No:
                self.ui.button_run.setEnabled(True)
                self.ui.button_check_run.setEnabled(True)
                self.ui.button_abort.setEnabled(False)
                self.ui.button_run.setText('Run')
                self.abort = False
                self.ui.progressBar_1.setValue(0)
                self.ui.progressBar_2.setValue(0)
                self.ui.progressBar_3.setValue(0)
                self.isRunning = False
                return #the user elected to cancel the measurement
            
            elif reply == QtGui.QMessageBox.Open:
                self.open_dataFile() # open a new data file; this reassigns self.dataFilename so the loop should break if necessary
                break #i'm not sure if I want a break here. I mean, here the open file takes care of the check that the fiel exists. I'ts a bit redundant to ask again. 
            else:
                break
            
        self.isRunning = True
        if self.parent:
            self.parent.check_runs(self) #turn off the runs for the other measurement windows that may be open.
        
        self.ui.button_abort.setEnabled(True) #we can abort now that it's running
        self.ui.button_run.setEnabled(False)
        self.ui.button_check_run.setEnabled(False)
        self.ui.button_run.setText('Running...')
        
        #the number of sweep and data columns. will be adjusted in the following code. 
        numSweeps = 1
        numData = 1 
        
        reader_name = str(self.ui.combo_read_1.currentText())

        sweeper1_set_name = str(self.ui.combo_sweep1_1.currentText())
        sweeper1_set = self.GASdict[sweeper1_set_name]
        
        try:
            reader = self.GASdict[reader_name]
            if reader.type == 'RT':
                numData+=1 #RT needs another column
        except KeyError: # if the spectrum analyzer is in use the reader name will change
            reader = None
        
        if sweeper1_set.isGASPSD() and reader is not None:
            numData+=1
            
        sweeper1_read_name = str(self.ui.combo_sweep1_2.currentText()) #take their names down; below these will be turned into references
        sweeper2_set_name = str(self.ui.combo_sweep2_1.currentText())
        sweeper2_read_name = str(self.ui.combo_sweep2_2.currentText())
        sweeper3_set_name = str(self.ui.combo_sweep3_1.currentText())
        sweeper3_read_name = str(self.ui.combo_sweep3_2.currentText())
        
        if sweeper1_read_name not in self.GASdict: #temporily make set point readers None; we'll make them fake objects in a bit
            sweeper1_read = None
        else:
            sweeper1_read = self.GASdict[sweeper1_read_name] # otherwise get it from the dictionary

        if sweeper2_read_name not in self.GASdict:
            sweeper2_read = None
        else:
            sweeper2_read = self.GASdict[sweeper2_read_name]
                                         
        if sweeper3_read_name not in self.GASdict:
            sweeper3_read = None
        else:
            sweeper3_read = self.GASdict[sweeper3_read_name]
            
        if sweeper2_set_name not in self.GASdict: # similarly with the other sweepers
            sweeper2_set = None
        else:
            sweeper2_set = self.GASdict[sweeper2_set_name]
        
        if sweeper3_set_name not in self.GASdict:
            sweeper3_set = None
        else:
            sweeper3_set = self.GASdict[sweeper3_set_name]
        
        def sign(n): # returns 1 or -1 dependign on the sign of n
            return n/abs(n)
        
#TODO: at the very least rename;
#consider adding a get() function to the setter class and use it as a fake getter, and see about fakeSetter set up too
        
        class fakeGetter(object):# this will be used when the 'set Point ' option is chosen for the sweeps
            #returns an item out of an array taht was initally passed in.
            def __init__(self, array):
                self.array = array
                self.index = -1
                
            def get(self): #cycles through the array; always returns a value, so need to be careful that it is being called the write number of times. 
                self.index+=1
                if self.index == len(self.array):
                    self.index = 0
                a =  self.array[self.index]
                return a
            
            def isNoiseSubtract(self):
                return False
            
        class fakeSetter(object): #thsi will be used when no measurment is selected for a loop.
            
            def set(self , x): # does nothing. 
                pass 
        
            def off(self): # also does nothing
                pass
        
        sweeper1_start = float(self.ui.edit_sweep1_start.text())*sweeper1_set.unitDictionary[str(self.ui.combo_sweep1_startUnit.currentText())]
        #...................^__________________________^...........^..............^.........^______________________________________________^__The current unit set as a string
        #...................|.......................................|..............|__ Take the unit and get the ratio to the SI one.
        #...................|.......................................|__The sweeper object in question
        #...................|__The value in the start field as a float
        #this gives us the start value in SI units

        sweeper1_end = float(self.ui.edit_sweep1_end.text())*sweeper1_set.unitDictionary[str(self.ui.combo_sweep1_endUnit.currentText())]
        sweeper1_dataPoints = int(self.ui.edit_sweep1_dataPoints.text())
        sweeper1_loop = self.ui.check_sweep1_loop.isChecked()
        
        sweeper1_standUnit = sweeper1_set.standUnit() # get the standard unit we're going to use internally. 

        #this range will hold the values for this sweep to iterate over
        sweeper1_range, sweeper1_stepSize = np.linspace(sweeper1_start, sweeper1_end, sweeper1_dataPoints/(1+sweeper1_loop), retstep = True) #must be cast from a numpy array to a python list 
        sweeper1_range = list(sweeper1_range)
        #the strange division by the loop ensures that the number of data poitns is halved when there is a loop
        
        if sweeper1_loop: # if we have to loop, insert the values again, backward. 
            sweeper1_range.extend(reversed(sweeper1_range))
        
        if sweeper1_read is None:
            sweeper1_read = fakeGetter(sweeper1_range) # make a fake getter for sweeper1_read
                
        sweeper1 = (sweeper1_set, sweeper1_read, sweeper1_range)
        #a tuple, so that we may compactly transfer the data into the measurement.
        
        sweeper2_loop = self.ui.check_sweep2_loop.isChecked()
        if sweeper2_set is None:
            sweeper2 = (fakeSetter(), fakeGetter([None]) , [None]) # there needs to be an array to iterate over once, as well as getters and setters to pretend to call
        else:
            numSweeps+=1
            sweeper2_start = float(self.ui.edit_sweep2_start.text())*sweeper2_set.unitDictionary[str(self.ui.combo_sweep2_startUnit.currentText())]
            sweeper2_end = float(self.ui.edit_sweep2_end.text())*sweeper2_set.unitDictionary[str(self.ui.combo_sweep2_endUnit.currentText())]
            sweeper2_dataPoints = int(self.ui.edit_sweep2_dataPoints.text())
            
            sweeper2_standUnit = sweeper2_set.standUnit() # get the standard unit we're going to use internally. 
            
            #this range will hold the values for this sweep to iterate over
            sweeper2_range, sweeper2_stepSize =  np.linspace(sweeper2_start, sweeper2_end, sweeper2_dataPoints/(1+sweeper2_loop), retstep = True)
            sweeper2_range = list(sweeper2_range)
            
            if sweeper2_loop: # if we have to loop, insert the values again, backward. 
                sweeper2_range.extend(reversed(sweeper2_range))
                    
            if sweeper2_read is None:
                sweeper2_num_range = [] # an array without the flags. 
                if not sweeper1[0].isGASPSD():
                    for i in sweeper2_range:
                        sweeper2_num_range.extend(i for counter in xrange( sweeper1_dataPoints))
                    
                else:
                        sweeper2_num_range.extend(sweeper2_range)
                            
                sweeper2_read = fakeGetter(sweeper2_num_range) # make a fake getter 
                    
            sweeper2 = (sweeper2_set, sweeper2_read, sweeper2_range)
            
        sweeper3_loop = self.ui.check_sweep3_loop.isChecked()
        if sweeper3_set == None:
            sweeper3 = (fakeSetter(), fakeGetter([None]), [None])
        else:
            numSweeps+=1
            sweeper3_start = float(self.ui.edit_sweep3_start.text())*sweeper3_set.unitDictionary[str(self.ui.combo_sweep3_startUnit.currentText())]
            sweeper3_end = float(self.ui.edit_sweep3_end.text())*sweeper3_set.unitDictionary[str(self.ui.combo_sweep3_endUnit.currentText())]
            sweeper3_dataPoints = int(self.ui.edit_sweep3_dataPoints.text())
                
            sweeper3_standUnit = sweeper3_set.standUnit() # get the standard unit we're going to use internally. 
                
            sweeper3_range, sweeper3_stepSize =  np.linspace(sweeper3_start, sweeper3_end, sweeper3_dataPoints/(1+sweeper3_loop), retstep = True)
            sweeper3_range = list(sweeper3_range)
                
            if sweeper3_loop: # if we have to loop, insert the values again, backward. 
                sweeper3_range.extend(reversed(sweeper3_range))
                    
            if sweeper3_read == None:
                sweeper3_num_range = [] #we need to extend the array so that multiple calls don't mess it up. This one will also have no flags. 
                if not sweeper1[0].isGASPSD():
                    for i in sweeper3_range:
                        sweeper3_num_range.extend(i for counter in xrange(sweeper2_dataPoints*sweeper1_dataPoints))
                else:                    
                    for i in sweeper3_range:
                        sweeper3_num_range.extend(i for counter in xrange( sweeper2_dataPoints))
                                    
                sweeper3_read = fakeGetter(sweeper3_num_range) # make a fake getter to read from. 
            sweeper3 = (sweeper3_set, sweeper3_read, sweeper3_range)
        
        self.__data__ = LabData.LabData( numData, numSweeps, self.dataFilename) #TODO: adjust this to work for multiple data columns. 
        
        #handle hte progress bar
        self.ui.progressBar_1.setMinimum(0)
        self.ui.progressBar_2.setMinimum(0)
        self.ui.progressBar_3.setMinimum(0)
        self.ui.progressBar_1.setValue(0)
        self.ui.progressBar_2.setValue(0)
        self.ui.progressBar_3.setValue(0)
        self.ui.label_sweep1.setText('0')
        self.ui.label_sweep2.setText('0')
        self.ui.label_sweep3.setText('0')
        
        if len(sweeper3[2]) != 1: # the progress bar will be updated with how many points are in the outermost loop; the highest sweep. If the array is one we know that it is 'fake'
            self.ui.progressBar_3.setMaximum(sweeper3_dataPoints)
            self.ui.progressBar_2.setMaximum(sweeper2_dataPoints)
            self.ui.progressBar_1.setMaximum(sweeper1_dataPoints)
        elif len(sweeper2[2]) != 1:
            self.ui.progressBar_3.setMaximum(1)
            self.ui.progressBar_2.setMaximum(sweeper2_dataPoints)
            self.ui.progressBar_1.setMaximum(sweeper1_dataPoints)
        else:
            self.ui.progressBar_3.setMaximum(1)
            self.ui.progressBar_2.setMaximum(1)
            self.ui.progressBar_1.setMaximum(sweeper1_dataPoints)
        
        #prepare to write to file. 
        readerUnit = '' # the standatd SI unit we're writing the dataFile in. 
        if reader != None: 
            readerUnit = reader.standUnit()
        else:
            readerUnit = sweeper1_set.standUnit(reader = True) 
            
        #TODO: Fix for multiple number of sweeps
        indicies= [[] for i in xrange(3)] #calculate where the loops will start and end in the data.
        sweep1Len = (len(sweeper1[2])-(2+sweeper1_loop))
        sweep2Len = (len(sweeper2[2])-(2+sweeper2_loop))
        sweep3Len = (len(sweeper3[2])-(2+sweeper3_loop))
        indicies[2].append((0, sweep3Len*sweep2Len*sweep1Len-1))
        
        k = 0
        for i in xrange(sweep3Len):
            indicies[1].append((i*sweep2Len*sweep1Len, (i+1)*sweep2Len*sweep1Len-1))
            for j in xrange(sweep2Len):
                indicies[0].append((k*sweep1Len, (k+1)*sweep1Len-1))
                k+=1
                
        #TODO: Make a writeHeader function that writes the header on its own when prompted. 
        header = 'Initial States of Connected Instruments\n'+ '_'*15+'\n'
        for INST in self.INSTdict.itervalues():
            header += INST.getInitialState()
            header+= '\n' + '_'*15+ '\n'
            
        i = 1
        header += 'Indicies of Loops\n'
        for loop in indicies:
            header += '__Loop %i__\n'%i
            i+=1
            counter = 0
            for tup in loop:
                header += str(tup)
                counter +=1
                if counter%10 ==0:
                    header+='\n' #print a newline if there are more then ten in a row
            header+= '\n'
        header += '_'*15 + '\n'
        
        #write out the inital states of the objects and also write the header for the measurement. 
        tableHeader = '\n%s (%s)'%( sweeper1_set_name, sweeper1_standUnit) #out is the top for the table of data
        if reader!= None:
            header+='__READER__\n'
            header += reader.getState() # add special characters at the begining of each line
            header+= '\n' + '_'*15+ '\n'
            
        header+= '__SWEEP 1__\n'
        header += sweeper1_set.getState()
        header += 'Datapoints = %i StepSize = %f %s'%(sweeper1_dataPoints, sweeper1_stepSize, sweeper1_standUnit)
        header+= '\n' + '_'*15+ '\n'
        if sweeper2_set != None:
            tableHeader+='\t%s (%s)'%(sweeper2_set_name, sweeper2_standUnit)
            header += '__SWEEP 2__\n'
            header += sweeper2_set.getState()
            header += 'Datapoints = %i StepSize = %f %s'%(sweeper2_dataPoints, sweeper2_stepSize, sweeper2_standUnit)
            header+= '\n' + '_'*15+ '\n'
            if sweeper3_set != None:
                tableHeader+='\t%s (%s)'%(sweeper3_set_name, sweeper3_standUnit)
                header+='__SWEEP 3__\n'
                header += sweeper3_set.getState()
                header += 'Datapoints = %i StepSize = %f %s'%(sweeper3_dataPoints, sweeper3_stepSize, sweeper3_standUnit)
                header+= '\n' + '_'*15+ '\n'
                
        if reader is not None and reader.type == 'RT':
            tableHeader += '\t %s (%s)\t %s (DEG)'%(reader_name + 'R', readerUnit, reader_name + 'T')
        elif reader is not None:
            tableHeader+='\t %s (%s)'%(reader_name, readerUnit)#TODO: Fix for multiple data values. 
            
        if sweeper1_set.isGASPSD():
            tableHeader+='\t %s (%s)'%('SpecAnalyzerOut','Hz')
            
        headerLines = header.split('\n')
        
        header = '#' + '\n#'.join( headerLines) # insert the spcial initial character for the header lines
        
        with open(self.dataFilename, 'w') as dataFile:
            dataFile.write(header + tableHeader + '\n') 
            
        #header written: begin measurement 
            
        import thread
        import Measurement
        args = ( reader, sweeper1, sweeper2, sweeper3, self.emitter, self.__data__,self.check_abort , self.show_message)
        #TODO Comment these properly
        
        thread.start_new_thread(Measurement.main, args)
        
    def save_as_preset(self):
        #saves the current configuration as a preset.
        reader = str(self.ui.combo_read_1.currentText())
        
        sweep1_set = str(self.ui.combo_sweep1_1.currentText())
        sweep1_read = str(self.ui.combo_sweep1_2.currentText())
        sweep1_start = str(self.ui.edit_sweep1_start.text())
        sweep1_end = str(self.ui.edit_sweep1_end.text())
        sweep1_start_unit = str(self.ui.combo_sweep1_startUnit.currentText())
        sweep1_stepSize = str(self.ui.edit_sweep1_stepSize.text())
        sweep1_stepSize_unit = str(self.ui.combo_sweep1_stepSizeUnit.currentText())
        sweep1_dataPoints = str(self.ui.edit_sweep1_dataPoints.text())
        sweep1_loop = self.ui.check_sweep1_loop.isChecked()
        
        sweep2_set = str(self.ui.combo_sweep2_1.currentText())
        sweep2_read = str(self.ui.combo_sweep2_2.currentText())
        sweep2_start = str(self.ui.edit_sweep2_start.text())
        sweep2_end = str(self.ui.edit_sweep2_end.text())
        sweep2_start_unit = str(self.ui.combo_sweep2_startUnit.currentText())
        sweep2_stepSize = str(self.ui.edit_sweep2_stepSize.text())
        sweep2_stepSize_unit = str(self.ui.combo_sweep2_stepSizeUnit.currentText())
        sweep2_dataPoints = str(self.ui.edit_sweep2_dataPoints.text())
        sweep2_loop = self.ui.check_sweep2_loop.isChecked()
        
        sweep3_set = str(self.ui.combo_sweep3_1.currentText())
        sweep3_read = str(self.ui.combo_sweep3_2.currentText())
        sweep3_start = str(self.ui.edit_sweep3_start.text())
        sweep3_end = str(self.ui.edit_sweep3_end.text())
        sweep3_start_unit = str(self.ui.combo_sweep3_startUnit.currentText())
        sweep3_stepSize = str(self.ui.edit_sweep3_stepSize.text())
        sweep3_stepSize_unit = str(self.ui.combo_sweep3_stepSizeUnit.currentText())
        sweep3_dataPoints = str(self.ui.edit_sweep3_dataPoints.text())
        sweep3_loop = self.ui.check_sweep3_loop.isChecked()
        
        out = ''
        if reader != 'SpecAnalyzerOut':
            out += 'Reader = %s\n'%reader
            
        out += 'Sweep 1 = %s\n'%sweep1_set
        out += 'Sweep 1 Read = %s\n'%sweep1_read
        if sweep1_start and sweep1_end:
            out += 'Sweep 1 Range = (%s, %s) %s\n'%(sweep1_start, sweep1_end, sweep1_start_unit)
            if sweep1_stepSize:
                out+= 'Sweep 1 Step Size = %s %s\n'%(sweep1_stepSize, sweep1_stepSize_unit)
            if sweep1_dataPoints:
                out+='Sweep 1 Data Points = %s\n'%sweep1_dataPoints
        out+= 'Sweep 1 Loop = %s\n'%str(sweep1_loop)
            
        if sweep2_set != 'None':
            out += 'Sweep 2 = %s\n'%sweep2_set
            out += 'Sweep 2 Read = %s\n'%sweep2_read
            if sweep2_start and sweep2_end:
                out += 'Sweep 2 Range = (%s, %s) %s\n'%(sweep2_start, sweep2_end, sweep2_start_unit)
                if sweep2_stepSize:
                    out+= 'Sweep 2 Step Size = %s %s\n'%(sweep2_stepSize, sweep2_stepSize_unit)
                if sweep2_dataPoints:
                    out+='Sweep 2 Data Points = %s\n'%sweep2_dataPoints
            out += 'Sweep 2 Loop = %s\n'%str(sweep2_loop)
            
            if sweep3_set != 'None':
                out+= 'Sweep 3 = %s\n'%sweep3_set
                out+= 'Sweep 3 Read = %s\n'%sweep3_read
                if sweep3_start and sweep3_end:
                    out += 'Sweep 3 Range = (%s, %s) %s\n'%(sweep3_start, sweep3_end, sweep3_start_unit)
                    if sweep3_stepSize:
                        out+= 'Sweep 3 Step Size = %s %s\n'%(sweep3_stepSize, sweep3_stepSize_unit)
                    if sweep3_dataPoints:
                        out+='Sweep 3 Data Points = %s\n'%sweep3_dataPoints
                out+= 'Sweep 3 Loop = %s\n'%str(sweep3_loop)
                
        name, ok = QtGui.QInputDialog.getText(self, 'Preset Name', 'Enter the Name of the Preset')
        
        if not ok:
            return
        
        #check to see if this name is in the file already. If it is, overwrite it. 
        presetLines = []
        with open(self.PRESETFilename, 'r') as presetFile:
            for line in presetFile:
                presetLines.append(line)
        for line in presetLines:
            values = parseKeyValue(line)
            if values is not None and values[1] == name: #the name is in the file
                #this code is copied from deletePreset_main, it is the code to delete the preset
                lines = []
                with open(self.PRESETFilename, 'r') as presetFile:
                    for line in presetFile:
                        lines.append(line)
                
                outDel = ''
                    
                for i , line in enumerate(lines):
                    values = parseKeyValue(line)
                    if values is not None and values[0] == 'Name' and values[1] == name:#we've found the one to delete
                        while lines[i] != 'END\n': #skip the rest of it
                            i+=1
                    else:
                        outDel+=lines[i]
                        
                with  open(self.PRESETFilename, 'w') as presetFile:
                    presetFile.write(outDel)
                break
            
        
        out = '\nName = %s\n'%name + out + 'END\n'
        
        with open(self.PRESETFilename, 'a') as presetFile:
            presetFile.write(out)
        
    def set_microwave_amp(self):
        microwaveDict = {}
        for key, obj in self.GASdict.iteritems():
            if obj.className == 'setMicrowaveSource':
                microwaveDict[key] = obj
        
        import microwaveAmp_main
        self.microwaveWindow = microwaveAmp_main.Start(microwaveDict)
        self.microwaveWindow.show()
        
    def set_plot_axes(self):
        #set's the options for x, y and Z for the plots
        read = str(self.ui.combo_read_1.currentText())
        sweep1 = str(self.ui.combo_sweep1_1.currentText())
        sweep2 = str(self.ui.combo_sweep2_1.currentText())
        sweep3 = str(self.ui.combo_sweep3_1.currentText())
        data = [read]
        sets = [sweep1]
        if sweep2 != 'None':
            sets.append(sweep2)
        if sweep3 != 'None':
            sets.append(sweep3)
            
        if any(not item for item in sets+data): #it any are blank strings
            return
        if self.GASdict[sweep1].isGASPSD() and read != 'SpecAnalyzerOut':
            data.append('SpecAnalyzerOut')
            
        if read != 'SpecAnalyzerOut' and self.GASdict[read].type == 'RT':
            base = data.pop(0)
            data.extend([base + 'T', base+ 'R'])
            
        self.ui.combo_xAxis.clear()
        self.ui.combo_xAxis.addItems(sets)
        self.ui.combo_image_x.clear()
        self.ui.combo_image_y.clear()
        self.ui.combo_image_z.clear()
        self.ui.combo_image_x.addItems(sets)
        self.ui.combo_image_y.addItems(sets) # add all but the reader to the image plot. 
        self.ui.combo_image_y.setCurrentIndex(1)#tick over so both aren't automatically the same. 
        self.ui.combo_image_z.addItems(data)
    
    def set_read_1(self):
        #makes sure the only readers for this setter are valid pairings .
        #also turns looping on and off depending on the new topName
        self.ui.combo_sweep1_2.clear()
        self.ui.combo_sweep1_2.addItem('Set Point')
        topName = str(self.ui.combo_sweep1_1.currentText())
        if not topName:
            return
        topType = self.GASdict[topName].className
        
        for name, obj in self.GASdict.iteritems():
            attr = GASconfig.getGASattributes(self.GASFilename, name)
            if obj.isGetter(): #it's a getter
                if attr['Class Type'][3:] == topType[3:]: #This getter corresponds to the setter that we have selected.
                    self.ui.combo_sweep1_2.addItem(name)
            if topType == 'GASPSD' and obj.isNoiseSubtract():
                    self.ui.combo_sweep1_2.addItem(name)
                    
        if topType == 'GASPSD':
            self.ui.check_sweep1_loop.setEnabled(False)
            self.ui.check_sweep1_loop.setChecked(False)
            self.check_GAPSD()
            
        else:
            self.ui.check_sweep1_loop.setEnabled(True)

    def set_read_2(self):
        #makes sure the only readers for this setter are valid pairings .
        self.ui.combo_sweep2_2.clear()
        self.ui.combo_sweep2_2.addItem('Set Point')
        topName = str(self.ui.combo_sweep2_1.currentText())
        if topName == 'None' or topName == '':
            return
        topType = self.GASdict[topName].className
        for name in self.GASdict:
            if  not self.GASdict[name].isNoiseSubtract():
                attr = GASconfig.getGASattributes(self.GASFilename, name)
                if attr['Class Type'][:3] == 'get': #it's a getter
                    if attr['Class Type'][3:] == topType[3:]: #This getter corresponds to the setter that we have selected.
                        self.ui.combo_sweep2_2.addItem(name)

        if topType == 'GASPSD':
            self.ui.check_sweep2_loop.setEnabled(False)
        else:
            self.ui.check_sweep2_loop.setEnabled(True)

    def set_read_3(self):
        #makes sure the only readers for this setter are valid pairings .
        self.ui.combo_sweep3_2.clear()
        self.ui.combo_sweep3_2.addItem('Set Point')
        topName = str(self.ui.combo_sweep3_1.currentText())
        if topName == 'None' or topName == '':
            return
        topType = self.GASdict[topName].className
        import getAndSet
        for name in self.GASdict:
            if not self.GASdict[name].isNoiseSubtract():
                attr = GASconfig.getGASattributes(self.GASFilename, name)
                if attr[getAndSet.classType][:3] == 'get': #it's a getter
                    if attr[getAndSet.classType][3:] == topType[3:]: #This getter corresponds to the setter that we have selected.
                        self.ui.combo_sweep3_2.addItem(name)
                    
        if topType == 'GASPSD': #turn off loop for PSD measurements. 
            self.ui.check_sweep3_loop.setEnabled(False)
        else:
            self.ui.check_sweep3_loop.setEnabled(True)

    #this and the below methods set toolTipsf rfor the combo boxes
    def set_toolTip_read1(self):
        currentGAS = str(self.ui.combo_read_1.currentText())
        if not currentGAS or currentGAS == 'SpecAnalyzerOut':
            self.ui.combo_read_1.setToolTip('')
            return
        self.ui.combo_read_1.setToolTip(self.GASdict[currentGAS].comment)
    
    def set_toolTip_sweep11(self):
        currentGAS = str(self.ui.combo_sweep1_1.currentText())
        if not currentGAS:
            self.ui.combo_sweep1_1.setToolTip('')
            return
        self.ui.combo_sweep1_1.setToolTip(self.GASdict[currentGAS].comment)
            
    def set_toolTip_sweep12(self):
        currentGAS = str(self.ui.combo_sweep1_2.currentText())
        if not currentGAS or currentGAS == 'Set Point':
            self.ui.combo_sweep1_2.setToolTip('')
            return
        self.ui.combo_sweep1_2.setToolTip(self.GASdict[currentGAS].comment)
    
    def set_toolTip_sweep21(self):
        currentGAS = str(self.ui.combo_sweep2_1.currentText())
        if not currentGAS or currentGAS == 'None':
            self.ui.combo_sweep2_1.setToolTip('')
            return
        self.ui.combo_sweep2_1.setToolTip(self.GASdict[currentGAS].comment)
    
    def set_toolTip_sweep22(self):
        currentGAS = str(self.ui.combo_sweep2_2.currentText())
        if not currentGAS or currentGAS == 'Set Point':
            self.ui.combo_sweep2_2.setToolTip('')
            return
        self.ui.combo_sweep2_2.setToolTip(self.GASdict[currentGAS].comment)
    
    def set_toolTip_sweep31(self):
        currentGAS = str(self.ui.combo_sweep3_1.currentText())
        if not currentGAS or currentGAS == 'None':
            self.ui.combo_sweep3_1.setToolTip('')
            return
        self.ui.combo_sweep3_1.setToolTip(self.GASdict[currentGAS].comment)
    
    def set_toolTip_sweep32(self):
        currentGAS = str(self.ui.combo_sweep3_2.currentText())
        if not currentGAS or currentGAS == 'Set Point':
            self.ui.combo_sweep3_2.setToolTip('')
            return
        self.ui.combo_sweep3_2.setToolTip(self.GASdict[currentGAS].comment)

    def start_sweep_1(self):
        #this method turns on all the attributes of sweep 1 that are turned off until a file is opened. 
        self.ui.combo_sweep1_1.setEnabled(True)
        self.ui.combo_sweep1_2.setEnabled(True)
        self.ui.edit_sweep1_start.setEnabled(True)
        self.ui.edit_sweep1_end.setEnabled(True)
        self.ui.edit_sweep1_dataPoints.setEnabled(True)
        self.ui.edit_sweep1_stepSize.setEnabled(True)
        self.ui.check_sweep1_loop.setEnabled(True)
        self.ui.combo_sweep1_startUnit.setEnabled(True)
        self.ui.combo_sweep1_endUnit.setEnabled(True)
        self.ui.combo_sweep1_stepSizeUnit.setEnabled(True)
        self.ui.combo_sweep2_1.setEnabled(True)
        self.ui.action_Calibrate_B_Field.setEnabled(True)
        self.ui.action_Get_Background_Subtract.setEnabled(True)
        self.ui.combo_plotType.setEnabled(True)
        self.ui.button_refresh_plot.setEnabled(True)
        self.change_plotType() # turn on the first plot Type
        self.set_read_1()
        
        self.ui.action_Calibrate_B_Field.setEnabled(True)
        self.ui.action_Get_Background_Subtract.setEnabled(True)
        
    def set_units_1(self):
        #this, and the 3 copies below, set the Units when the getter or setter is changed. 
        name = str(self.ui.combo_sweep1_1.currentText())
        
        import operator #this changes the dict ot a sorted list of tuples, so we can have them ordered. 
        unitDict = self.GASdict[name].unitDictionary
        sortedUnitDict = sorted(unitDict.iteritems(), key = operator.itemgetter(1))
        units = [tup[0] for tup in sortedUnitDict]
        
        self.ui.combo_sweep1_startUnit.clear()
        self.ui.combo_sweep1_startUnit.addItems(units)
        self.ui.combo_sweep1_endUnit.clear()
        self.ui.combo_sweep1_endUnit.addItems(units)
        self.ui.combo_sweep1_stepSizeUnit.clear()
        self.ui.combo_sweep1_stepSizeUnit.addItems(units)
        self.ui.combo_slice1.clear()
        self.ui.combo_slice1.addItems(units)
        
        standUnit = self.GASdict[name].standUnit()
        i = self.ui.combo_sweep1_startUnit.findText(standUnit)
            
        self.ui.combo_sweep1_startUnit.setCurrentIndex(i)
        self.ui.combo_sweep1_endUnit.setCurrentIndex(i)
        self.ui.combo_sweep1_stepSizeUnit.setCurrentIndex(i)
        
    def set_units_2(self):
        name = str(self.ui.combo_sweep2_1.currentText())
        if name== 'None' or name == '':
            return
        
        import operator #this changes the dict ot a sorted list of tuples, so we can have them ordered. 
        unitDict = self.GASdict[name].unitDictionary
        sortedUnitDict = sorted(unitDict.iteritems(), key = operator.itemgetter(1))
        units = [tup[0] for tup in sortedUnitDict]
            
        self.ui.combo_sweep2_startUnit.clear()
        self.ui.combo_sweep2_startUnit.addItems(units)
        self.ui.combo_sweep2_endUnit.clear()
        self.ui.combo_sweep2_endUnit.addItems(units)
        self.ui.combo_sweep2_stepSizeUnit.clear()
        self.ui.combo_sweep2_stepSizeUnit.addItems(units)
        self.ui.combo_slice2.clear()
        self.ui.combo_slice2.addItems(units)
        
        standUnit = self.GASdict[name].standUnit()
        i = self.ui.combo_sweep2_startUnit.findText(standUnit)
            
        self.ui.combo_sweep2_startUnit.setCurrentIndex(i)
        self.ui.combo_sweep2_endUnit.setCurrentIndex(i)
        self.ui.combo_sweep2_stepSizeUnit.setCurrentIndex(i)
        
    def set_units_3(self):
        name = str(self.ui.combo_sweep3_1.currentText())
        if name== 'None' or name== '':
            return

        import operator #this changes the dict ot a sorted list of tuples, so we can have them ordered. 
        unitDict = self.GASdict[name].unitDictionary
        sortedUnitDict = sorted(unitDict.iteritems(), key = operator.itemgetter(1))
        units = [tup[0] for tup in sortedUnitDict]
            
        self.ui.combo_sweep3_startUnit.clear()
        self.ui.combo_sweep3_startUnit.addItems(units)
        self.ui.combo_sweep3_endUnit.clear()
        self.ui.combo_sweep3_endUnit.addItems(units)
        self.ui.combo_sweep3_stepSizeUnit.clear()
        self.ui.combo_sweep3_stepSizeUnit.addItems(units)
        self.ui.combo_slice3.clear()
        self.ui.combo_slice3.addItems(units)
        
        standUnit = self.GASdict[name].standUnit()
        i = self.ui.combo_sweep3_startUnit.findText(standUnit)
            
        self.ui.combo_sweep3_startUnit.setCurrentIndex(i)
        self.ui.combo_sweep3_endUnit.setCurrentIndex(i)
        self.ui.combo_sweep3_stepSizeUnit.setCurrentIndex(i)

    def show_message(self, message):
        #displays a message on the status bar. used to call in another thread
        self.ui.statusbar.showMessage(message)

    def update_GAS_INST(self):
        #ask the parent window to update everyone with the new instrument configurations
        if self.parent is not None:
            self.parent.update_GAS_INST()

    def write_data(self):
        #write the newly acquired data to file. 
        self.__data__.write()
    
    def write_dataPoints_1(self):
        name = str(self.ui.combo_sweep1_1.currentText())
        start = str(self.ui.edit_sweep1_start.text())
        end = str(self.ui.edit_sweep1_end.text())
        stepSize = str(self.ui.edit_sweep1_stepSize.text())
        self.ui.edit_sweep1_dataPoints.clear()
        try:
            start = float(start)
            end = float(end) #make sure we can turn them to floats properly
            stepSize = float(stepSize)
            if stepSize==0:
                raise ZeroDivisionError # we don't want to divide by 0 later. 
        except:
            return# just exit; the user could be in the middle of something.
        startUnit = str(self.ui.combo_sweep1_startUnit.currentText())
        stepSizeUnit = str(self.ui.combo_sweep1_stepSizeUnit.currentText())
        if stepSizeUnit == '':
            return 
        #convert all them to SI for internal calculations
        if not name or not startUnit:
            return #in between cycles.
        startSI = start*self.GASdict[name].unitDictionary[startUnit]
        endSI = end*self.GASdict[name].unitDictionary[startUnit]
        try:
            stepSizeSI = stepSize*self.GASdict[name].unitDictionary[stepSizeUnit]#we get the ratio between the units, in case they are different. 
        except KeyError:
            #sometimes the wrong unit is passed in
            return
        dataPoints = int(round(abs(endSI-startSI)/stepSizeSI))
        dataPoints += 1 #there is an extra to include the endpoint
        if self.ui.check_sweep1_loop.isChecked():
            dataPoints*=2 # we'll have twice as many points if we loop through. 
            
        if self.GASdict[name].isGASPSD():#there are only some valid datapoint amounts for the GASPSD. This rounds up.
            if dataPoints not in self.GASdict[name].LIRef.validSweepPoints:
                for item in self.GASdict[name].LIRef.validSweepPoints:
                    if dataPoints<=item:
                        dataPoints = item #round up to the first item that is larger
                        break
                else:#go for the biggest if the user goes over. 
                    dataPoints = self.GASdict[name].LIRef.validSweepPoints[-1]
                self.ui.edit_sweep1_dataPoints.setText('%i'%dataPoints)
                self.write_stepSize_1()#we need to write a new stepsize. this will in turn call this method again, but it will exit below.
                
            
        self.ui.edit_sweep1_dataPoints.setText('%i'%dataPoints)
        
    def write_dataPoints_2(self):
        name = str(self.ui.combo_sweep2_1.currentText())
        start = str(self.ui.edit_sweep2_start.text())
        end = str(self.ui.edit_sweep2_end.text())
        stepSize = str(self.ui.edit_sweep2_stepSize.text())
        self.ui.edit_sweep2_dataPoints.clear()
        try:
            start = float(start)
            end = float(end) #make sure we can turn them to floats properly
            stepSize = float(stepSize)
            if stepSize==0:
                raise ZeroDivisionError # we don't want to divide by 0 later. 
        except:
            return# just exit; the user could be in the middle of something.
        startUnit = str(self.ui.combo_sweep2_startUnit.currentText())
        stepSizeUnit = str(self.ui.combo_sweep2_stepSizeUnit.currentText())
        if stepSizeUnit == '':
            return 
        #convert all them to SI for internal calculations
        startSI = start*self.GASdict[name].unitDictionary[startUnit]
        endSI = end*self.GASdict[name].unitDictionary[startUnit]
        try:
            stepSizeSI = stepSize*self.GASdict[name].unitDictionary[stepSizeUnit]#we get the ratio between the units, in case they are different. 
        except KeyError:
            #sometimes the wrong unit is passed in
            return
        dataPoints = int(round(abs(endSI-startSI)/stepSizeSI))
        dataPoints += 1 #there is an extra to include the endpoint
        if self.ui.check_sweep2_loop.isChecked():
            dataPoints*=2 # we'll have twice as many points if we loop through. 
            
        if self.GASdict[name].isGASPSD():#there are only some valid datapoint amounts for the GASPSD. This rounds up.
            if dataPoints not in self.GASdict[name].LIRef.validSweepPoints:
                for item in self.GASdict[name].LIRef.validSweepPoints:
                    if dataPoints<item:
                        dataPoints = item #round up to the first item that is larger
                        break
                else:#go for the biggest if the user goes over. 
                    dataPoints = self.GASdict[name].LIRef.validSweepPoints[-1]
                self.ui.edit_sweep2_dataPoints.setText('%i'%dataPoints)
                self.write_stepSize_2()#we need to write a new stepsize. this will in turn call this method again, but it will exit below.
                
            
        self.ui.edit_sweep2_dataPoints.setText('%i'%dataPoints)
            
    def write_dataPoints_3(self):
        name = str(self.ui.combo_sweep3_1.currentText())
        start = str(self.ui.edit_sweep3_start.text())
        end = str(self.ui.edit_sweep3_end.text())
        stepSize = str(self.ui.edit_sweep3_stepSize.text())
        self.ui.edit_sweep3_dataPoints.clear()
        try:
            start = float(start)
            end = float(end) #make sure we can turn them to floats properly
            stepSize = float(stepSize)
            if stepSize==0:
                raise ZeroDivisionError # we don't want to divide by 0 later. 
        except:
            return# just exit; the user could be in the middle of something.
        startUnit = str(self.ui.combo_sweep3_startUnit.currentText())
        stepSizeUnit = str(self.ui.combo_sweep3_stepSizeUnit.currentText())
        if stepSizeUnit == '':
            return 
        #convert all them to SI for internal calculations
        startSI = start*self.GASdict[name].unitDictionary[startUnit]
        endSI = end*self.GASdict[name].unitDictionary[startUnit]
        try:
            stepSizeSI = stepSize*self.GASdict[name].unitDictionary[stepSizeUnit]#we get the ratio between the units, in case they are different. 
        except KeyError:
            #sometimes the wrong unit is passed in
            return
        dataPoints = int(round(abs(endSI-startSI)/stepSizeSI))
        dataPoints += 1 #there is an extra to include the endpoint
        if self.ui.check_sweep3_loop.isChecked():
            dataPoints*=2 # we'll have twice as many points if we loop through. 
            
        if self.GASdict[name].isGASPSD():#there are only some valid datapoint amounts for the GASPSD. This rounds up.
            if dataPoints not in self.GASdict[name].LIRef.validSweepPoints:
                for item in self.GASdict[name].LIRef.validSweepPoints:
                    if dataPoints<item:
                        dataPoints = item #round up to the first item that is larger
                        break
                else:#go for the biggest if the user goes over. 
                    dataPoints = self.GASdict[name].LIRef.validSweepPoints[-1]
                self.ui.edit_sweep3_dataPoints.setText('%i'%dataPoints)
                self.write_stepSize_3()#we need to write a new stepsize. this will in turn call this method again, but it will exit below.
                
            
        self.ui.edit_sweep3_dataPoints.setText('%i'%dataPoints)

    def write_stepSize_1(self):
        name = str(self.ui.combo_sweep1_1.currentText())
        start = str(self.ui.edit_sweep1_start.text())
        end = str(self.ui.edit_sweep1_end.text())
        dataPoints = str(self.ui.edit_sweep1_dataPoints.text())
        
        self.ui.edit_sweep1_stepSize.clear()
        try: #ensure that they can all be turned into numbers properly.
            start = float(start)
            end = float(end)
            dataPoints = int(dataPoints)
            if dataPoints ==0:
                raise ZeroDivisionError # we'll end up dividing here anyway
        except:
            return #just exit; the user could be in the middle of something. 
        
        if self.ui.check_sweep1_loop.isChecked() and dataPoints%2 != 0: # a loop needs an even number of datapoints
            dataPoints+=1
            self.ui.edit_sweep1_dataPoints.setText('%i'%dataPoints)
        
        if self.GASdict[name].isGASPSD():#there are only some valid datapoint amounts for the GASPSD. This rounds up.
            if dataPoints not in self.GASdict[name].LIRef.validSweepPoints:
                for item in self.GASdict[name].LIRef.validSweepPoints:
                    if dataPoints<=item:
                        dataPoints = item #round up to the first item that is larger
                        break
                else:#go for the biggest if the user goes over. 
                    dataPoints = self.GASdict[name].LIRef.validSweepPoints[-1]
                self.ui.edit_sweep1_dataPoints.setText('%i'%dataPoints)
        
        if self.ui.check_sweep1_loop.isChecked():
            dataPoints*=.5
        
        dataPoints-=1 # take off the end point. 
            
        startUnit = str(self.ui.combo_sweep1_startUnit.currentText())
        stepSizeUnit = str(self.ui.combo_sweep1_stepSizeUnit.currentText())
        
        startSI = start*self.GASdict[name].unitDictionary[startUnit]
        endSI = end*self.GASdict[name].unitDictionary[startUnit]#convert internally to SI units
        
        stepSizeSI = abs(endSI-startSI)/dataPoints
        stepSize = stepSizeSI/self.GASdict[name].unitDictionary[stepSizeUnit] #convert back to the units we want. 
        
        self.ui.edit_sweep1_stepSize.setText(str(stepSize))

    def write_stepSize_2(self):
        name = str(self.ui.combo_sweep2_1.currentText())
        start = str(self.ui.edit_sweep2_start.text())
        end = str(self.ui.edit_sweep2_end.text())
        dataPoints = str(self.ui.edit_sweep2_dataPoints.text())
        
        self.ui.edit_sweep2_stepSize.clear()
        try: #ensure that they can all be turned into numbers properly.
            start = float(start)
            end = float(end)
            dataPoints = int(dataPoints)
            if dataPoints ==0:
                raise ZeroDivisionError # we'll end up dividing here anyway
        except:
            return #just exit; the user could be in the middle of something. 
        
        if self.ui.check_sweep2_loop.isChecked() and dataPoints%2 != 0: # a loop needs an even number of datapoints
            dataPoints+=1
            self.ui.edit_sweep2_dataPoints.setText('%i'%dataPoints)
        
        if self.GASdict[name].isGASPSD():#there are only some valid datapoint amounts for the GASPSD. This rounds up.
            if dataPoints not in self.GASdict[name].LIRef.validSweepPoints:
                for item in self.GASdict[name].LIRef.validSweepPoints:
                    if dataPoints<item:
                        dataPoints = item #round up to the first item that is larger
                        break
                else:#go for the biggest if the user goes over. 
                    dataPoints = self.GASdict[name].LIRef.validSweepPoints[-1]
                self.ui.edit_sweep2_dataPoints.setText('%i'%dataPoints)
        
        if self.ui.check_sweep2_loop.isChecked():
            dataPoints*=.5
        
        dataPoints-=1 # take off the end point. 
            
        startUnit = str(self.ui.combo_sweep2_startUnit.currentText())
        stepSizeUnit = str(self.ui.combo_sweep2_stepSizeUnit.currentText())
        
        startSI = start*self.GASdict[name].unitDictionary[startUnit]
        endSI = end*self.GASdict[name].unitDictionary[startUnit]#convert internally to SI units
        
        stepSizeSI = abs(endSI-startSI)/dataPoints
        stepSize = stepSizeSI/self.GASdict[name].unitDictionary[stepSizeUnit] #convert back to the units we want. 
        
        self.ui.edit_sweep2_stepSize.setText(str(stepSize))
        
    def write_stepSize_3(self):
        name = str(self.ui.combo_sweep3_1.currentText())
        start = str(self.ui.edit_sweep3_start.text())
        end = str(self.ui.edit_sweep3_end.text())
        dataPoints = str(self.ui.edit_sweep3_dataPoints.text())
        
        self.ui.edit_sweep3_stepSize.clear()
        try: #ensure that they can all be turned into numbers properly.
            start = float(start)
            end = float(end)
            dataPoints = int(dataPoints)
            if dataPoints ==0:
                raise ZeroDivisionError # we'll end up dividing here anyway
        except:
            return #just exit; the user could be in the middle of something. 
        
        if self.ui.check_sweep3_loop.isChecked() and dataPoints%2 != 0: # a loop needs an even number of datapoints
            dataPoints+=1
            self.ui.edit_sweep3_dataPoints.setText('%i'%dataPoints)
        
        if self.GASdict[name].isGASPSD():#there are only some valid datapoint amounts for the GASPSD. This rounds up.
            if dataPoints not in self.GASdict[name].LIRef.validSweepPoints:
                for item in self.GASdict[name].LIRef.validSweepPoints:
                    if dataPoints<item:
                        dataPoints = item #round up to the first item that is larger
                        break
                else:#go for the biggest if the user goes over. 
                    dataPoints = self.GASdict[name].LIRef.validSweepPoints[-1]
                self.ui.edit_sweep3_dataPoints.setText('%i'%dataPoints)
        
        if self.ui.check_sweep3_loop.isChecked():
            dataPoints*=.5
        
        dataPoints-=1 # take off the end point. 
            
        startUnit = str(self.ui.combo_sweep3_startUnit.currentText())
        stepSizeUnit = str(self.ui.combo_sweep3_stepSizeUnit.currentText())
        
        startSI = start*self.GASdict[name].unitDictionary[startUnit]
        endSI = end*self.GASdict[name].unitDictionary[startUnit]#convert internally to SI units
        
        stepSizeSI = abs(endSI-startSI)/dataPoints
        stepSize = stepSizeSI/self.GASdict[name].unitDictionary[stepSizeUnit] #convert back to the units we want. 
        
        self.ui.edit_sweep3_stepSize.setText(str(stepSize))        
            
def main():
    
    import os

    def parseKeyValue(line):
        # a funciton that will take a line and split it along the equals sign and make a tuple
        splitLine = line.split('=')
        if len(splitLine) != 2:
            return None #if the length is not 2, this line may be blank, or not have a key value
        return (splitLine[0].strip(), splitLine[1].strip())
    
    compName = os.environ['COMPUTERNAME']
    lines = []
    master_config = open('config&data\master_config.txt', 'r')
    
    for line in master_config:
        lines.append(line)
        
    master_config.close()
    
    fileDict = {}
    
    for index in xrange(len(lines)):
        tup = parseKeyValue(lines[index])
        if tup is not None and tup[1] == compName: #found our computer
            for i in xrange(index + 1, index + 4):
                tup = parseKeyValue(lines[i])
                if tup is not None:
                    fileDict[tup[0]] = tup[1] #add the file type and name into the dicitonary.
            break
        
    from pyvisa import visa_exceptions
    import GASconfig
    try:
        GASdict, INSTdict = GASconfig.getsAndSetsFromConfig(fileDict['GAS'])
    except visa_exceptions.VisaIOError:
        return
    
    app = QtGui.QApplication(sys.argv)
    ex = Start(fileDict,'lockinVoltage', GASdict, INSTdict)
    ex.showMaximized()
    sys.exit(app.exec_())
    
if __name__== '__main__':
    main()