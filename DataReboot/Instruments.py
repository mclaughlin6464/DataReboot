'''
Created on Jun 11, 2013

@author: swm2
This module contains the objects for all the instruments. 
'''
if __name__ == '__main__':
    print '''This module contains abstract objects for each of the lab instruments. There is a distinct hierarchy to the inheritance of this module. 
The main class is labInstrument, which is a subclass of visa.Instrument, which allows writing and reading GPIB commands to an instrument.
The LabInstrument class contains a few general methods and a standard constructor. It also contains an error message to raise when there is a LabInstrumentError.
LabInstrument is subclassed by a few classes, which represent the kind of instrument (LockIn, HallProbe, etc.). These contain most of the main functionality of the 
instruments. These are subclasses by the useable objects, which differ by model name and number. These account for small changes in makes and models of equipment.
This module also contains the dictionary which matches the type of an instrument to it's object name. It is used in the config files and a few other places. 
IT IS IMPERITIVE THAT IF A NEW INSTRUMENT IS ADDED TO THIS MODULE THAT ITS NAME IS ALSO ADDED TO THE DICTIONARY.
'''
try:
    from pyvisa import visa
    from time import sleep
except ImportError:
    print "There was a problem with importing visa. Please check the PYTHONPATH."
else:
    
    class LabInstrument(visa.Instrument):
    #This class is the general subclass. It will contain all functions common to all instruments. 
        noInstruments = 0 #this is not used in any present code. However, keeping a count of the active instruments is not a bad thing. 
        
        def __init__(self, resAd): #takes resource address as an initial parameter
            super(LabInstrument, self).__init__(resAd)
            #self.clear()
            
            #The below code is duplicated in Gauesmeter425.
            #python doesn't initialzie it the way I'd like to I just copied it down. 
            self.address = resAd 
            self.ID = self.ask("*IDN?") #the instrument's Unique ID. Could be useful so I'll store it. 
            self.type = "LabInstrument"
            # A string that tells what type of instrument it is; overwritten in the subclasses. May be best as a class variable rather than an isntance.  
            self.validGetsAndSets = []
            from getAndSet import GASdictionary
            from copy import deepcopy
            self.validMeasurementTypes = GASdictionary.fromkeys(GASdictionary, deepcopy([]))
            #this dict will be initially entirely empty.
            #It will be modified in the subclasses, saying what getAndSet's the instrument can be used as. 
            self.labID = LabInstrument.noInstruments+1 # a number of how many instruments there are and each is numbered
            LabInstrument.noInstruments+=1
            
        def __str__(self):
            return "Type = %s\nResource Address = %s\nID = %s\nEND\n\n"%(self.type,self.address, self.ID)
        
        def busy(self): #This should work for seeing if a function is doing something else or not. 
            try:
                self.ask('*STB? 1')
                return False
            except:
                return True
    
        def clear(self): #This function will read any stray inputs, and handle them if there is a timeout. This takes a few seconds. 
        #It's conceivable that there is a command that does this function, but I can't find a universal one. 
            try:
                a =self.ask('*STB? 4')
                if a=='1':
                    self.read()
            except:
                pass
    
        def getInitialState(self):
            return str(self)[:-5] #overwritten in subclasses
        #the -5 removes the END\n\n
        
        def release(self):
            pass #some instruments lock out local access to the front panel. With this, I can return control to the user. 
    
        class LabInstrumentError(Exception): # an exception for the Instrument to throw if there are problems. 
            
            def __init__(self, value= None):
                self.value = value

            def __str__(self):
                if self.value!= None:
                    return str(self.value)
                return "There was a problem with the %s"%self.type
    
    class HallProbe(LabInstrument):
    #subclass for the Hall Probe
        def __init__(self, resAd):
            super(HallProbe, self).__init__(resAd)
            self.type = "Hall Probe"
            self.bUnits = {'G':1, 'T':2, 'Oe':3, 'A/m':4}
            self.tUnits = {'C':1, 'K':2}
            self.validGetsAndSets.append('getBField')
            
            self.write('AUTO 0') # turn off autorange. 
            
        def getBField(self):
        #returns the B-field as a floating point number in the units set by setBUnit
            return float(self.ask("RDGREL?"))
            
        def getBUnit(self):
            units = self.bUnits.keys()
            return units[int(self.ask('UNIT?'))] # there may be a problem here with the dictionaries being unordered. For now though, it works. 
            
        def getInitialState(self):
            unit = self.getBUnit()
            field = self.getBField()
            out = 'Initial Field = %f %s'%(field, unit)
            return str(self)[:-5]+ out
            
        def release(self):
            #returns the isntrument to local control
            self.write('MODE 0')
             
        def setBUnit(self, unitStr):
            #takes a unit G,T, O or A/m
            if unitStr in self.bUnits:
                unit = self.bUnits[unitStr]
                self.write('UNIT %i'%unit)
                
        def zeroProbe(self): 
            self.write("ZPROBE") 
            sleep(30)
            
    class Gaussmeter455(HallProbe):
        #this class exists for completeness' sake. All of it's functionality is taken care of in the Hall Probe class
        def __init__(self, resAd):
            super(Gaussmeter455, self).__init__(resAd)
            self.type = "Gaussmeter 455"

        def setTUnit(self, unitStr):
            #takes either 'C' or 'T'
            if unitStr in self.tUnits.keys():
                unit = self.tUnits[unitStr]
                self.write('UNIT %f'%unit)
                
        def getTemp(self):
        #returns the temperature as a floating point number in the units set by setTUnit.
            return float(self.ask("RDGTEMP?"))
            
        def getTUnit(self):
            units = self.tUnits.keys()
            return units[int(self.ask('TUNIT?'))-1]
             
            
    class Gaussmeter450(HallProbe):
        #this class exists for completeness' sake. All of it's functionality is taken care of in the Hall Probe class
        def __init__(self, resAd):
            super(Gaussmeter450, self).__init__(resAd)
            self.type = "Gaussmeter 450"
            
        def getBField(self):
        #returns the B-field as a floating point number in the units set by setBUnit
            return float(self.ask("FIELD?"))
            
        def getBUnit(self):
            units = self.bUnits.keys()
            return self.ask('UNIT?') # there may be a problem here with the dictionaries being unordered. For now though, it works. 
            
        def setBUnit(self, unitStr):
            #takes a unit G,T, O or A/m
            # might need a little error checking - 450/460 only accept G or T as unit, but use string not number
            if unitStr in self.bUnits.keys():
                unit = self.bUnits[unitStr]
                self.write('UNIT %s'%unitStr)


    class Gaussmeter425(visa.SerialInstrument, HallProbe):
        #this gauss probe requires special intialization, because it is a virtual serial instrument. All other functionality is in Hall Probe
        #most of the initialization done in the superclasses must be redone here
        def __init__(self, resAd):
            super(Gaussmeter425, self).__init__(resAd, baud_rate = 57600, data_bits = 7, parity = 1, stop_bits = 1, term_chars = '\r\n')
            self.type = 'Gaussmeter 425'
            #this code is copied from the LabInstrument __init__ method. 
            #When doing the multiple inheritance, python only calls serial instrument, and cannot call HallProbe without causing trouble. 
            self.address = resAd 
            self.ID = self.ask("*IDN?") #the instrument's Unique ID. Could be useful so I'll store it. 
            self.labID = LabInstrument.noInstruments+1 # a number of how many instruments there are and each is numbered
            LabInstrument.noInstruments+=1
            self.validGetsAndSets = []
            
            self.validGetsAndSets.append('getBField')
            self.bUnits = {'G':1, 'T':2, 'Oe':3, 'A/m':4}
            self.tUnits = {'C':1, 'K':2}
            
            self.write('AUTO 0') # turn off autorange. 
        
            
            from GASconfig import GASdictionary
            from copy import deepcopy
            self.validMeasurementTypes = GASdictionary.fromkeys(GASdictionary, deepcopy([]))
            
    class LockIn(LabInstrument):
        
        def __init__(self, resAd):
            super(LockIn, self).__init__(resAd)
            self.type = "Lock-in Amplifier"
            self.sensitivityConstants = ['2 nV/fA','5 nV/fA','10 nV/fA','20 nV/fA','50 nV/fA','100 nV/fA', '200 nV/fA','500 nV/fA','1 uV/pA','2 uV/pA','5 uV/pA','10 uV/pA','20 uV/pA',
                         '50 uV/pA','100 uV/pA','200 uV/pA','500 uV/pA','1 mV/nA','2 mV/nA','5 mV/nA','10 mV/nA','20 mV/nA','50 mV/nA','100 mV/nA','200 mV/nA','500 mV/nA','1 V/uA' ]
            #The above are all the possible settings for the sensitivity. To set the sensitivity, write the index of the proper setting to the lockin.
            self.timeConstants = [1e-5,3e-5,1e-4,3e-4,1e-3,3e-3,1e-2,3e-2 ,1e-1 ,3e-1 ,1 ,3 ,10 ,30 ,100 ,300 ,1e3,3e3,10e3,30e3]
            
            temp = ['setVoltage','getVoltage','setBField','getBField', 'getCurrent', 'setCurrent', 'getResistance']
            self.validGetsAndSets.extend(temp)
            
            self.nVSteps = 15 # in the rampV function, how many steps to take to go to a large voltage change. 
            self.vLimit = .05 #also in rampV, the voltage difference over which to step the voltage rather than set it directly. 
            
            #below is a dictionary that matches validGAS's to measurement types that can be used for them . 
            self.validMeasurementTypes['setVoltage' ] = ['AuxOut', 'SineOut']
            self.validMeasurementTypes['getVoltage'] = ['AuxOut', 'SineOut', 'RT', 'AuxIn']
            self.validMeasurementTypes['setBField'] = ['AuxOut']
            self.validMeasurementTypes['getBField'] = []
            self.validMeasurementTypes['getCurrent'] = ['AuxOut', 'SineOut']
            self.validMeasurementTypes['setCurrent'] = ['AuxOut', 'SineOut']
            
        def checkSafe(self, port):#Returns Boolean. Checks if the lockin is off or not. 
            out = float(self.ask("AUXV? %f"%port))
            if abs(out)<.02:
                return True
            else:
                return False
            
        def clear(self): #This function is slow because it waits for a timeout error. I've considered manually lowering the timeout on the lock-in to make it useable.
            try:
                self.read()
            except:
                pass
            
        def getAuxVoltageIn(self, port):
            return float(self.ask('OAUX? %i'%port))
        
        def getAuxVoltageOut(self, port):
            return float(self.ask('AUXV? %i'%port))
        
        def getFilterStatus(self): #get the status of the filters
            l = ['None','Line notch', '2xLine Notch', 'Both']
            i = int(self.ask('ILIN?'))
            return l[i]
        
        def getInitialState(self): #return the initial state. 
            tc = self.getTimeConstant()
            sen = self.getSensitvity()
            ref = self.getRefFreq()
            src = self.getRefSource()
            amp = self.getSinAmp()
            fstatus = self.getFilterStatus()
            return str(self)[:-5] + "Time Constant = %s\nSensitivity = %s\nReference Frequency = %f Hz\nSine Amplitude = %f V\nReference Source = %s\nFilter Status = %s\n"%(tc,sen,ref,amp,src,fstatus)

        def getRandT(self): #Returns a tuple with the R and theta value taken at the same instant. 
            both = self.ask("SNAP? 3,4").split(',')
            R=float(both[0].strip())
            T=float(both[1].strip())
            return (R,T)
            
        def getRefFreq(self):
            return float(self.ask('FREQ?'))
            
        def getRefSource(self): #Return's the reference source as a string.
            out = int(self.ask('FMOD?'))
            if out==1:
                return 'Internal'
            return 'External'
            
        def getSensitvity(self): #Returns the sensitivity as a string, with units.
            key = int(self.ask("SENS?"))
            return self.sensitivityConstants[key]
            
        def getSinAmp(self): #Gets the amplitude of the sine output
            return float(self.ask('SLVL?'))
            
        def getTimeConstant(self):# Returns the time constant as a string, with units. 
            key = int(self.ask("OFLT?"))
            return self.timeConstants[key]
            
        def getVoltage(self): #returns only the R value of R and T
            V= self.getRandT()
            return V[0]
            
        def makeSafe(self,port): #This function raises an error if the lockin won't turn off. 
            self.rampDownV(port)
            if not self.checkSafe(port):
                raise self.LabInstrumentError
            
        def rampDownV(self, port): #Ramp down the voltage to 0 rather than a large change. 
            self.rampV(port, 0) 
            
        def rampV(self, port, vf):
            #this function safely ramps the voltage both up and down.
            #i'm considering if vf-v is within some small bound just writing it normally and not worrying about itereating. 
            v = float(self.ask('AUXV? %i'%port))
            if abs(vf-v)<self.vLimit:
                self.write('AUXV %i,%f'%(port, vf))
                return
            vstep = (vf-v)/self.nVSteps 
            while abs(vf-v)>self.Limit:
                v+=vstep
                self.write('AUXV %i,%f'%(port, v))
            self.write('AUXV %i,%f'%(port, vf))
            
        def setAuxVoltage(self, port, voltage):
            self.rampV(port, voltage)# this should ramp the voltage. 
            #self.write('AUXV %i,%f'%(port, voltage))
            
        def setRefFreq(self, freq):
            self.write('FREQ %f'%freq)
            
        def setSensitvity(self, sens): # set the sensitivity from values in sensitivityConstants
            index = -1
            for i in xrange(len(self.sensitivityConstants)):
                if sens==self.sensitivityConstants[i]:
                    index = i
            if i!=-1:
                self.write('SENS %i'%index)
                
        def setSinAmp(self, amp): 
            self.write('SLVL %f'%amp)
                
        def setTimeConstant(self, const): #set the Time Constant from the values in timeConstants
            index = -1
            for i in xrange(len(self.timeConstants)):
                if const==self.timeConstants[i]:
                    index = i
            if i!=-1:
                self.write('OFLT %i'%index)
        
    class NanoVoltmeter(LabInstrument):
    #The nanovoltmeter is even more simple than the other devices I've used. This is the best I could come up with
    #for it. 
        def __init__(self,resAd):
            super(NanoVoltmeter, self).__init__(resAd)
            self.type = "Nanovoltmeter"
            self.ID = 'NONE' #As far as I can tell there is no unique ID for the NVM
            self.ranges = {'.002':1, '.02':2, '.2':3,'2':4,'20':5,'200':6,'1000':7}
            self.validGetsAndSets.extend(('getVoltage', 'getResistance'))
            
        def clear(self):
        #clear doesn't work for the NVM. 
            try:
                self.read()
            except:
                pass
            
        def getInitialState(self):
            volt = self.getVoltage()
            out = 'Initial Voltage = %f V'%volt
            return str(self)[:-5] + out
            
        def getVoltage(self):
            answer =self.ask("T1X")
            return float(answer[5:])
            
        def setFilter(self, setting): #set the device filter. 
            if setting in range(3):
                self.write("P"+str(setting)+'X')
            
        def setRange(self, r):#sets the voltmeter range
            #if the input is invalid it does not change the range.
            try:
                self.write("R"+str(self.ranges[r])+"X")
            except KeyError:
                pass
            
    class Voltmeter182(NanoVoltmeter):
    #the functionality of the Nanovoltmeter is similar to this more advanced model, but it is not exactly the same. 
        def __init__(self, resAd):
            super(Voltmeter182, self).__init__(resAd)
            self.type = "Voltmeter 182"
            self.ranges = {'.003':1, '.03':2, '.3':3,'3':4,'30':5,'AUTO':0,'OFF':8}
            
        def setFilter(self, setting): #set the device filter. 
            if setting in range(4): #0 is off, 1-3 is fast to slow.
                self.write("P"+str(setting)+'X')
            
        def setRange(self, r):#sets the voltmeter range
            #if the input is invalid it does not change the range.
            try:
                self.write("R"+str(self.ranges[r])+"X")
            except KeyError:
                pass
            
    class Voltmeter181(NanoVoltmeter):
    #this class only exists for completeness's sake. all of it's functionality is covered in Nanovoltmeter
        def __init__(self,resAd):
            super(Voltmeter181, self).__init__(resAd)
            self.type = "Voltmeter 181"
            
    class SpectrumAnalyzer(LabInstrument):
        #subclass for the spectrum Analyzer. 
        
        def __init__(self, resAd):
            super(SpectrumAnalyzer, self).__init__(resAd)
            self.type = 'Spectrum Analyzer'
            self.validGetsAndSets.append('GASPSD')
            self.validGetsAndSets.append('Noise Subtract')
            # i will also need to specify the valid gets and sets, as well as valid measurement types. 
            
    class FSP38(SpectrumAnalyzer):
        # subclass for a specific analyzer. 
        
        def __init__(self, resAd):
            super(FSP38, self).__init__(resAd)
            self.type = 'FSP38'
            self.validPowerUnits = ['DBM', 'V', 'W', 'DB'] #valid units to set to measure power. There are other, redundant ones, like 'VOLT' and 'AMP'.
            self.validSweepPoints = [125,251,501,1001, 2001,4001, 8001]
            # I wonder if I should move/copy these to the GAS method.
            
            #the below code is copied from the VB. initial initializations may be necessary, and some of these may not be. 
            self.write('SYST:DISP:UPD ON') #set display to update while measurements are run.
            self.write('DISP:FORM SINGLE') # set it to full screen
            self.write('DISP:WIND1:SEL') # select screen A
            self.write('INIT:CONT ON') #turn on continuous measurement 
            
            #get some initial parameters. 
            self.refLevel = float(self.ask('DISP:TRAC:Y:RLEV?')) #Reference level at start. Should be the same unit as the powerUnit
            self.resBandwidth = float(self.ask('BAND:RES?')) #bandwith resolution in Hz
            #Some commands, Like BAND and FREQ automatically assume a prefix of SENS:
            self.startFreq = float(self.ask('FREQ:START?'))
            self.stopFreq = float(self.ask('FREQ:STOP?')) # Both in Hz. 
            self.powerUnit = str(self.ask('CALC:UNIT:POW?')) #get the unti the power is measured in as a string; will usually be one character. 
            self.sweepCount = int(self.ask('SWEEP:COUNT?')) # the number of sweeps
            self.sweepPoints = int(self.ask('SWEEP:POINTS?')) # the number of datapoints for the measurement
            
        def getInitialState(self):
            #returns all the information for all the getters for this object
            out = 'Reference Level = %.2f %s\n'%(self.getRefLevel(), self.getPowerUnit())
            out +='RES Bandwidth = %.2e Hz\n'%self.getResBandwidth()
            out+='Range = (%.2e, %.2e) Hz\n'%(self.getStartFreq(), self.getStopFreq())
            out+='Sweep Count = %i\n'%self.getSweepCount()
            out+='Sweep Points = %i\n'%self.getSweepPoints()
            out+='Amplitude Unit = %s\n'%self.getPowerUnit()
            return str(self)[:-5] + out
            
        def getPowerUnit(self):
            self.powerUnit = str(self.ask('CALC:UNIT:POW?'))
            return self.powerUnit
            
        def getRange(self):
            #returns the start and stop frequency as a tuple
            return (self.getStartFreq(), self.getStopFreq())
        
        def getRefLevel(self):
            self.refLevel = float(self.ask('DISP:TRAC:Y:RLEV?'))
            return self.refLevel
        
        def getResBandwidth(self):
            self.resBandwidth = float(self.ask('BAND:RES?'))
            return self.resBandwidth
        
        def getStartFreq(self):
            self.startFreq = float(self.ask('FREQ:START?'))
            return self.startFreq
        
        def getStopFreq(self):
            self.stopFreq = float(self.ask('FREQ:STOP?'))
            return self.stopFreq
        
        def getSweepCount(self):
            self.sweepCount = int(self.ask('SWEEP:COUNT?'))
            return self.sweepCount
        
        def getSweepPoints(self):
            self.sweepPoints = int(self.ask('SWEEP:POINTS?'))
            return self.sweepPoints
        
        def release(self):
            pass # I wanted to find a way to release the front panel but my search for a simple way to do it was fruitless
            #i may try again later. 
        
        def setPowerUnit(self, unit):
            if unit not in self.validPowerUnits: #check that the unit is valid.
                raise self.LabInstrumentError, 'Invalid Power Unit for the FSP38'
            self.write('CALC:UNIT:POW %s'%unit)
            self.getPowerUnit() #reassign the instance variable in the get method. 
            
        def setRange(self, start, stop, points = None):
            #sets both the start and stop freq
            #inputs must be in Hz
            self.setStartFreq(start)
            self.setStopFreq(stop)
            if points!= None:
                self.setSweepPoints(points)
            
        def setRefLevel(self, refLev):
            self.write('DISP:TRAC:RLEV %f'%refLev)
            self.getRefLevel()
            
        def setResBandwidth(self, resBand):
            self.write('BAND:RES %f'%resBand)
            self.getResBandwidth()
            
        def setStartFreq(self, freq):
            self.write('FREQ:START %f'%freq)
            self.getStartFreq()
            
        def setStopFreq(self, freq):
            self.write('FREQ:STOP %f'%freq)
            self.getStopFreq()
            
        def setSweepCount(self, count):
            self.write('SWEEP:COUNT %i'%count)
            self.getSweepCount() 
        
        def setSweepPoints(self, points):
            if points in self.validSweepPoints: # valid values for this
                self.write('SWEEP:POINTS %i'%points)
                self.getSweepPoints()

        def takeSpectrum(self, start = None, stop = None, points = None):
            if (start and stop): #Start and stop are not None
                self.setRange(start, stop, points)
            #runs the spectrum on the device
            self.write('INIT:CONT OFF') # I don't nkow why we turned this on in the first place.
            self.write('ABORT;INIT:IMM; *WAI') # start a sweet immeadiately; wait fro result. 
            #WAI waits until the measurement is done.
            
            #I don't know if ASCII will provide enough precision. If that's the case, REAL 32 will need to be used instead, and I'll need to figure out how to convert it to floats. 
            self.write('FORMAT ASC') 
            out = self.ask('TRAC1? TRACE1') #get the data from the instrument. 
            
            data = out.split(',')
            for i in xrange(len(data)):
                data[i] = float(data[i]) #turn from strings to float.
                
            self.write('INIT:CONT ON')
            return data
        
    class MicrowaveSource(LabInstrument):
        
        def __init__(self, resAd):
            super(MicrowaveSource,self).__init__(resAd)
            self.type = 'Microwave Source'
            self.validGetsAndSets.append('setMicrowaveSource')
            #TODO: Append the valid gets and sets here
            
    class AN68369A(MicrowaveSource):
        
        def __init__(self, resAd):
            super(AN68369A, self).__init__(resAd)
            self.type = 'AN 68369A'
        
            #TODO: in here, but in a dictionary of the constants and units that this inst uses
            
        def incFreq(self):
            #increases the frequency by a predetermined stepsize.
            self.write('F1 UP CLO')
            
        def decFreq(self):
            #decreases the frequency by a predetermined stepsize
            self.write('F1 DN CLO')
            
        def release(self):
            #restore local control of the instrument
            self.write('RL')
            
        def setStepsize(self, stepSize):
            #determine the stepsize that is incremented
            #stepsize always in Hz
            self.write('F1 SYZ %f Hz CLO'%stepSize)
            
        def setAmp(self, amp, unit = 'mV'): #dBm is represented by DM
            #set the outward power; also turns it on
            if unit == 'mV':
                self.write('LIN L1 %f mV CLO'%amp)
            else:
                self.write('LOG L1 %f DM CLO'%amp)
            
        def setFreq(self, freq):
            #self explanatory; freq always in Hz
            self.write('F1 %f Hz CLO'%freq)
            
        def off(self):
            #turn off RF power. 
            self.write('RF0')
        
        def on(self):
            #turn on RF power. 
            self.write('RF1')
        
    instrumentDictionary = {'Lock-in Amplifier':LockIn, 'Voltmeter 181': Voltmeter181, 'Voltmeter 182': Voltmeter182, 'Gaussmeter 425': Gaussmeter425, 
                            'Gaussmeter 455': Gaussmeter455, 'Gaussmeter 450': Gaussmeter450, 'FSP38': FSP38, 'AN 68369A': AN68369A}
    #the above dictionary holds the type of each instrument as a key and maps to the object definition. Used in a few files to take strings to objects easily. 
    
    
    #this code attempts to autogenerate the instrumentDictionary. I ran into a snag though in that I don't know how to make the string into an object name
    '''
    f = open('Instruments.py', 'r')
    objectsAndTypes= [[],[]]
    objectsToIgnore = []
    lines = []
    for line in f:
        lines.append(line)
        
    for lineNumber in xrange(len(lines)):
        line = lines[lineNumber]
        if line[:9]=='    class':
            parIndex = -1
            for char in line:
                parIndex+=1
                if char=='(':
                    break
            objectsAndTypes[0].append(line[10:parIndex])
            objectsToIgnore.append(line[parIndex+1:-3])
            n = -1
            for line in lines[lineNumber:]:
                n+=1
                if line.find('type')!=-1:
                    break
            typeLine = lines[lineNumber+n]
            objectsAndTypes[1].append(typeLine[25:-2])
    arr = []
    for i in xrange(len(objectsAndTypes[0])):
        if objectsAndTypes[0][i] not in objectsToIgnore:
            arr.append((objectsAndTypes[1][i], objectsAndTypes[0][i]))
    out =  dict(arr)
    '''