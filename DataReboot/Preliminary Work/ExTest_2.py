'''
Created on Jun 11, 2013

@author: Sean McLaughlin
I'm rewriting the ExTest module to use the Instruments module objects to try and abstract the procedure a little more. 
'''

try:
    import numpy as np
    from matplotlib import pyplot as plt
    from time import clock
    import Instruments
except ImportError:
    print "There was a problem importing the modules; check the PYTHONPATH"
else:
    
    
    
    #All this I get the input from the user. It's a major pain in the ass of string manipulation. 
    try:
        print "Below is the configuration for this experiment. If you would like to change it enter 'Y'."
        configFile = open('config.txt', 'r')
        configLines = []
        for line in configFile:
            configLines.append(line)
            print line,
            
        change = raw_input(">>>")
    except:
        print "There is no config file."
        change = 'Y'
        
    while change=='Y':
        try:
            print "What is the resource address of the Hall Probe for this experiment?"
            print "Enter in the form of 'GPIB0::XX'"
            hAdd = raw_input(">>>")
            hallp = Instruments.HallProbe(hAdd)
            
            print "What is the resource address of the Lock-in for this experiment?"
            print "Enter in the form of 'GPIB0::XX'"
            liAdd = raw_input(">>>")
            lockin = Instruments.LockIn(liAdd)
            
            configFile = open('config.txt', 'w')
            configFile.write(str(hallp)+str(lockin))#Save this configuration to the config file so it doesn't need ot be changed. 
            configFile.close()
        except:
            print "There was a problem with your inputs. Using the ones in the config file. Would you like to use the config file?"
            change=raw_input('>>>')
        
    else: #This is very dependent on what the layout of the config file is. 
        hAdd = configLines[3][19:-1]
        hallp = Instruments.HallProbe(hAdd)
        liAdd = configLines[7][19:-1]
        lockin = Instruments.LockIn(liAdd)
        configFile.close()
        
        
    
    lockin.clear()
    hallp.clear()
    
    print "What is the name of the file that you would like the results to be written to? Please remember to include the suffix."
    name = raw_input(">>>")
    name = "data.txt"
    dataFile = open(name, 'w') #get the file to write the data to. 
    #write the header
    dataFile.write(lockin.getInitialState())
    
    #Make sure the lockin is off at all ports. 
    for i in xrange(1,5):
        lockin.makeSafe(i)
    
    print "Beginning measurement..."
    
    try: 
        hallp.setBUnit(1) #Set the units on the hall probe to Gauss
        bfields = []
        resistances = []
        times = []# each of these arrays will hold the values we measure through the for loop
        voltages = np.arange(0,1.01,.01)
        
        dataFile.write("\nB-Field (G)\tResistance (Ohm)\tVoltage (V)\tTime (s)\n")
        #^^^Write the top of the file in. I don't know if this format works with origin; it'll work for now though. 
        
        for volt in voltages:
            lockin.setAuxVoltage(4, volt)
            b = float(hallp.getBField())
            bfields.append(b)
            R,T= lockin.getRandT() #get the first part of the tuple, the magnitude
            r = R*100
            resistances.append(r) #Multiply by 100 to get the resistance
            t = clock()
            times.append(t)
            #I don't know how long these appends take v. standard assignments. Worth considering. 
            dataFile.write("%.9e\t%.9e\t%.9e\t%.9e\n"%(b,r,volt,t))
            
        lockin.makeSafe(4)
        
        dataFile.close()
        
        print "The measurement is done. Take a look at the plots!"
        
        #below all I'm doing is plotting the data. 
        
        fig1 = plt.figure(1)
        plt.plot(voltages, bfields, 'gs')
        plt.ylabel("B-field (G)")
        plt.xlabel("Voltage (V)")
        plt.title("B-field v. Voltage")
            
        plt.figure(2)
        plt.plot(bfields, resistances, 'bo')
        plt.ylabel("Resistance (Ohms)")
        plt.title("Resistance v. B-Field")
        plt.xlabel("B-Field (G)")
        
            
        plt.show()
        
    finally:
        if not dataFile.closed: #close open files one exit
            dataFile.close()
            
        for port in xrange(1,5):
            try:
                lockin.makeSafe(port) #turn off every port
            except lockin.LabInstrumentError:
                print "The Lock-in stopped responding. Port %i is still on."%port
