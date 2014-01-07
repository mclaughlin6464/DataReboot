'''
7/19/2013
Sean McLaughlin
This is the companion file to the auto-generated noiseSubtract.py. It opens a small window which allows the user to take a background spectrum to subtract off from the 
spectrum analyzer measurement. 
'''

import sys
from PyQt4 import QtGui, QtCore
from noiseSubtract import Ui_noiseSubtract

class Start(QtGui.QWidget):
    
    class noiseSubtractException(Exception):
    # will be raised if there is a problem in this window. 
        
        def __init__(self, value = None):
            self.value = value
            
        def __str__(self):
            if self.value != None:
                return str(self.value)
            return 'There was a problem taking the background spectrum.'
    
    def __init__(self, NSobjsDict, emitter, args, parent = None):
        super(Start, self).__init__()
        self.ui = Ui_noiseSubtract()
        self.ui.setupUi(self)
            
        self.NSobsDict = NSobjsDict # a dictionary of the available noise subtract objects that are configured. 
        if not self.NSobsDict: #if there are none:
            raise self.noiseSubtractException, 'There are no noise subtracts configured.'
        
        self.emitter = emitter
        
        self.ui.combo_noiseSubtractObj.addItems(self.NSobsDict.keys())
        
        self.unitDict ={'Hz': 1 , 'GHz': 1e9, 'MHz': 1e6, 'KHz' : 1e3} # same units for all of em
        self.validSweepPoints = [125,251,501,1001, 2001,4001, 8001]
        
        self.ui.combo_startUnit.addItems(self.unitDict.keys())
        self.ui.combo_stopUnit.addItems(self.unitDict.keys())
        self.ui.combo_stepSize.addItems(self.unitDict.keys())
        
        index = self.ui.combo_startUnit.findText('GHz')
        self.ui.combo_startUnit.setCurrentIndex(index)
        self.ui.combo_stepSize.setCurrentIndex(index)
        
        #inset what's currently in the spectrum 
        self.ui.edit_start.insert(str(args[0]))
        self.ui.edit_stop.insert(str(args[1]))
        self.ui.edit_points.insert(str(args[2]))
        self.ui.edit_stepSize.insert(str(args[3]))
        self.check_takeSpectrum()
        
        #the signals and slots
        self.ui.button_takeSpectrum.clicked.connect(self.takeSpectrum)
        
        self.ui.edit_points.textChanged.connect(self.check_takeSpectrum)
        self.ui.edit_start.textChanged.connect(self.check_takeSpectrum)
        self.ui.edit_stepSize.textChanged.connect(self.check_takeSpectrum)
        self.ui.edit_stop.textChanged.connect(self.check_takeSpectrum)
        
        self.ui.edit_stepSize.editingFinished.connect(self.write_points)
        self.ui.edit_points.editingFinished.connect(self.write_stepSize)
        
    def check_takeSpectrum(self):
        start = str(self.ui.edit_start.text())
        stop = str(self.ui.edit_stop.text())
        points = str(self.ui.edit_points.text())
        stepSize = str(self.ui.edit_stepSize.text())
        try:
            start = float(start)
            stop = float(stop)
            points = int(points)
            stepSize = float(stepSize)
            
            if stepSize == 0 or points == 0 or start-stop == 0:
                raise ValueError
        except ValueError:
            self.ui.button_takeSpectrum.setEnabled(False)
            return #the inputs are not valid
        self.ui.button_takeSpectrum.setEnabled(True)
        
    def takeSpectrum(self):
        NSobjName = str(self.ui.combo_noiseSubtractObj.currentText())
        NSobj = self.NSobsDict[NSobjName]
        
        start = float(self.ui.edit_start.text())
        stop = float(self.ui.edit_stop.text())
        points = int(self.ui.edit_points.text())
        
        startUnit = str(self.ui.combo_startUnit.currentText())
        start = start*self.unitDict[startUnit]
        stop = stop*self.unitDict[startUnit]
    
        NSobj.set(start, stop, points)
        self.emitter('Check Run')  # turn on the run button in the main window after this has been run. 
        self.emitter('Plot Noise') #plots the noise on the screen
        self.close()
    
    def write_points(self):
        #write the number of points when the step size is changed.
        start = str(self.ui.edit_start.text())
        stop = str(self.ui.edit_stop.text())
        stepSize = str(self.ui.edit_stepSize.text())
        
        try:
            start = float(start)
            stop = float(stop)
            stepSize = float(stepSize)
            
            if stepSize == 0 or start-stop == 0:
                raise ValueError
        except ValueError:
            self.ui.edit_points.clear()
            return #the inputs are not valid
        startUnit = str(self.ui.combo_startUnit.currentText())
        stepSizeUnit = str(self.ui.combo_stepSize.currentText())
        
        start = start*self.unitDict[startUnit]
        stop = stop*self.unitDict[startUnit]
        stepSize = stepSize*self.unitDict[stepSizeUnit]
        
        points = int(abs(stop-start)/stepSize)
        points +=  1 # add the endpoint

        if points not in self.validSweepPoints:# the spectrum analyzer only takes certain point sizes. 
            for point in self.validSweepPoints:
                if points<point:
                    points = point # round up
                    break
            else:
                points = self.validSweepPoints[-1] # it we're too big go with the last one.
                
            newStepSize = float(abs(stop-start)/points)
            self.ui.edit_stepSize.clear()
            self.ui.edit_stepSize.insert(str(newStepSize))
            
        self.ui.edit_points.clear()
        self.ui.edit_points.insert(str(points))
        
    def write_stepSize(self):
        #write the stepSize when the data Points are changed. 
        start = str(self.ui.edit_start.text())
        stop = str(self.ui.edit_stop.text())
        points = str(self.ui.edit_points.text())
        try:
            start = float(start)
            stop = float(stop)
            points = int(points)
            
            if points == 0 or start-stop == 0:
                raise ValueError
        except ValueError:
            self.ui.edit_stepSize.clear()
            return #the inputs are not valid
        
        if points not in self.validSweepPoints:# the spectrum analyzer only takes certain point sizes. 
            for point in self.validSweepPoints:
                if points<point:
                    points = point # round up
                    break
            else:
                points = self.validSweepPoints[-1] # it we're too big go with the last one.
            self.ui.edit_points.clear()
            self.ui.edit_points.insert(str(points))
        
        points -= 1 #take off the endpoint
            
        startUnit = str(self.ui.combo_startUnit.currentText())
        stepSizeUnit = str(self.ui.combo_stepSize.currentText())
        
        start = start*self.unitDict[startUnit]
        stop = stop*self.unitDict[startUnit]
        stepSize = abs(stop-start)/points
        
        stepSize = stepSize/self.unitDict[stepSizeUnit]
        
        self.ui.edit_stepSize.clear()
        self.ui.edit_stepSize.insert(str(stepSize))
        