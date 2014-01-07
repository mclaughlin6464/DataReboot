'''
6/26/2013
Sean McLaughlin
This module will handle the file IO for the getAndSet objects. 
'''
if __name__ == '__main__':
    print'''This module handles the file IO for the getAndSet objects. It is accesses primarily through the GASconfigGUI modules, though there is an incomplete text interface as well.
    This module allows adding, deleting, and editing (which simply deletes than adds). There are a few other functions as well, some to inteface easily with the GUI, and others to 
    returns funcitoning objects to a measurement window. For example, the function getsAndSetsFromConfig returns a dictionary of all GAS objects in the file, with pairs of names to
    object reference. 
    '''

from Instruments import *
import getAndSet 

def parseKeyValues(line): # a function that take a string of key value pairs and attempts to split it into a list of length 2. (A tuple would work fine as well)
    pair = line.split('=')
    if len(pair) != 2:
        return None, None #may want to return 2 Nones so the size of the output is consistent. 
    out = []
    for item in pair:
        out.append(item.strip())
    return out

def addGas(GASfilename, INSTFilename,classType, InstrumentType, **kwargs):
    #function that adds a new GAS object to the config file.
    #GASfilename and INSTfilename should be somewhat self explanatory
    #classtype is a string to be used aas a key in the GASdictionary, so that the right constructor can be found
    #similarly with InstrumentType
    #**kwargs is the initialization that is passed into the GAS object; the values allowed should correspond to the object selected. More details in getAndSet.py
    instrumentsDict = getInstrumentsFromConfig(INSTFilename)
    kwargs[getAndSet.instrument] = instrumentsDict[InstrumentType]
    reference = getAndSet.GASdictionary[classType](**kwargs) #create the reference here
    num = numGASObjects(GASfilename)
    
    with open(GASfilename, 'a') as GASfile:#use the reference's __str__ method to write it file easily.
        GASfile.write('%i'%(num+1)+str(reference)+ getAndSet.end)
    
def changeInstrumentConfigFilename(GASfilename, newINSTfilename):
    #simply changes the INSTfilename in the GASfile. This is not terribly necessary, and to be honest a bit sloppy way of handling it
    #The instfilename probably does not need to be stored in the GASfile
    lines, oldFilename = readConfig(GASfilename)
    
    for index, line in enumerate(lines):
        if line.find('Instrument ConfigFile') != -1:
            lines[index] = 'Instrument ConfigFile = '+newINSTfilename + '\n'
            break
        
    with open(GASfilename, 'w') as outFile:
            outFile.write(''.join(lines))
    
def delGas(filename, name):
    #delete a  GAS object from the file
    #filename is the getAndSetfilename
    #name is the name of the GASobject to be deleted.
    
    lines, garbage = readConfig(filename)
    del(garbage)
    out = [] #a list of lines, that will be joined together later. 
    write = True
    instNum = 1
    for line in lines:
        try: #first check: if this line's a number
            int(line.strip())
        except ValueError:
            pass #this line isn't a number
        else:
            out.append(str(instNum)+ '\n') #this line is a number, write the correct number and iterate the number. 
            instNum+=1
            continue #go onto the next step of the loop. 
        key, value = parseKeyValues(line)
        if  key == getAndSet.GASname:
            if value == name:
                write = False
                del(out[-1]) #delete the preceding number
                instNum-=1
            else:
                write = True
        if write: #if we are allowed to write the line, put it in the array. 
            out.append(line)
            
    with open(filename, 'w') as GASfile:
        GASfile.write(''.join(out)) #joining an array of lines is faster than both writing line by line and adding them together to one large string. 
    
def displayGAS(filename, name):
    #returns the lines of one object. Mostly for displaying on the GUI
    if not name: #sometimes this function gets called with an invalid name. 
        return ''
    
    lines, garbage = readConfig(filename)
    del(garbage)
    out = [] #list of lines to be joined into a string. 
    for index, line in enumerate(lines):
        key, value = parseKeyValues(line)
        if key == getAndSet.GASname and value == name: #we've found our line
            break
    else: #if we don't find our name, return nothing. 
        return ''
        
    for line in lines[index:]: #start adding lines to the display. 
        if line==getAndSet.end: #if the line is the end of the object , break. 
            break
        out.append(line)
    return ''.join(out)

def editGAS(GASfilename, INSTFilename, oldName, classType, InstrumentType, **kwargs):
    #simply deletes the old object and creates a new one. 
    #GASfilename and INSTfilename are self-explanatory
    #oldName is the name of the object ot be deleted
    #classType and INSTtype are the same as in addGAS
    #kwargs is the set of attributes to pass onto the new GAS object (the new name is in here)
    delGas(GASfilename, oldName)
    addGas(GASfilename, INSTFilename, classType, InstrumentType, **kwargs)
    
def getGASattributes(filename, name):
    #returns a dictionary of the attributes of one GAS object
    
    attr = {}
    lines = displayGAS(filename, name).split('\n') #make a list of the lines.
    for line in lines:
        key, value = parseKeyValues(line) #get the key value pair
        if key == getAndSet.delay or key == getAndSet.delay2:
            attr[key] = value.split(' ')[0] #the delays require special treatment 
        elif key is not None:
            attr[key] = value #assign the pair if there is one. 
    return attr

def getGASNames(filename):
    #returns a list of all the names of the objects in the file
    #best used in conjunction with displayGAS
    lines, garbage = readConfig(filename)
    del(garbage)
    names = []
    for line in lines:
        key, value = parseKeyValues(line)
        if key == getAndSet.GASname:
            names.append(value)
    return names         

def getInstrumentsFromConfig(INSTFilename):
    #opens the INSTconfigfile and returns a dictionary with the instrument name and a reference to it. 
    #this function is a little bit out of place in this module. 
    
    from INSTconfig import getResAds
    addressDictionary = getResAds(INSTFilename)
    instruments = {}
    for name, address in addressDictionary.iteritems(): 
        instruments[name] = (instrumentDictionary[name](address))
        #this line is a bit messy. We take the instrument Name and from the instrumentDictionary of constructors we make a reference. 

    return instruments
    #this may not work if there is more than one of an isntrument in a set. 
    
def getsAndSetsFromConfig(GASfilename):
    #reads the config file and returns  a tuple of the GASdictionary and an INSTdictionary
    #more specifically it returns a dictionary with the name as the key and returns a reference to the object in the config file.
    #it also returns the instrument dictionary used with these objects
    lines, instrumentFilename = readConfig(GASfilename)
    instrumentDictionary = getInstrumentsFromConfig(instrumentFilename)
    
    namesAndKwargs = {} #this dictionary will use the name of the object as the key, and a dictionary of the kwargs as the values. This will be used to make the references
    for index, line in enumerate(lines):
        key, name  = parseKeyValues(line)
        if key == getAndSet.GASname: #we've found a new object
            namesAndKwargs[name] =  kwargs = {getAndSet.GASname:name} #start the kwargs dict with the name
            for line in lines[index:]:
                key, value = parseKeyValues(line)
                if key is not None:
                    kwargs[key] = value #set up the key value pair
                else:
                    break #onto the next instrument
    #we have to convert the instrument names to actual instrument references. 
    #this is also where cleanup of certain inputs is done. 
    for kwargs in namesAndKwargs.itervalues():
        INSTname = kwargs.pop(getAndSet.instrument)
        add = kwargs.pop(getAndSet.add)
        kwargs[getAndSet.instrument] = instrumentDictionary[INSTname] #make an actual INST reference
        
        if getAndSet.delay in kwargs: #clean up the delay
            delay = kwargs.pop(getAndSet.delay)
            delaySplit = delay.split(' ')
            kwargs[getAndSet.delay] = delaySplit[0]
            kwargs[getAndSet.TCM] = len(delaySplit) != 2 #it either is a number followed by 'seconds' or 'multiples of the time constant'. easier to check lenght. 
        
        if getAndSet.delay2 in kwargs:
            delay2 = kwargs.pop(getAndSet.delay2)
            delay2Split = delay2.split(' ')
            kwargs[getAndSet.delay2] = delay2Split[0]
            kwargs[getAndSet.TCM2] = len(delay2Split) != 2 #it either is a number followed by 'seconds' or 'multiples of the time constant'. easier to check lenght. 
                
        if getAndSet.cal in kwargs: #remove the unit from the cal
            kwargs[getAndSet.cal] = kwargs[getAndSet.cal].split(' ')[0] #get the first term, the number
            
        if getAndSet.OCR in kwargs: #remove the unit from the OCR
            kwargs[getAndSet.OCR] = kwargs[getAndSet.OCR].split(' ')[0]
                
    OUTdict = {}
    resistanceNames = [] # we can't make the resistance objects until the rest of dict is made because we need the rerences
    for name, kwargs in namesAndKwargs.iteritems():
        OUTdict[name] = getAndSet.GASdictionary[kwargs[getAndSet.classType]](**kwargs) #assign the new getAndset type (of the determined class type) into the dict. 
            
    for name in resistanceNames: #now, do the getResistance objects.
        kwargs = namesAndKwargs[name]
        kwargs[getAndSet.gV] = OUTdict[kwargs[getAndSet.gV]] #change the strings that reperesent names to references to the objects. 
        kwargs[getAndSet.gC] = OUTdict[kwargs[getAndSet.gC]]
        OUTdict[name] = getAndSet.GASdictionary[kwargs[getAndSet.classType]](**kwargs)
        
    return OUTdict, instrumentDictionary

def numGASObjects(filename):
    #counts the number of instruments already in the file by counting the appearances of END
    lines, garbage = readConfig(filename)
    del(garbage) #same story as above; not necessary but the warning was annoying. 
    count = 0
    for line in lines:
        if line== getAndSet.end:
            count+=1
    return count

def readConfig(GASfilename):
    #takes a filename and attempts to read it. If it succeeds, it returns a tuple.
    #the first element is all the lines of the file in a list. the second is the name of the instrument config file, the first element of this file. 
    #if it fails, it raises an error.

    lines = []
    with open(GASfilename, 'r') as GASfile:
        for line in GASfile:
            lines.append(line)
    
    return lines, lines[1][24:-1]
    #returns a tuple. The first element is an array of lines. The second is the name of the config file where the instruments are. 
