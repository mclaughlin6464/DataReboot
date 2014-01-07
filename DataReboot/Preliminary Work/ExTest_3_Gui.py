'''
Created on Jun 13, 2013

@author: Sean McLaughlin
This module will conduct a simple experiment using the lockin, nanovoltmeter and Hall Probe. There will be a choice on whether or not the user wants to use the Voltmeter or Lockin to 
measure the resistance.I also am going to attempt to use as much functional programming as possible to make the actual experiment be very very simple. 
'''



def main(StartRef, configFilename, dataFilename, lockinForV, maxField, minField, dataPoints):
    try:
        import numpy as np
        from time import clock, sleep
        from Instruments import LockIn, Voltmeter182
        from config import getResAds
        import datetime
    except ImportError:
        print 'There was a problem importing the modules; check the PYTHONPATH'
    else:
        global calibration
        calibration = 1
        #Not sure about this but I'll be able to reference them from within functions without them being arguements
        print '0'
        # Using the config module, read the config file specified by the user and assign the objects needed for this experiment. 
        instrumentDictionary = getResAds(configFilename)
        print '.2'
        lockin = LockIn(instrumentDictionary['Lock-in Amplifier'])
        print '0.5'
        nvm = Voltmeter182(instrumentDictionary['Voltmeter 182'])
        
        try:  # most of the module is run inside a try, with a finally that turns off voltage sources and closes files. 
                
            # start with all the function declarations
                
            def checkAbort():
                if (StartRef != None) and StartRef.abort: #allows it to run with 'None' for startref
                    raise IOError  # In the future,I will make my own error to raise. 
                
            def calibrateField(vsource, vport, lockin, fport):
                # takes a reference to a voltage source and a field measuremtn along with the bunit and returns the ratio between field/1V.
                # i am concerned that this should be more general. It will only work with a lockin source for now, and this specific one. 
                vsource.setAuxVoltage(vport, 2)
                
                b1 = getBField(lockin, fport)  # these two chunks make sure the bfield is nearly steady. 
                b2 = getBField(lockin, fport)
                while (b2 - b1) > 0.02:  # within a tolerance. The analog probe is very fast. I would loosen for the digital one. 
                    b2 = b1
                    b1 = getBField(lockin, fport)
                sleep(.1)
                bat2 = getBField(lockin, fport)
                    
                vsource.setAuxVoltage(vport, 1)
                    
                b1 = getBField(lockin, fport)
                b2 = getBField(lockin, fport)
                while (b2 - b1) > 0.02:  # within a tolerance.
                    b2 = b1
                    b1 = getBField(lockin, fport)
                sleep(.1)
                bat1 = getBField(lockin, fport)
                    
                vsource.makeSafe(vport)
                return (bat2 - bat1)
                
            def getVoltageFromField(field, c):
                return field / c
            
            def getResistance(current):
                return getVoltage() / current
            
            def setBField(field):
                voltage = getVoltageFromField(field, calibration)
                lockin.setAuxVoltage(4, voltage)
                
            def getBField(lockin, port):
                # i'm not using a hall probe for this experiment so I need to use the analog on the lock in.
                # i am unsure what to do for this function. it depends on how often we'll use this probe; which I think is infrequently
                v = lockin.getAuxVoltageIn(port)
                return v * 2  # the voltage is off by a factor of 2. 
                
            def calibrate():
                global calibration
                calibration = calibrateField(lockin, 4, lockin, 3)
                calibration = 1 #delete!
                
    
            calibrate()
            
            if lockinForV:
                def getVoltage():
                    return lockin.getVoltage()
            else:
                def getVoltage():
                    return nvm.getVoltage()
                    
            # handling of the data file. 
            print '1'
            dataFile = open(dataFilename, 'w')
            dataFile.write(str(datetime.date.today()) + '\n')  # write date
            dataFile.write(lockin.getInitialState())  # write the header
                    
            stepSize = (maxField - minField) / dataPoints
            print '2'
            # We conduct the measurement, and write the data to file and a few arrays.
            setBfields = np.arange(minField, maxField, stepSize)
            bfields = []
            resistances = []
            times = []
            dataFile.write('\nSet Field (kG)\tB-Field (kG)\tResistance (Ohm)\tTime (s)\n')
            StartRef.data = [[], bfields, resistances, times] #2x2 array of all the data, passed to the GUI to plot. 
            StartRef.abort = False #we can abort now that the measurement's begun.
            print '2'
            for sb in setBfields:
                setBField(sb)
                t = clock()
                times.append(t)
                b = getBField(lockin, 3)
                bfields.append(b)
                r = getResistance(.01)
                resistances.append(r)
                StartRef.data[0].append(sb) #This makes it so that the whole numpy array isn't in the data. 
                dataFile.write('%f\t%f\t%f\t%f\n' % (sb, b, r, t))
                checkAbort()
                    
            # after data collection is complete, close and turn off what we do not need
            lockin.makeSafe(4)
            dataFile.close()
            StartRef.statusBar().showMessage('Done.')
        finally: #This runs if there is an error or not. 
            dataFile.close()  # close the file.
            for port in xrange(1, 5):  # turn off the lock in in case of accidental exit. 
                lockin.makeSafe(port)
                if not lockin.checkSafe(port):
                    print 'The Lock-in stopped responding. Port %i is still on.' % port
                    
                    
if __name__=='__main__':
    main(None, 'config.txt', 'data.txt', True, .5, -.5, 500)
