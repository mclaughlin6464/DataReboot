'''
7/1/2013
Sean McLaughlin
This is an adjustment of the config.py file. That file works fine, but it needs to be more function-based in order to work with a GUI. 
Also, having a more modular structrue will make it easier to modify it to support regular expressions. 
'''
if __name__ == '__main__':
    print '''This module handles the configuration of he Instrument objects. It is primarily accessed via the INSTconfig_GUI. It's a pretty straightforward module, which
    implements adding, editing, and deleting. The other main funcion of this module is the getResAds method, which returns a dict of the INSTname and it's resource address,
    for creation of INST objects.
    '''

from Instruments import *

inDict = instrumentDictionary
# a dictionary matching the name of an instrument to it's callable object

def addINST(filename, resAd, INSTtype):
    #this function allows the user to add a new instrument to the end of the file. 
    
    #create an object for this new instrument and append it's info to the file, along with a new number. 
    x = inDict[INSTtype](resAd)
    noI = getNumInstruments(filename)
    with open(filename, 'a') as configFile:
        configFile.write("%i\n"%(noI+1)+str(x))

def delINST(filename, resAd):
    #deletes an existing instrument object from the file.
    #this works fine, but It could stand to be updated so that it conforms with the standards set in teh GASconfig module
    lines = readConfig(filename)
    with open(filename, 'w') as INSTfile:
    
        for lineNo in xrange(len(lines)):#read/write lines preceding the name we want to delete. 
            if lines[lineNo+1][:4] == 'Type': #next line has Name in it (don't want to write the preceding numbe
                if parseKeyValue(lines[lineNo+2]) == resAd:
                    break #we found our name, we want to stop writing. 
            INSTfile.write(lines[lineNo])
        
        for i in xrange(lineNo+6, len(lines)): #read/write lines after the name we want to delete. 
            if lines[i-2][:-1]=='END': #this lines a number, cuz the previous line was END
                INSTfile.write(str(int(lines[i][:-1])-1) + '\n') #we want to decrease the number for the remaining ones. 
            else:
                INSTfile.write(lines[i])

def displayINST(filename, resAd):
    #returns the lines of one object. Mostly for displaying on the GUI
    if  not resAd: #sometimes this function gets called with an invalid name. 
        return ''
    #this works fine, but It could stand to be updated so that it conforms with the standards set in teh GASconfig module
    lines = readConfig(filename)
    out = []
    for i in xrange(len(lines)):
        if lines[i][:4] == 'Type':
            if parseKeyValue(lines[i+1]) == resAd:
                break
    if i< len(lines)-3:
        for j in xrange(i,i+3):
            out.append(lines[j])
    return ''.join(out)

def editINST(filename, newResAd, oldResAd):
    #deletes the old instrument and creates a new one. GPIB
    INSTtype = getTypeFromAdd(filename, oldResAd)
    delINST(filename, oldResAd)
    addINST(filename, newResAd, INSTtype)

def getINSTnames(filename):
    #gets the names of the instruments from the file and returns them in a list. 
    lines = readConfig(filename)
    names = []
    for line in lines:
        if line[:4] == 'Type':
            names.append(parseKeyValue(line))
    return names         

def getNumInstruments(filename):
    #returns the number of instruments in the file by counting the appearances of 'END\n'
    lines = readConfig(filename)
    noI = 0
    for line in lines:
        if line=='END\n':
            noI+=1
    return noI

def getResAds(filename):
    #this function reads the file and creates a dictionary pairing the name of an instrument with a resource address
    lines = readConfig(filename)
    
    #so i looked at the commented out code below and I cringed pretty hard. I dont' have time to test this new code but I believe it works faster, better, and more clearly.
    #if there are problems, jsut put the old code back in, but I couldn't stand to leave it as it was without trying to fix it. 
    output = {}
    for index, line in enumerate(lines):
        try:
            int(line.strip())
        except ValueError:#the line is not a number
            continue 
        else: #the line is a number
            output[parseKeyValue(lines[index+1])] = parseKeyValue(lines[index+2]) #snag the name and the address. 
    return output
#     noI = getNumInstruments(filename)
#     output = []
#         
#     numInstRange = range(1, noI+1)
#     strInstRange = []
#     for i in numInstRange:
#         strInstRange.append(str(i))
#         
#     for i in numInstRange:
#         for j in xrange(len(lines)):
#             if lines[j][0] in strInstRange:#if the line is equal to the instrument number we want
#                 output.append((parseKeyValue(lines[j+1]), parseKeyValue(lines[j+2]))) #append a tuple of the name of the instrument with it's address
#     return dict(output)

def getTypeFromAdd(filename, resAd):
    #reads the file to get the type from the resAddress
    lines = readConfig(filename)
    for lineNo in xrange(len(lines)):
        if parseKeyValue(lines[lineNo+1]) == resAd:
            return parseKeyValue(lines[lineNo])

def parseKeyValue(string):
    #returns the string between the equals sign and the newline. 
    #this module if DIFFERENT than the other, (better) parseKeyValues I used in other modules. 
    eq = string.find('=')
    nl = string.find('\n')
    if eq==-1:
        eq = 0
    if nl == -1:
        nl = len(string)
    return string[eq+1:nl].strip()

def readConfig(filename): 
#this function reads the config file and returns the lines of the file. If there is no such file, an 
    lines = []
    with open(filename, 'r') as INSTfile:
        for line in INSTfile:
            lines.append(line)
    return lines