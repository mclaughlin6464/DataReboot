'''
6/26/2013
Sean McLaughlin
A helper function for GASconfig that allows text input. 
'''

if __name__ == '__main__':
    print ''' A command line wrapper for GASconfig.py There is a GUI that works with it as well, which is the reccomended way to handle it. This is outdated and doesn't contain 
    updates that have been made. 
    '''

from GASconfig import *

def mainMenu(filename):
    #nexus of the program; the GUI takes control of this later.
    from config import handleInput
    lines, CFN =readConfig(filename)
    
    for line in lines: #show the lines and ask for input
        print line,
    print '\nAdd : A\nDelete : D\nShow: S\nExit : E\n'
    answer = handleInput(['A', 'D','S', 'E'])
    if answer == 'A':
        a(filename, CFN)
    elif answer=='D':
        d(filename)
    elif answer=='S':
        s(filename, raw_input('Name?>>>'))
    else: #E
        return

def a(GASfilename, ConfigFilename):
    #get user input and call the addGas function
    from config import handleInput
    name = raw_input('Name>>>')
    print 'ClassType'
    classType= handleInput(GASdictionary.keys())
    print 'InstrumentType'
    InstrumentType = handleInput(instrumentDictionary.keys())
    ttype = raw_input('Type>>>')
    port = raw_input('Port>>>')
    if ttype=='None':
        ttype = None
    if port == 'None':
        port = None
    else:
        port = int(port)
    addGas(GASfilename, ConfigFilename, name, classType, InstrumentType, ttype, port)
    mainMenu(GASfilename)
    
def d(filename):
    #gets user input and runs delGas
    name = raw_input('Name to Delete>>>')
    delGas(filename, name)
    mainMenu(filename)
    
def s(filename, name):
    out = displayGAS(filename, name)
    print out
    mainMenu(filename)

if __name__ == '__main__':
    filename = raw_input('Filename?>>>')
    mainMenu(filename)
    print getsAndSetsFromConfig(filename)