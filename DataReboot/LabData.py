'''
8/2/2013
Sean McLaughlin
This module contains the LabData object, which is an object that handles all the data storage, manipulation, and writing for the measurement. 
'''

if __name__ == '__main__':
    print''' This module contains the labdata object, which handles all of the writing, storage, and manipulation of the data. I also planned to include the ability to 
    read data from existing files, but never got around to it. 
    '''

from os.path import isfile
import thread
import copy
import numpy as np
from itertools import izip

class DataError(Exception):# an error for the object to raise
    
    def __init__(self, value = None):
        self.value = value
        
    def __str__(self):
        if self.value is not None:
            return str(self.value)
        return 'There was a problem with the data, raised by the LabData Object'

class LabData(object):
    
    def __init__(self, nData, nSet, dataFilename):
        #nData and nSet denote the number of columns for the data and the setters respectively
        #dataFilename is self explanatory
        #*n
        self.__data__ = [[] for i in xrange(nData)] #the master data list.
        self.__sets__ = [[] for i in xrange(nSet)] #the parralel tree to __data__ that corresponds to all the values the instruments were set at. 
        self.mainLock = thread.allocate_lock() # a lock to protect the main tree
        self.nData = nData
        self.lastDataIndexWritten = 0
        self.dataFileName = dataFilename
        
        #these variables are used for making the list of mapping dictionaries. 
        self.mapsList = [{} for i in xrange(nSet-1)] #there is no map for the first sweep
        self.mapsIndicies = [ 0 for i in xrange(nSet-1)]
        
        #these variables are for the data_to_array functions
        self.pseudoArray = []
        self.columnsIndiciesandSlices = [-1, -1, -1, None] # the x, y and z columns of the image, and the slicing dict
        self.coordinateDicts = [] # a list holding all the dicts that map to coordinates in the  image
        self.lastDataIndexArray = 0 # he last data Index inserted into the array
        self.arrayLock = thread.allocate_lock() # a lock object to control access to the pseudoarray
        self.miscLock = thread.allocate_lock() # a lock to control access to the other variables used to make the array
        
    def __copy__(self):
        #returns a shallow copy of the object. Fast, but it's possible to change the main data tree with this; don't use if you will be doing anything other than reading
        Copy = LabData(self.nData, self.dataFileName)
        Copy.lastDataIndexWritten = self.lastDataIndexWritten
        with self.mainLock:
            Copy.__data__ = copy.copy(self.__data__)
            Copy.__set__ = copy.copy(self.__sets__)
        return Copy
        
    def __deepCopy__(self, memo):
        #returns a deep copy. Slower, but is able to edited freely
        Copy = LabData(self.nData, self.dataFileName)
        Copy.lastDataIndexWritten = self.lastDataIndexWritten
        with self.mainLock:
            Copy.__data__ = copy.deepcopy(self.__data__)
            Copy.__set__ = copy.deepcopy(self.__sets__)
        return Copy
        
    #the getitem and setitem overrides correspond to the data list. it would be easy to make it correspond to the set array instead, and possible to make it do both in some fashion. 
    
    def __getitem__(self, key): # i may want to make this return a row
        with self.mainLock:
            if key < self.nData:
                return self.__data__[key]
            else:
                return self.__sets__[key-self.nData]
    
    def __setitem__(self, key, value):# i don't know if this will be used at all but I think for symettry's sake I'll leave it. 
        with self.mainLock:
            if key<self.nData:
                self.__data__[key] = value
            else:
                self.__sets__[key-self.nData] = value
    
    #iteration over the object performs the same fucntion as iterating over the list. 
    def __iter__(self):
        self.iteratorIndex = 0
        return self
    
    def next(self):
        if self.iteratorIndex == len(self):
            raise StopIteration
        
        else:
            return self[self.iteratorIndex]
            self.iteratorIndex +=1
        
#this code allows the user to iterate over the rows. I don't know if that's too confusing, so i'm going to leave a standard iterator in.
#     def __iter__(self): # the iterator overload. When stepping through the data, returns tuples of rows
#         self.iteratorIndex = 0 
#         return self
#     
#     def next(self):
#         if self.iteratorIndex == len(self):
#             raise StopIteration
#         else:
#             output = []
#             for column in self.__data__:
#                 output.append(column[self.iteratorIndex])
#             self.iteratorIndex+=1
#             return tuple(output)
        
    def __len__(self): #the len() function correspondes to the number of rows, NOT the number of columns. 
        with self.mainLock:
            return len(self.__data__[0])
    
    def addData(self, *args):
        #accepts either a set of lists or a set of values. The number of values input must be the same as the number of total columns or there will be an error
        #the data should be first, followed by the set values
        #it the input is lists, it extends the data by those values
        #if they are values, they are appended
        #i.e. the addition is optimized for what type of input is sent in. 
        
        if len(args) != self.nData + len(self.__sets__): #the user cannot input more or less values than there are columns in the data
            raise DataError, 'Attempted to append a number of arguements unequal to the number of columns.'
        
        try:
            iterator = iter(args[0])#attempt to iterate over the object, and take note of it's type
        except TypeError:
            isIterator = False
        else:
            isIterator = True
            
        if self.__sets__[0]: #get the previous values input; if there are not previous values (data is empty), put in None references
            lastValues = []
            for col in self.__sets__[1:]:
                lastValues.append(col[-1])
        else:
            lastValues = [ None for i in xrange(len(self.__sets__)-1)]
            
        if isIterator:
            for i in args: #the input must also all be of the same type. 
                if any(type(i) != type(j) for j in args):
                    raise DataError, 'There was a type mismatch in the inputs.'
            
            #put the data into the main lists
            with self.mainLock:
                for dataColumn, argsCol in izip(self.__data__, args[:self.nData]):
                    dataColumn.extend(argsCol)
                    
                for setColumn, argsCol in izip(self.__sets__, args[self.nData:]):
                    setColumn.extend(argsCol)
            
            skip = self.nData + 1 #skip all the data columns and the first set column. use this to avoid doing the calculation over and over. 
            for col in xrange(len(lastValues)):
                for row in xrange(len(args[col+skip])): #the first 2 elements of args do not have maps, so they are skipped over
                    if lastValues[col] != args[col+skip][row]: #check if the last value is the same or different then the current one. 
                        self.buildEnd(col, lastValues[col])
                        self.buildStart(col, args[col+skip][row])#end building a map for the last value and start a new set for the new one
                    else:
                        self.buildPass(col, lastValues[col])#keep incrementing the present value. 
                    lastValues[col] = args[col+skip][row] #transfet the value to the most recent holder. 
                
        else: #not an iterator; use append. 
            with self.mainLock:
                for  dataCol, arg in izip(self.__data__,args):
                        dataCol.append(arg) #put the input inot the main data tree
                for setCol, arg in izip(self.__sets__, args[self.nData:]):
                        setCol.append(arg)
                    
            skip = self.nData + 1
            for col in xrange(len(lastValues)): 
                if lastValues[col] == args[col+skip] and args[col+skip] is not None: #the fist 2 elements of args do not have maps; they are skipped. Also, check if the new value is different from teh last one. 
                    self.buildPass(col, lastValues[col])#keep incrementing the present value
                else:
                    self.buildEnd(col, lastValues[col]) #finish the last one and start the new one
                    self.buildStart(col, args[col+skip])
            lastValues = args[skip:] #update the most recent holder. 
                
    def buildStart(self, column, value):
        #this and the following 2 functions are used to generate the dictionaries in mapList that indicate where certain values are in the data.
        #this one in particular creates a key to the value if it doesn't exist, and append's a list with the current index and end. 
        dict = self.mapsList[column]
        if value not in dict: 
            dict[value] = [] #create the array if none exists
        dict[value].append([self.mapsIndicies[column], self.mapsIndicies[column]]) #append the values that we know this value exists, and update counter. 
        self.mapsIndicies[column]+=1
        
    def buildEnd(self, column, value):
        #this and the the 2 neighboring functions are used when mapping out the values are for slicing. 
        #this one adjusts the final value and converts the list to a tuple, to help with finality. 
        if value is None: #None can be passed in at first but should be ignored. 
            return
        dict = self.mapsList[column]
        coord = dict[value][-1]
        coord[1] = self.mapsIndicies[column] #may be uncessary; check later if coord[1] is already the right index. 
        dict[value][-1] = tuple(coord) #reassign as a finished tuple. 
        
    def buildPass(self, column, value):
        # this and the preceding 2 functions are used when building the mapping dictionary
        #this one only increments the indicies that the mapping function is on. 
        self.mapsIndicies[column]+=1
        dict = self.mapsList[column]
        coord = dict[value][-1]
        coord[1] = self.mapsIndicies[column] #increment the last value. 
                
    def data_to_array(self, xColi, yColi, dataColi, **slices):
        #reformats the data from a list to numpy array.
        #i'd like to find a way to do this operation in a new thread. 
        oldXColi, oldYColi, oldDatColi, oldSlices = self.columnsIndiciesandSlices
        data, sets = self.parse_data_map(twoLists = True, **slices) #return a copy of the data adn the sets, with the slices. 

        data = data[dataColi] #get columns from the arrays, since that's all we need to work with .
        xCol = sets[xColi]
        yCol = sets[yColi]

        if oldXColi == xColi and oldYColi == yColi and oldDatColi == dataColi and slices == oldSlices:
            #we can use the old pseudo arr
            newData = data[self.lastDataIndexArray:] # slice off only the new, relevant part.
            newXCol = xCol[self.lastDataIndexArray:]
            newYCol = yCol[self.lastDataIndexArray:]
                
            thread.start_new_thread(self.data_to_array_thread_old, (newData, newXCol, newYCol))
        else:
            #it's a new image; we'll need to make some new variables. 
            self.pseudoArray = []
            self.columnsIndiciesandSlices = [xColi, yColi, dataColi, slices] #update the most recent holder. 
            self.coordinateDicts = []
            thread.start_new_thread(self.data_to_array_thread_new, (data, xCol, yCol))
        self.lastDataIndexArray = len(data)
        from time import sleep #allow the threads time to get the locks in place. 
        sleep(.1)
        return self.get_array()
            
    def data_to_array_thread_new(self,data, xCol, yCol):
        #this method is called in a thread when an entireley new image needs ot be generated from the data. 
        #it is importnat that the self variables used in this function are not reassigned to new addresses; the manipulation of them will not work. 
         # the order is switched because that is the order they are accessed in the array i.e. first column is y second is x
        #it'd be possibel to add a custom data column
        
        with self.arrayLock: #lock to protect the main array. 
            columns = [yCol, xCol]
            with self.miscLock: # this is the lock for the psudoe array; while this si going, it can't be accessed
                #this lock does make some threading things a bit slower; it could be moved up to right before the first called to self.pseudoArray
                #having it here gurantees that when get_array is called, it gets a finished array
                
                self.coordinateDicts.extend({} for i in xrange(2)) # will be a list of dictionaries holding the coordinates to map to for the 2 columns.
                
                for column, dictionary in izip(columns, self.coordinateDicts): #make the mapping dictionaries
                    i = 0
                    for setValue in column:
                        if setValue not in dictionary:
                            dictionary[setValue] = i
                            i+=1
                            
            arr = 0
            for dictionary in self.coordinateDicts:
                arr = [copy.deepcopy(arr) for i in xrange(len(dictionary)) ] # make the array
            
            self.pseudoArray.extend(arr) # add in this array of 0's to our old memory location
            
            for i in xrange(len(xCol)):
                coordinates = [] # this array will hold the data coordinates for this point
                for column, dictionary in izip(columns, self.coordinateDicts):
                    coordinates.append(dictionary[column[i]])
                point = self.pseudoArray
                
                for coordinate in reversed(coordinates[1:]): # we need to work through them backwards; also, the last value requires special assignment
                    point = point[coordinate]
                point[coordinates[0]] = data[i]
                    
    def data_to_array_thread_old(self,data, xCol, yCol):
        #this method is called in a thread when we can reuse some of the last image. 
        #it is important that self variables not be assigned to new addresses, or their changes will not work
 #the order is switched because that is their order in the array
            
         #so we can identify which column has been changed
        with self.arrayLock:
            changedColumn = None
            columns = [yCol, xCol]
            with self.miscLock:
                #this lock does make some threading things a bit slower; it could be moved up to right before the first called to self.pseudoArray
                #having it here gurantees that when get_array is called, it gets a finished array
                for column, dictionary in izip(columns, self.coordinateDicts):
                    i = max(dictionary.values()) +1 # i is the maximum coordinate given plus one
                    for setValue in column:
                        if setValue not in dictionary:
                            dictionary[setValue] = i
                            i+=1
                            changedColumn = column
            if changedColumn is not None: # if it has been changed in a way that we need to add new columns
                if changedColumn is columns[1]: #changedColumn == xCol i.e. we added more x values
                    addition = [[ 0 for i in xrange(len(self.coordinateDicts[0]))] for j in xrange(len(self.coordinateDicts[1]) - len(self.pseudoArray))]
                    self.pseudoArray+=addition
                else: #changed == yCol i.e. we added more y values
                    addition = [[0 for i in xrange(len(self.coordinateDicts[0]) - len(self.pseudoArray[0]))] for j in xrange(len(self.coordinateDicts[1]))]
                    for arrRow, additionRow in izip(self.pseudoArray, addition):
                        arrRow += additionRow
                    #it took me a great deal of trial and error to get these to work out right. they're messy but they work
        
            for i in xrange(len(data)):
                coordinates = []
                for column, dictionary in izip(columns, self.coordinateDicts):
                    coordinates.append(dictionary[column[i]])
                    
                point = self.pseudoArray
                for coordinate in reversed(coordinates[1:]): # we need to work through them backwards; also, the last value requires special assignment
                    point = point[coordinate]
                point[coordinates[0]] = data[i]
                
    def get_array(self):
        #returns the numpy array of self.pseudoArr
        with self.arrayLock:
            out = np.array(self.pseudoArray)
        return out
                
    def parse_data_map(self, twoLists = False, **kwargs): #TODO: implement checks that valid kwargs are input. Also, using search for key = 1
        
        if not kwargs: #if kwargs is empty, return a copy of the whole array
            with self.mainLock:
                data = copy.copy(self.__data__)
                sets  = copy.copy(self.__sets__)
            if twoLists: #if twolists, return a tuple of 2 lists (duh) otherwise, return one large list. 
                return data,sets
            else:
                return data+sets
        #i'm writing 2 versions of this function. One searches for the values explicitly, and this one uses a dictionary map. 
        #self.mapList holds a list of dictionaries, where each dictionary maps a  value to the indices where that value is. 
        #kwargs holds key value pairs, where the key is sweep number and the value is the value to slice in that loop
        indicies = [] # a list of all the lists of indicies for the values
         
        for key in kwargs.keys(): #change the keys from strings to integers
        #the use of kwargs.keys is deliberate. NEVER iterate over a dict itself and mutate it at the same time. 
            kwargs[int(key)] = kwargs[key]
            del kwargs[key]
        skip = self.nData + 1 # the data columns and the first sweep don't have a map. 
        for key in xrange(max(kwargs.keys()), 1, -1): #go through all the sweep numbers. If one was not given, assign it's indicies to those above it. 
            if key not in kwargs: #this sweep number was not specified
                indicies.insert(0, indicies[0]) #copy the range of the preceding key
            elif kwargs[key] not in self.mapsList[key-skip]: # the user asked for a key that isn't in the map yet. 
                
                for mapPoint in self.mapsList[key-skip]:#try rounding to one decimal place. THIS MAY BE TOO SLOPPY
                    if round(kwargs[key] ,1 )-round(mapPoint, 1) == 0:
                        indicies.insert(0, self.mapsList[key-skip][mapPoint])
                        break
                else:# return a blank array if the number is too far off. 
                    if twoLists:
                        return [[] for i in xrange(self.nData)], [[] for i in xrange(len(self.__sets__))]
                    else:
                        return [[] for i in xrange(self.nData+ len(self.__sets__))] 
                
            else:
                indicies.insert(0, self.mapsList[key-skip][kwargs[key]]) #get the list of indicies from the map 
                 
        #cycles through the set of indicies and finds which of the current indicies fit 'inside' the previous ones
        #we slowly cut down what indicies to slice through
        #for example, if the validIndicies start with (0,50), and the next set has (5,10) and (55, 60), the next validIndicies will be (5,10)
        validIndicies = indicies[-1] #the largest set of indicies is the first group of valid ones
        for indiciesList in reversed(indicies[:-1]):
            temp = []
            for prevStart, prevStop in validIndicies:
                for start, stop in indiciesList:
                    if (prevStart<=start<=prevStop) and (prevStart<=stop<=prevStop):
                        temp.append((start, stop))
            validIndicies = temp #update most recent holder
             
        #copy the data, and then slice it by the indicies that we ahve. 

        with self.mainLock:
            data = copy.copy(self.__data__)
            sets = copy.copy(self.__sets__)
        output = [[] for i in xrange(len(data) + len(sets))]
        for start, stop in validIndicies: 
            for outputCol, dataCol in izip(output,data):
                outputCol.extend(dataCol[start:stop])
            for outputCol, setCol in izip(output[self.nData:], sets):
                outputCol.extend(setCol[start:stop])
        
        if 1 in kwargs: #a specification over sweep 1 requires a search
            kwargs = {'1': kwargs[1]}
            output = self.parse_data_search(data = output[:self.nData], sets = output[self.nData:], **kwargs)
            
        if twoLists:
            return output[:self.nData], output[self.nData:]
        else:
            return output
                
    def parse_data_search(self,data = None,sets = None,  **kwargs):
        #i'm writing 2 versions of this function. One that has a dicitonary map, and this version, which searches through the list and finds values that correspond with those
        #that the user wants sliced. 
        #the keys in kwargs are the the sweep, and the value is the value
        output = [[] for i in xrange(self.nData)]
        if data is None or sets is None:
            with self.mainLock:
                data = copy.copy(self.__data__)
                sets = copy.copy(self.__sets__)
        #else search with the data and sets passed in. 
        
        for key in kwargs.keys(): #change the keys from strings to ints
            kwargs[int(key)] = kwargs[key]
            del kwargs[key]
        
        for row in xrange(len(data[0])):
            for key, value in kwargs.iteritems():
                if value != sets[key]:
                    break
            else:
                for outputCol, dataCol in izip(output, data):
                    outputCol.append(dataCol[row])
                for outputCol, setCol in izip(output[self.nData:], sets):
                    outputCol.append(setcol[row])
                            
        return output
                
    def write(self):
        if not self.dataFileName or not isfile(self.dataFileName): #if the filename isnt' valid than we don't want to write to it. 
            raise DataError, 'The datafile specified in the LabData object does not exist.'
        with self.mainLock:
            data = copy.copy(self.__data__) # we want a shallow copy just in case something is changed 
            sets = copy.copy(self.__sets__)
        thread.start_new_thread(self.write_data_thread, (data,sets))
        
    def write_data_thread(self, data,sets):
        #called by the write function, it writes 
        #it is possible to copy either jsut the data tree or the whole object; i think just the tree is better. 
        out = []
        
        for row in xrange(self.lastDataIndexWritten, len(data[0])):
            outPutLine = []
            for column in sets:
                outPutLine.append('%.9e'%column[row])
            for column in data:
                outPutLine.append('%.9e'%column[row])#we want the measured data to be last for formatting reasons. . 
            out.append('\t'.join(outPutLine))
        out = '\n' + '\n'.join(out)
        with open(self.dataFileName, 'a') as dataFile:
            dataFile.write(out)
        self.lastDataIndexWritten = len(data[0])
        