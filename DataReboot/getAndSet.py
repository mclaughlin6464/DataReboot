'''
6/21/2013
Author: Sean McLaughlin
This module will contain the references to all the methods used to abstractly set sources and readers for instruments. 
'''
if __name__ ==  '__main__':
    print''' 
This module contains the code for the getters and setters for the instrument. Each class will be passed a LabInstrument reference and a few other parameters to allow them
to become independent sources.  This class also contains the dictionary that mathces the name of each method to it's constructor. Also in this module is the 
location of unit dictionaries and the keys to use in the kwargs and the GASconfig.

What is a getAndSet object and why was it created? I'll try to explain it briefly. Each object takes an instrument and a few other initialziations and 
allows for smooth setting and reading of a parameter. The object handles idiosyncracies between instruments and abstracts the measurement process a great deal.
Each object has a 'get()' or 'set(x)' method that allows for the measurement to be extremely general. There are a few exceptions to this rule and they are commented in detail.
It is important that in this module, when a new object is added, to update the dictionary at the end to include the object.
'''
    
from Instruments import *
from time import sleep
from math import pi

#a dictionary of dictionaries, which produces the units for a type of measurement
units = {}
units['Volts'] = {'uV':1e-6,'mV':.001, 'V':1}
units['B-Field'] = {'T':1,'G':1e-4, 'Oe':1e-4, 'A/m': 1/((4*pi)*1e-7)}
units['Current'] = {'uA': 1e-6, 'mA': 1e-3, 'A': 1}
units['Resistance'] = {'Ohm':1, 'mOhm':.001, 'kOhm':1e3}
units['Frequency'] = {'Hz': 1 , 'GHz': 1e9, 'MHz': 1e6, 'KHz' : 1e3} 

#these objects overload multiplication and division, so they can be used to convert units teh same way as the others.
class convertDBMToPow(object): 
    #a class with overloads so it will behave like a number but will act as a function to do unit conversions
    def __eq__(self, other): # using the units I check if they are == 1, to see if they are the default. 
        return False
    
    def __mul__(self, other):# I multiply the  dbm value by the conversion to convert to power. I'm adjusting it to do the calculation itself.
        return .001*(10**other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __div__(self, other): # do the inverse conversion
        return 1/(self.__rdiv__(other))
    
    def __rdiv__(self, other):
        from math import log10
        return log10(other/.001)
            
class convertVToPow(object):
    #a class with overload so it will behave like a number but will act like a function to do unit conversions. 
    def __eq__(self, other):# using the units I check if they are == 1, to see if they are the default. 
        return False
    
    def __mul__(self, other):# i multiply the V value by the conversion to conver to power. I'm adjusting it to do the function instead. 
        return other**2/50
    
    def __rmul__(self,other):
        return self.__mul__( other)
    
    def __div__(self, other):# do the inverse conversion; this only works one way, so I don't know if some code will break. 
        return 1/(self.__rdiv__(other))
    
    def __rdiv__(self, other):
        from math import sqrt
        return sqrt(50*other)

units['PSD'] = {'W': 1, 'dBm': convertDBMToPow(), 'V': convertVToPow()}

#These are the keys used in the kwargs for the get and sets. They are what is written to the config file and used in initialztion. 
GASname = 'Name'
measType= 'Measurement Type'
classType = 'Class Type'
port = 'Port'
delay = 'Delay'
comment = 'Comment'
instrument = 'Instrument'
add = 'Address'
delay2 = 'Delay 2'
gC = 'getCurrent'
gV = 'getVoltage'
OCR = 'OCR'
TCM = 'TCM'
TCM2 = 'TCM2'
amp = 'Amplitude'
cal = 'Calibration Factor' 
end = 'END\n'

GASkeys = (GASname, measType, port, delay, comment, instrument, delay2, gC, gV, OCR, TCM, TCM2, amp, cal, end)

class getAndSet(object):
    #general superclass. Subclasses provide functionality.
    def __init__(self, **kwargs):
        #kwargs::
        #GASname : the name of the object
        #measType: the type of measurement, i.e. auxout, sinamp, etc. 
        #instrument: the reference to a LabInstrument object
        #port: the port (if there is one) to use
        #comment: the comment that shows up in the tooltip for this object
        #delay: how long to wait after a set or before a measurement to ensure accuracy.
        
        self.name = kwargs[GASname]
        self.className = 'getAndSet'
        if measType not in kwargs or kwargs[measType] is None:
            self.type = None
        else:
            self.type = kwargs[measType]
        self.LIRef = kwargs[instrument]
        self.InstrumentType = self.LIRef.type
        if port not in kwargs or kwargs[port] is None:
            self.port = None
        else:
            self.port = int(kwargs[port])
        self.OCR = None #over written in the lower classes. 
        
        if comment not in kwargs or kwargs[comment] is None:
            self.comment = 'None'
        else:
            self.comment = str(kwargs[comment]) # an optional comment to explain the details of the object to the user.
            
        if delay not in kwargs or kwargs[delay] is None: # a delay to wait after a parameter is set or before a measurement is taken
            self.delay = 0
        else:
            self.delay = float(kwargs[delay])
            
        #instance variables
        self.validTypes = ['AuxOut', 'SineOut', 'R']
        self.validPorts = range(1,5)
        self.unitDictionary = {} #will be populated with a key for the unit abbreviation adn the conversion the standard SI unit. 
        
        #certain errors to raise if there is an incorrect input. 
        if (self.InstrumentType == "Lock-in Amplifier") and (self.type == 'AuxOut') and (self.port == None):
            raise self.LIRef.LabInstrumentError, 'When using AuxOut on the lock-in, please specify a port.'
        elif (isinstance(self.LIRef, NanoVoltmeter) or isinstance(self.LIRef, HallProbe)) and (self.type!= None or self.port!=None):
            raise self.LIRef.LabInstrumentError, "The %s doesn't have a port or type"%str(self.LIRef)
        
    def __str__(self):
        #makes a default string representation of the object. Used when writing the object to file. 
        #this is frequently overwritten in subclasses to add new features. 
        out = ['\n%s = %s'%(GASname, self.name), 'Class Type = %s'%self.className, '%s = %s'%(instrument, self.InstrumentType),'%s = %s'%(add, self.LIRef.address)]
        if self.type is not None:
            out.append('%s = %s'%(measType, self.type))
        if self.port is not None:
            out.append('%s = %s'%(port, self.port))
        if self.OCR is not None:
            out.append('%s = %f (A/V)'%(OCR, self.OCR))
        if self.delay is not None:
            out.append('%s = %s seconds'%(delay, self.delay))
        out.append('%s= %s\n'%(comment, self.comment) )
        return '\n'.join(out)
    
    def getState(self):
        #returns a string with all the initial info of the object. 
        INSTstate = self.LIRef.getInitialState()
        GASstate = str(self)
        return GASstate+INSTstate
    
#the below methods are overwrittne below, and return a boolean to easily determine it's nature. 
    
    def isGetter(self):
        return False
    
    def isSetter(self):
        return False

    def isGASPSD(self):
        return False
    
    def isNoiseSubtract(self):
        return False

    def off(self):
        #turns off the device in a specific way
        #overwritten in subclasses
        self.LIRef.release()

    def standUnit(self):
        #finds the 'standard unit' for the object. In the unit dictionary, the standard unit is the unit with a value of 1. 
        #the concept of a 'standard unit' can get a little more complex than it at first seems. For example, there are frequenct issues with frequency measurements
        #the standard unit of frequency is Hz, but GHz is far more convenient. 
        for key, value in self.unitDictionary.iteritems():
            if value == 1:
                return key
        else:
            return 'None'

class setVoltage(getAndSet):
    #defines a voltage source Class. I should consider a better name. 
    def __init__(self, **kwargs): 
        #kwargs::
        #None
        
        super(setVoltage, self).__init__( **kwargs ) #call the super class
        self.className = 'setVoltage'
        
        self.unitDictionary = units['Volts'] #get the unit dict. 
        
        if 'setVoltage' not in self.LIRef.validGetsAndSets: #check to see that the instrument is valid for this class
            raise self.LIRef.LabInstrumentError, '%s is not a valid setVoltage object'%(self.InstrumentType)
    
    def isSetter(self):
        return True
    
    def off(self): 
        self.set(0)
        self.LIRef.release()
    
    def set(self, voltage):
        #all classes in this module will have a 'get' or 'set' method based on their nature. this makes them more general
        # i considered making the objects callable, but that could make things confusing down the line. 
        # I intend to do this for all classes in this module
        self.setVoltage(voltage)
        
    def setVoltage(self, voltage): 
        #main function for this object, set the voltage depending on what the INST is.
        #it could be possible to alternatively define this method based on the INST, so that these checks dont' need to be made every time.
        global sleep
        if (self.InstrumentType == "Lock-in Amplifier") and (self.type == 'SineOut'):
            #set the internal reference voltage
            if voltage == 0:
                voltage = 1 # the sineout cannot be set to 0.
            self.LIRef.setSinAmp(voltage)
                
            #I wonder if I should set a few methods specific to this type of instrument, like refFreq. I worry about having non-general methods.
        elif (self.InstrumentType == 'Lock-in Amplifier') and (self.type=='AuxOut'):
            #set the aux out for that particular port. (self, voltage):
            self.LIRef.setAuxVoltage(int(self.port), voltage)
            
        else:
            raise self.LIRef.LabInstrumentError , 'There was a problem with your inputs that was not normal for the %s.'%self.name
        sleep(self.delay)#sleep to allow conditions to settle
        
class getVoltage(getAndSet):
    #defines a voltage reader. similar to the setVoltage class. 
    def __init__(self, **kwargs):
        #kwargs :: 
        #TCM : a boolean whether or not to set the delay as a multiple of the time constant on the lockin or a manual set time. 
        
        super(getVoltage, self).__init__(**kwargs )
        
        self.className = 'getVoltage'
        self.multiples = -1 #if this is not negative one, there are multiples to the time constant. 
        if isinstance(self.LIRef, LockIn):#if the INST is a lockin, it could be a multiple of the timeconstant. 
            if kwargs[TCM]: #TODO: Fix so this will work with the new config. 
                self.multiples = self.delay
                self.delay = self.delay*self.LIRef.getTimeConstant() #i may need to change this so this gets called before the measurement
        
        self.unitDictionary = units['Volts']
        
        if 'getVoltage' not in self.LIRef.validGetsAndSets:
            raise self.LIRef.LabInstrumentError, '%s is not a valid getVoltage object'%(self.InstrumentType)
    
    def __str__(self):
        if self.multiples != -1: #if we have multiples of the time constant, we need to change our output string. 
            old = super(getVoltage, self).__str__()
            delayIndex = old.find('Delay = ') 
            newLineIndex = old.find('\n', delayIndex+ len('Delay = '))
            newStr = old[:delayIndex-1] + 'Delay = %i multiples of the time constant'%(self.multiples) + old[newLineIndex:]
            return newStr
        else:
            return super(getVoltage, self).__str__()
        
    def isGetter(self):
        return True
    
    def get(self):
        return self.getVoltage()
    
    def getVoltage(self):
        global sleep
        #main method for the object. defines the proper way for the instrument to read
        sleep(self.delay)
        if (self.InstrumentType == "Lock-in Amplifier") and (self.type == 'SineOut'):
            #get the internal reference voltage
            return self.LIRef.getSinAmp()
        elif (self.InstrumentType == 'Lock-in Amplifier') and (self.type == 'RT'):
            return self.LIRef.getRandT() #WARNING: This returns a tuple. Be careful when using this method. 
            
        elif (self.InstrumentType == 'Lock-in Amplifier') and (self.type=='AuxOut'):
            #get the aux out for that particular port.
            return self.LIRef.getAuxVoltageOut(int(self.port))
        
        elif isinstance(self.LIRef, NanoVoltmeter) or isinstance(self.LIRef, LockIn):
            return self.LIRef.getVoltage() #both have this method. 
        
        else:
            raise self.LIRef.LabInstrumentError , 'There was a problem with your inputs that was not normal.'
        
    def standUnit(self): #if the type is RT, this can return 2 values instead of one. Therefore, there are sometiems 2 units. 
        if self.type == 'RT':
            return super(getVoltage, self).standUnit(), 'DEG'
        else:
            return super(getVoltage, self).standUnit()
        
class getBField(getAndSet):
    
    def __init__(self, **kwargs):
        #kwargs :: 
        #TCM : a boolean whether or not to set the delay as a multiple of the time constant on the lockin or a manual set time. 
        
        super(getBField, self).__init__(**kwargs)
        self.className = 'getBField'
        self.multiples = -1
        if isinstance(self.LIRef, LockIn):#if the INST is a lockin, it could be a multiple of the timeconstant. 
            if kwargs[TCM]: #TODO: Fix so that this works with the new CONFIG
                self.multiples = self.delay
                self.delay = self.delay*self.LIRef.getTimeConstant() #i may need to change this so this gets called before the measurement
        
        self.unitDictionary = units['B-Field']
        
        if isinstance(self.LIRef, HallProbe):
            self.LIRef.setBUnit('T') #the default unit in the code will be Tesla.
        
        if 'getBField' not in self.LIRef.validGetsAndSets:
            raise self.LIRef.LabInstrumentError, '%s is not a valid getBField object'%(self.InstrumentType)
    
    def __str__(self):
        if self.multiples != -1: #if we have multiples of the time constant, we need to reflect that in the string representation. 
            old = super(getBField, self).__str__()
            delayIndex = old.find('Delay = ') + len('Delay = ')
            newLineIndex = old.find('\n', delayIndex)
            newStr = old[:delayIndex-1] + 'Delay = %i multiples of the time constant'%(self.multiples) + old[newLineIndex:]
            return newStr
        else:
            return super(getBField, self).__str__()
    
    def isGetter(self):
        return True
    
    def get(self):
        return self.getBField()
    
    def getBField(self):
        global sleep
        sleep(self.delay)
        #if isinstance(self.LIRef, LockIn):
        #    return self.LIRef.getVoltage()*self.calibrationFactor
        #i currently havne't fully configured using a lockin to read field. 
        if isinstance(self.LIRef, HallProbe):
            from time import sleep
            return self.LIRef.getBField()

class setBField(getAndSet):
    
    def __init__(self,**kwargs): 
        #kwargs::
        #cal: the calibration factor relating voltage to field strength
        #delay2: the second delay, to use if the field step is large, to give it more time to adapt. 
        
        super(setBField, self).__init__( **kwargs)
        self.className = 'setBField'
        
        if cal in kwargs and kwargs[cal] is not None:
            self.calibrationFactor = float(kwargs[cal]) #in units of T/V
        else:
            self.calibrationFactor = 1
            
        if delay2 not in kwargs or kwargs[delay2] is None: # a second delay for large field changes. 
            self.delay_2 = 1
        else:
            self.delay_2 = float(kwargs[delay2])
        self.lastField = 0 # a most recent holder so we can decide what delay to use 
        
        self.unitDictionary = units['B-Field']
        
        if 'setBField' not in self.LIRef.validGetsAndSets:
            raise self.LIRef.LabInstrumentError, '%s is not a valid setBField object'%(self.InstrumentType)
        
    def __str__(self):
        #factor in our delay 2 and cal factor to the string output.
        old = super(setBField, self).__str__()
        commentIndex = old.find('Comment')
        newStr = old[:commentIndex] + 'Delay 2 = %s seconds\nCalibration Factor = %f T/V\n'%(self.delay_2,self.calibrationFactor) + old[commentIndex:] #insert the calibration factro
        return newStr
        
    def isSetter(self):
        return True
        
    def off(self):
        self.setVoltage(0)
        self.LIRef.release()
        
    def set(self, field):
        self.setBField(field)
            
    def setBField(self, field):
        global sleep
        self.LIRef.setAuxVoltage(int(self.port), (field/self.calibrationFactor))
        if abs(field-self.lastField) >=.1:#sleep for longer if we're setting a major field.
            sleep(self.delay_2)
        else:
            sleep(self.delay)
        self.lastField = field #update most recent holder
        
    def setVoltage(self, voltage): #set a voltage without a calibration factor. Used when calibrating.
        self.LIRef.setAuxVoltage(int(self.port), voltage)
        
class setCurrent(getAndSet):
    
    def __init__(self,**kwargs):
        #kwargs:
        #OCR: the output current range, the ratio between output volts and current. 
        
        self.maxV = 10 #the maximum current allowed to be pumped into the currenst source. 
        
        super(setCurrent, self).__init__(**kwargs)
        self.className = 'setCurrent'
        if  OCR not in kwargs or kwargs[OCR] is None:
            self.OCR = 1e-5
        else:
            self.OCR = float(kwargs[OCR])
        
        self.unitDictionary = units['Current']
        
        if 'setCurrent' not in self.LIRef.validGetsAndSets:
            raise self.LIRef.LabInstrumentError, '%s is not a valid setCurrent object'%(self.InstrumentType)
        
    def isSetter(self):
        return True
        
    def off(self):
        if self.type == 'SineOut':
            self.LIRef.setSinAmp(1)
        elif self.type == 'AuxOut':
            self.LIRef.setAuxVoltage(self.port, 0)
        self.LIRef.release()
        
    def set(self, current = None, freq = None):
        #passing in one arguement sets the current. Passing 2 sets current and frequency. Passing in freq = x sets the freq to x without changing the current.
        self.setCurrent(current, freq = freq)
        
    def setCurrent(self, current = None, freq = None):
        global sleep
        if current is  None and freq is None:
            raise self.LIRef.LabInstrumentError, 'setCurrent requires either a current or frequency to set.'
        if freq is not None:
            if self.type == 'SineOut': #set the AC current freq
                self.LIRef.setRefFreq(freq)
            else:
                raise self.LIRef.LabInstrumentError, "%s doesn't have a Frequency to set."
        if current is not None:
            v = current/self.OCR
            if abs(v)>self.maxV: #check that the voltage isn't over the maximum allowed. 
                raise self.LIRef.LabInstrumentError, 'Too high of a current.'
            if self.type=='SineOut':
                self.LIRef.setSinAmp(v)
            elif self.type == 'AuxOut':
                self.LIRef.setAuxVoltage(self.port, v)
            else:
                raise self.LIRef.LabInstrumentError, "User entry did not match any expected output."
        sleep(self.delay)

class getCurrent(getAndSet):
    #i dont know if I should have the ability to get frequency
    
    def __init__(self, **kwargs):
        #kwargs:
        #OCR: The output current range, the ratio between current and voltage. 
        #TCM: Determine if the delay is from a multiple of the time constant or a manually set time. 
        
        super(getCurrent, self).__init__(**kwargs)
        self.className = 'getCurrent'
        self.multiples = -1
        if isinstance(self.LIRef, LockIn):#if the INST is a lockin, it could be a multiple of the timeconstant. 
            if kwargs[TCM]: #TODO Fix with new GASconfig
                self.multiples = self.delay
                self.delay = self.delay*self.LIRef.getTimeConstant() #i may need to change this so this gets called before the measurement
        
        if OCR not in kwargs or kwargs[OCR] is None:
            self.OCR = 1e-5
        else:
            self.OCR = float(kwargs[OCR])
        
        self.unitDictionary = units['Current']
        
        if 'getCurrent' not in self.LIRef.validGetsAndSets:
            raise self.LIRef.LabInstrumentError, '%s is not a valid getCurrent object'%(self.InstrumentType)
        
    def __str__(self):
        if self.multiples != -1: #update the output string with our new delay.
            old = super(getCurrent, self).__str__()
            delayIndex = old.find('Delay = ') 
            newLineIndex = old.find('\n', delayIndex+ len('Delay = '))
            newStr = old[:delayIndex-1] + 'Delay = %i multiples of the time constant'%(self.multiples) + old[newLineIndex:]
            return newStr
        else:
            return super(getCurrent, self).__str__()
        
    def isGetter(self):
        return True
        
    def get(self, freq = False): #passing in True will return the frequency, not the current.
        return self.getCurrent(freq)
        
    def getCurrent(self, freq = False):
        #this function has the ablility to return the current frequency. IT would also be possible to make it return both in a tuple, like in getVoltage.
        global sleep
        sleep(self.delay)
        if freq:
            return self.LIRef.getRefFreq()
        elif self.type=='AuxOut':
            return self.LIRef.getAuxVoltageOut(self.port)*self.OCR
        elif self.type=='SineOut':
            return self.LIRef.getSinAmp()*self.OCR
        else:
            raise self.LIRef.LabInstrumentError, "User entry did not match any expected output."
            
class getResistance(getAndSet): 
    #an object that reads from both a getCurrent and a getVoltage object and returns a resistance. 
    
    def __init__(self, **kwargs):
        #kwargs::
        #gC: the getCurrent object to use
        #gV: the getVoltage object ot use. 
        
        super(getResistance, self).__init__(**kwargs)
        self.className = 'getResistance'
        
        self.current = kwargs[gC]
        self.voltage = kwargs[gV]
        
        self.unitDictionary = units['Resistance']
        
        if 'getResistance' not in self.LIRef.validGetsAndSets:
            raise self.LIRef.LabInstrumentError, '%s is not a valid getResistance object'%(self.InstrumentType)
        
    def __str__(self):
        #update the string with the getVoltage and getCurrent object's names. 
        old = super(getResistance,self).__str__()
        commentIndex = old.find('Comment')
        newStr = old[:commentIndex] + 'getCurrent = %s\ngetVoltage = %s\n'%(self.current.name, self.voltage.name) + old[commentIndex:]
        return newStr
    
    def isGetter(self):
        return True
    
    def get(self):
        return self.getResistance()
    
    def getResistance(self):
        #simply uses Ohms 'Law' to calculate a resistance. 
        v =self.voltage.get()
        I = self.current.get()
        if I!=0:
            return v/I
        else:
            return float('inf') #when cast as a float, will be infinity. don't know if this messes anything up. 
            
class setMicrowaveSource(getAndSet):
    #an object that sets and steps frequencies on the microwave source
    
    def __init__(self, **kwargs):
        #kwargs:
        #amp: a string containing the amplitude and the ampUnit to set. This can be configured in the main measurement window and in the config. 
        
        super(setMicrowaveSource, self).__init__(**kwargs)
        self.className = 'setMicrowaveSource'
        
        if amp not in kwargs or kwargs[amp] is None:
            self.amp = -1 # an error will be raised if the amp is not set before a measurement is conducted. 
            self.ampUnit = 'mV'
        else:
            self.amp = float(kwargs[amp].split(' ')[0]) #split the string so separate the number and the unit.
            self.ampUnit = kwargs[amp].split(' ')[1]
            if self.ampUnit == 'dBm':
                self.ampUnit = 'DM'
            self.setMSAmp(self.amp, self.ampUnit)
            
        self.unitDictionary = units['Frequency']
        
        if 'setMicrowaveSource' not in self.LIRef.validGetsAndSets:
            raise self.LIRef.LabInstrumentError, '%s is not a valid setMicrowaveSource object'%(self.InstrumentType)
        
    def __str__(self):
        old = super(setMicrowaveSource,self).__str__()
        commentIndex = old.find(comment)
        newStr = old[:commentIndex] + '%s = %s %s\n'%(amp, str(self.amp), self.ampUnit)+ old[commentIndex:]
        return newStr
        
    def isSetter(self):
        return True
    
    def off(self):
        self.LIRef.off()
        self.LIRef.release()
    
    def set(self, freq = None, amp = None):
        self.setMS(freq, amp)
        
    def setMS(self, freq = None, amp = None, ampUnit = 'mV'):
        #I am unsure about this function for a couple of reasons. 
        #The MS has the ability to specify the step size and then 'step' the frequency. 
        #It also has the function to set the frequency directly. I do not know which is better. The frequency one is easier to implement at present and 
        #Matt and I were unable to find a difference between the 2 of any importance.
        #In order to implmenet the stepSize, if necessary, the MS object would require special intialization before each measurement to pass in a step size
        #and start frequency and then put the step here. 
        if freq is not None:
            if self.amp == -1:
                raise self.LIRef.LabInstrumentError, 'The amplitude must be set first.'
            self.LIRef.setFreq(freq)
        if amp is not None:
            self.LIRef.setAmp(amp, ampUnit)
            self.amp = amp
        self.LIRef.on()
        
    def setMSAmp(self, amp, ampUnit = 'mV'): #set the amplitude without turning on the source. 
        self.LIRef.setAmp(amp, ampUnit)
        self.amp = amp
        self.ampUnit = ampUnit
        
class GASPSD(getAndSet):
    #A unique subclass of the getAndSet class. This uses the spectrum analyzer, and unlike the others , cannot 'set' or 'get' one point. Rather, it does it's own spacing and measureing.
    #the code using this object will have ot account for this. 
    def __init__(self, **kwargs): 
        #kwargs::
        #None
        super(GASPSD, self).__init__( **kwargs)
        self.className = 'GASPSD'
        self.set(powerUnit = 'W')
            
        #there are 2 units dictionaries, because this class is a bit of a getter and a setter. 
        self.unitDictionary = units['Frequency']
        self.readerUnitDictionary = units['PSD']
        
        if 'GASPSD' not in self.LIRef.validGetsAndSets or not isinstance(self.LIRef,SpectrumAnalyzer):
            raise self.LIRef.LabInstrumentError, '%s is not a valid %s object'%(self.InstrumentType, self.className)
        
    def isGASPSD(self):
        return True
        
    def get(self, start = None, stop = None, points = None):
        #generic wrapper for the getPSD method
        data = self.getPSD(start, stop, points)
        return data
            
    def getPSD(self, start = None, stop = None, points = None):
        #allows the user to set a power spectrum parameters and returns an array of the data. 
        global sleep
        sleep(self.delay)
        data = self.LIRef.takeSpectrum(start, stop, points)
        return data
        
    def set(self,refLevel = None, resBandwidth = None, start = None, stop = None, points = None, count = None, powerUnit = None):
        # a wrapper for the setPSDmethod
        self.setPSD( refLevel, resBandwidth,start, stop, points, count, powerUnit)
            
    def setPSD(self,refLevel = None, resBandwidth = None, start = None, stop = None, points = None, count = None, powerUnit = None): #could modify to a **kwargs call. 
        #one method that allows the user to set any and all variables for the spectrum analyzer with keyword arguements. 
        if (start and stop):
            self.LIRef.setRange(start, stop)
                
        if points:
            self.LIRef.setSweepPoints(points)
            
        if count:
            self.LIRef.setSweepCount(count)
                
        if powerUnit:
            self.LIRef.setPowerUnit(powerUnit)
                
        if refLevel:
            self.LIRef.setRefLevel(refLevel)
            
        if resBandwidth:
            self.LIRef.setResBandwidth(resBandwidth)
                
    def standUnit(self, reader = False): # a complex overwrite of the standUnit function. Allows for the return ofa unit from either unit dict. Also, uses GHz as the default. 
        if not reader:
            for unit, value in self.unitDictionary.iteritems():
                if value == 1e9:
                    return unit
            else:
                return 'None'
        else: # return the reading units 
            for unit,value in self.readerUnitDictionary.iteritems():
                if value == 1:
                    return unit
            else:
                return 'None'
                
class NoiseSubtract(getAndSet):  
    #another unique subclass of the get and set class. used in conjunction with the GASPSD class, this class takes and stores a background spectrum, to subtract off from the 
    #psd spectrum. 
    
    #I considered the idea of making this class a subset of GASPSD. I didn't, ultimately, because not a lot of functionality would carry over, at least not as much as you'd think.
    def __init__(self, **kwargs):
        #kwargs:
        #None
        
        super(NoiseSubtract, self).__init__(**kwargs)
        
        self.className = 'Noise Subtract'
        #these can be used to convert the amplitude units if need be. 
            
        self.unitDictionary = units['Frequency']
        self.readerUnitDictionary = units['PSD']
        
        #intance variables to describe the spectrum.
        self.freqRange = (-1, -1)
        self.points = -1
        self.spectrum = []
        
        if self.className not in self.LIRef.validGetsAndSets or not isinstance(self.LIRef,SpectrumAnalyzer):
            raise self.LIRef.LabInstrumentError, '%s is not a valid %s object'%(self.InstrumentType, self.className)
        
    def __str__(self):
        #update the string method. 
        #this object is not written to file, though, at least not presently.
        oldStr = super(NoiseSubtract, self).__str__()
        commentIndex = oldStr.find(comment)
        newStr = oldStr[:commentIndex] + 'Range = (%f,%f) Hz    Points = %i\n'%(self.freqRange[0], self.freqRange[1], self.points)
        newStr += oldStr[commentIndex:]
        return newStr
        
    def isNoiseSubtract(self):
        return True
    
    def get(self, data):
        return self.getNoiseSubtract(data)
    
    def getNoiseSubtract(self, data):
        #this is not much of a 'get' in the same sense as the others; it is only called that for symmetry with the others
        #when the data from the PSD is passed in, it subtracts off the backgrounds spectrum
        #it is assumed that data and the spectrum are over the same frequency and number of points. 
        #the protection from that will be handled elsewhere
        global sleep
        sleep(self.delay)
        out = [0 for i in xrange(len(data))]
        for i in xrange(len(data)):
            out[i] = data[i] - self.spectrum[i]
        return out
    
    def set(self,startFreq, stopFreq, points):
        self.setNoiseSubtract( startFreq, stopFreq, points)
    
    def setNoiseSubtract(self, startFreq, stopFreq, points):
        #unlike the other set functions, this one sets self.spectrum by taking a sweep over the inputs
        self.freqRange = (startFreq, stopFreq)
        self.points = points
        self.spectrum = self.LIRef.takeSpectrum(startFreq, stopFreq, points)
                
    def standUnit(self, reader = False):
        #same unique standUnit as in GASPSD
        if not reader:
            for key in self.unitDictionary.keys():
                if self.unitDictionary[key] == 1e9:
                    return key
            else:
                return 'None'
        else: # return the reading units 
            for key in self.readerUnitDictionary.keys():
                if self.readerUnitDictionary[key] == 1:
                    return key
            else:
                return 'None'

#a dictionary that converts from the name of the class to its callable. 
#it is important that this is updated when new objects are added. 
GASdictionary = {'getAndSet': getAndSet, 'setVoltage': setVoltage, 'getVoltage': getVoltage, 'getBField': getBField,
                  'setBField': setBField, 'getCurrent': getCurrent, 'setCurrent': setCurrent, 'GASPSD': GASPSD, 
                  'Noise Subtract': NoiseSubtract, 'getResistance' : getResistance, 'setMicrowaveSource': setMicrowaveSource}