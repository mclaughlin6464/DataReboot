'''
Created on Jun 11, 2013

@author: Sean McLaughlin
I'm attempting to get the plots of the data to animate live. So far, it appears to not be working. 
'''

try:
    import numpy as np
    from matplotlib import pyplot as plt
    import matplotlib.animation as animation
    from time import clock,sleep
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
        bfields = [[0],[0]]
        resistances = [0]
        times = [0]# each of these arrays will hold the values we measure through the for loop
        
        dataFile.write("\nB-Field (G)\tResistance (Ohm)\tVoltage (V)\tTime (s)\n")
        #^^^Write the top of the file in. I don't know if this format works with origin; it'll work for now though. 
        
        def updateLineAndMeasure(num,volt,bfields,lockin, line):
            lockin.setAuxVoltage(4, volt*num)
            bfields[0].append(volt*num)
            b = float(hallp.getBField())
            bfields[1].append(b)
            line.set_data(bfields)
            sleep(.1)
            return line,
        
        #below all I'm doing is plotting the data. 
        
        fig1 = plt.figure(1)
        l1, = plt.plot(bfields, 'g-', lw=2)
        plt.ylabel("B-field (G)")
        plt.xlabel("Voltage (V)")
        plt.title("B-field v. Voltage")
        plt.axis([0,5,-500,500])
        line1_ani = animation.FuncAnimation(fig1, updateLineAndMeasure, frames=100, fargs=(.01, bfields, lockin,l1), blit=True)
            
            
        plt.show()
        
    finally:
        if not dataFile.closed: #close open files one exit
            dataFile.close()
            
        for port in xrange(1,5):
            try:
                lockin.makeSafe(port) #turn off every port
            except lockin.LabInstrumentError:
                print "The Lock-in stopped responding. Port %i is still on."%port
