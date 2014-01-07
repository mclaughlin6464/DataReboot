'''
Created on Jun 7, 2013

@author: Sean McLaughlin
This is my first module coded in the lab. I'm going to try to work with a few moving pieces and operate a few instruments. 
The program steps the output from the lock-in my 10mV from 0V to 5V. This voltage is proportional to the field strength of the magnet, which is measured by 
the Gauss probe. I've implemented some convuluted safety features which may be unecessary.  
'''
try:
    import numpy as np
    from matplotlib import pyplot as plt
    import visa
    import time
except ImportError:
    print "There was a problem importing the files; check the PYTHONPATH"
else:
    
    resAddresses = visa.get_instruments_list() #Get all the resource addresses
    #as far as I can tell, we will need to use the adresses as starter data, because I don't know how to tell what instrument is which from the address
    #I could use *IDN? to get the model number and maybe use that but I'm not sure if that's a good idea.
    #the Gauss probe is GPIB0::12 at present, and the Lock-in is GPIB0::24 at present.
    hallp = visa.Instrument(resAddresses[3])
    lockin = visa.Instrument(resAddresses[6])
    
    safe = True #Boolean to see if device is on or off
    
    try:
        
        def splitRTheta(both, R, T): #This function comes into play for splitting the r and theta string into 2 things
            for s in both:
                commaIndex = -1
                for i in xrange(len(s)):
                    if s[i]==',':
                        commaIndex = i
                        break
                R.append(float(s[:commaIndex]))
                T.append(float(s[commaIndex+1:]))
            
            
        def handleInput(char):# Get input from the user, returns boolean
            if char=='Y':
                return True
            elif char=='N':
                return False
            else:
                print "I think you must have mistyped. Try again.\nRemember, only 'N' and 'Y' are valid responses."
                char = raw_input(">>>")
                return handleInput(char)
                
                
        def checkSafe(lockin):#Returns Boolean. Checks if the lockin is off or not. 
            out = float(lockin.ask("OAUX? 4"))
            if out<.01:
                return True
            else:
                return False
            
        def makeSafe(lockin, safe):
            i = 0
            while safe==False:
                rampDownV(lockin)
                safe = checkSafe(lockin)
                i+=1
                if i==10:
                    raise ImportError
                return safe #This will quickly allow us to exit the program. 
                
        def rampDownV(lockin):
            v = float(lockin.ask("AUXV? 4"))
            while v > .01:
                v = v*.9
                lockin.write("AUXV 4,%f"%v)
            lockin.write("AUXV 4, 0")
        
        hallp.write("UNIT 1;AUTO 1") #Reset readings to Gauss and turns Auto Range on
        #I'm not sure if these are a good idea but I'll figure that out. 
        
        print "Would you like to recalibrate the Gauss probe?\nIf so, put a shield on the probe and enter 'Y'.\nElse, enter 'N'"
        answer = raw_input(">>>")
        if handleInput(answer):
            hallp.write("ZPROBE")
            print "Calibrating..."
            time.sleep(30)
            print "Done calibrating, please remove the cover."
            #Might want to give more time to remove the cover.
            time.sleep(5)
        print "Ok, beginning measurement."
        #The above exchange is pretty self explanatory
        
        bfields = []
        randtheta = []
        voltages = np.arange(0,1.01,.01)
        
        safe = False
        for volt in voltages: #This loop will step the voltage and sample the corresponding field. 
            lockin.write("AUXV 4,%f"%volt)
            time.sleep(.1) # I want to be sure the instruments sync up.
            bfields.append(float(hallp.ask("RDGREL?")))
            randtheta.append(lockin.ask("SNAP? 3,4")) #These are returned in one string; I'll need to do some post on em. 
        
        makeSafe(lockin, safe)# Ensure the lockin is off. 
            
        print "Measurement complete. Take a look at the plot!"
            
        rvalues = []
        thetas = []
        splitRTheta(randtheta, rvalues, thetas) #Separate the R's and T's
        
        #Now I'll move onto doing the plot
        plt.figure(1)
        plt.subplot(211)
        plt.plot(voltages, bfields, 'gs')
        plt.ylabel("B-field (G)")
        plt.title("B-field v. Voltage")
        
        plt.subplot(212)
        plt.plot(voltages, thetas, 'ro')
        plt.ylabel("Theta (Deg)")
        plt.title("Theta v. Voltage")
        
        plt.xlabel("Voltage (V)")
        
        plt.show()
        
    finally: #This snippet will ensure that the lockin is turned off if there is a problem somewhere in the code. 
        if safe==False:
            i = 0
            while safe==False:
                rampDownV(lockin)
                safe = checkSafe(lockin)
                i+=1
                if i==10:
                    print "The lock-in is not responding. Please turn it off manually."
                    break
            else:
                print "There was a problem with the code; the program has been exited safely."