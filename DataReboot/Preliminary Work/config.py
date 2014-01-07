'''
Created on Jun 13, 2013

@author: Sean McLaughlin
this module will contain the functions to read the config file and return the object's addresses, as well as change the configurations. The main function runs all the operations in this file, so
it is the only one of major importance. It returns a dictionary matching the names of the objects to their resAddresses. 
'''

if __name__ == '__main__':
    print''' This is the module that wraps the INST config module. There is aso a GUI interface that handles it, so it is a bit outdated. 
    
    '''

from Instruments import *
import INSTconfig

inDict = instrumentDictionary
#above is a dictionary which matches the name of each instrument to its object.

def readConfig(): 
#this function reads the config file and call the main menu.
    print 'Please enter the filename for the config file.'
    filename = raw_input('>>>')
    try: #see if it's a valid filename in the directory
        lines = INSTconfig.readConfig(filename)
        return mainMenu(filename)# it is, so let's go to the main menu
    except IOError: #there was a problem; ask again.
        print 'That filename was not correct. Please try again.'
        return readConfig()
    
def newConfig():
    #this module will write a new file for the configuration. 
    print 'Please enter the filename for the config file.'
    filename = raw_input('>>>')
    if filename[-4]=='.':
        f = open(filename, 'w')#write a blank file
        f.close()
        y = mainMenu(filename)
        return y
    else:
        print  "That was not a vaild filename."
        return newConfig()

def mainMenu(filename): #This will be the hub of this module. I fell it's mostly self-explanatory.
    #The user, from here, can change an instrument, add an instrument, remove an instrument or continue.
    showLines(INSTconfig.readConfig(filename))
    print 'If you would like to change an instrument enter "C".\nIf you would like to add a new instrument, enter "A".\nIf you would like to remove an instrument, enter "R".\nElse, enter "N".'
    answer = handleInput(['C', 'N','A','R'])
    if answer=='C':
        return changeConfig(filename)
    elif answer=='N':
        x =  getResAds(filename)
        return x
    elif answer=='R':
        return removeInstrument(filename)
    else:
        return addInstrument(filename)

def changeConfig(filename):
    # This will allow the user to change part of the config file. 
    print 'Which instrument would you like to change? Enter its resAd'
    oldAdd = raw_input('>>>')
    
    print 'What is the resource address of the new instrument? Just enter the number.'
    newAdd = raw_input('>>>')

    INSTconfig.editINST(filename, newAdd, oldAdd)
    return mainMenu(filename)

def removeInstrument(filename):
    print 'Which instrument would you like to Remove? Enter its resAddress.'
    add = raw_input('>>>')
    
    INSTconfig.delINST(filename, add)
    return mainMenu(filename)
            
def addInstrument(filename):
    #this function allows the user to add a new instrument to the end of the file. 
    i = 1
    #print all the types of instruments. 
    for key in inDict.keys():
        print "%i) %s"%(i,key)
        i+=1
    print 'Which of the above instrument types would you like to add?'
   
    #get correct input from the use. 
    answers =[]
    for x in xrange(1,i+1):
        answers.append(str(x))
    answer = int(handleInput(answers))
    ttype = inDict.keys()[answer-1]
    
    print 'What is the resource address of the new instrument?'
    resAd = raw_input('>>>')
    
    INSTconfig.addINST(filename, resAd, ttype)
    return mainMenu(filename)

def getResAds(filename):
    #this is the final function of the chain. It returns a dictionary that links the resource addresses of instruments with their names. 
    return INSTconfig.getResAds(filename)

def handleInput(answers):
#this function is passed in a list of acceptable answers from the user. It prompts the user for their answer and returns it if it is acceptable. It asks again if it isn't.
    out = raw_input('>>>')
    for answer in answers:
        if out==answer:
            return out
            break
    else:
        return handleInput(answers)        
    
def getNumInstruments(filename):
    # this function gets the number of instruments in the file by counting the 'END\n's.
    configFile = open(filename, 'r')
    noI = 0
    for line in configFile:
        if line=='END\n':
            noI+=1
    configFile.close()
    return noI

def getLines(filename):
    #this function returns an array of the liens of the file as strings.
    configFile = open(filename, 'r')
    lines = []
    for line in configFile:
        lines.append(line)
    configFile.close()
    return lines

def showLines(lines):
    # this function simply takes the array of lines and prints them. 
    for line in lines:
        print line,

def main(): #the standard function of this file. When importing config, only import and run this. 
    return readConfig()

if __name__=='__main__':#if this module is run on its own, it will print the output of main. otherwise nothing will happen. 
    print main()