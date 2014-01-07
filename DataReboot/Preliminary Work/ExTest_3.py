'''
Created on Jun 13, 2013

@author: Sean McLaughlin
This module will conduct a simple experiment using the lockin, nanovoltmeter and Hall Probe. There will be a choice on whether or not the user wants to use the Voltmeter or Lockin to 
measure the resistance.I also am going to attempt to use as much functional programming as possible to make the actual experiment be very very simple. 
'''
try:
    import numpy as np
    from matplotlib import pyplot as plt
    from time import clock,sleep
    from Instruments import *
    from config import main, handleInput
    import datetime
except ImportError:
    print 'There was a problem importing the modules; check the PYTHONPATH'
else:
                
    #Using the config module, read the config file specified by the user and assign the objects needed for this experiment. 
    instrumentDictionary = main()
    lockin = LockIn(instrumentDictionary['Lock-in Amplifier'])
    print 'Lock-in linked.'#I've been having a problem here where they take a long time to start. 
    nvm = Voltmeter182(instrumentDictionary['Voltmeter 182'])
    print 'Voltmeter linked.'
    
    try: #most of the module is run inside a try, with a finally that turns off voltage sources and closes files. 
        
        #start with all the function declarations
        def calibrateField(vsource,vport, lockin, fport):
            #takes a reference to a voltage source and a field measuremtn along with the bunit and returns the ratio between field/1V.
            # i am concerned that this should be more general. It will only work with a lockin source for now, and this specific one. 
            vsource.setAuxVoltage(vport,2)
            
            b1 = getBField(lockin, fport) #these two chunks make sure the bfield is nearly steady. 
            b2 = getBField(lockin, fport)
            while (b2-b1)>0.02: #within a tolerance. The analog probe is very fast. I would loosen for the digital one. 
                b2 = b1
                b1 = getBField(lockin, fport)
                sleep(.1)
            bat2 =getBField(lockin, fport)
            
            vsource.setAuxVoltage(vport,1)
            
            b1 = getBField(lockin, fport)
            b2 = getBField(lockin, fport)
            while (b2-b1)>0.02: #within a tolerance.
                b2 = b1
                b1 = getBField(lockin, fport)
            bat1 = getBField(lockin, fport)
            
            vsource.makeSafe(vport)
            return (bat2-bat1)
        
        def getVoltageFromField(field, c):
            return field/c
    
        def getResistance(current):
            return getVoltage()/current
        
        def getBField(lockin, port):
            #i'm not using a hall probe for this experiment so I need to use the analog on the lock in.
            #i am unsure what to do for this function. it depends on how often we'll use this probe; which I think is infrequently
            v = lockin.getAuxVoltageIn(port)
            return v*2 #the voltage is off by a factor of 2. 
        
        def getDataFile():
            #this function gets the data file and affirms that it is valid. 
            print 'What is the name of the file that the data should be written to?'
            dFileName = raw_input('>>>')
            try:
                if dFileName[-4]!='.': #check that there is a valid suffix.
                    raise IOError
                dataFile = open(dFileName, 'w')
                print 'Writing data to %s.'%dFileName
                return dataFile
            except IOError:
                print 'That was not a valid filename; try again.'
                return getDataFile()
        
        #ask the user how they would like the voltage to be read, and define the getVoltage method accordingly. 
        print 'Which instrument should be used to read the voltage?\n1)Lockin\n2)Nanovoltmeter'
        answer = handleInput(['1','2'])
        if answer=='1':
            def getVoltage():
                return lockin.getVoltage()
        else:
            def getVoltage():
                return nvm.getVoltage()
        
        #handling of the data file. 
        dataFile = getDataFile()# get the data file to write to from the user. 
        dataFile.write(str(datetime.date.today())+'\n')#write date
        dataFile.write(lockin.getInitialState()) #write the header
            
        #This is not exception-proof, like the rest of my inputs. I don't know if it's necessary. 
        print 'What is the Max and Min B-field (in kG) and number of data points for this experiment?.'
        #unit = raw_input('Unit>>>') #the hall probe i'm currently using can't be written to. 
        maxField = float(raw_input('Max Field (kG)>>>'))
        minField = float(raw_input('Min Field (kG)>>>'))
        dataPoints = int(raw_input('Number of Data Points>>>'))
    
        #taking the user's input, we get a voltage and stepsize, which we will need to set the field for our measurements. 
        print 'Calibrating...'
        c = calibrateField(lockin, 4, lockin, 3)
        maxV = getVoltageFromField(maxField,c)
        minV = getVoltageFromField(minField, c)
        stepSize = (maxV-minV)/dataPoints
    
        #We conduct the measurement, and write the data to file and a few arrays.
        voltages = np.arange(minV,maxV,stepSize)
        bfields = []
        resistances = []
        times = []
        dataFile.write('\nVoltage (V)\tB-Field (kG)\tResistance (Ohm)\tTime (s)\n')
        print 'Measuring...'
        for volt in voltages:
            lockin.setAuxVoltage(4, volt)#setField() command
            t = clock()
            times.append(t)
            b= getBField(lockin, 3)
            bfields.append(b)
            r = getResistance(.01)
            resistances.append(r)
            dataFile.write('%f\t%f\t%f\t%f\n'%(volt,b,r,t))
        
        #after data collection is complete, close and turn off what we do not need
        lockin.makeSafe(4)
        dataFile.close()
            
        #plot the data
        #i intend to add more plotting to this module.
        print 'Done.'
        plt.figure()
        plt.plot(bfields, resistances, 'bo')
        plt.xlabel('B-Field (kG)')
        plt.ylabel('Resistance (Ohm)')
        plt.title('Resistance as a function of B-Field')
        
        plt.figure()
        plt.plot(voltages, bfields, 'gs')
        plt.xlabel('Voltage (V)')
        plt.ylabel('B-Field (kG)')
        plt.title('B-Field v. Voltage')
        
        plt.show()
        
    finally:
        dataFile.close()#close the file.
        
        for port in xrange(1,5):#turn off the lock in in case of accidental exit. 
            lockin.makeSafe(port)
            if not lockin.checkSafe(port):
                print 'The Lock-in stopped responding. Port %i is still on.'%port