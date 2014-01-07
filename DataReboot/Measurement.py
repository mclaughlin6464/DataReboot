'''
7/3/2013
Sean McLaughlin
This module is called by MeasurementGUI_main, and runs the actually experiment on the instruments, and writes the dataFile. 
'''

def main( reader, sweeper1, sweeper2, sweeper3, emitter, data,  abort, showMessage):
    # each of the 'sweeper' inputs is a tuple, with a setter, a getter, and an array of values to sweep over, in that order. 
    from time import sleep
    from time import time
    from Instruments import LabInstrument
    import LabData
    
    t3s = []
    t2s = []
    t1s = []
    
    try:#The external try catches and show the errors 
        try: # there is a finally to ensure that no matter what the instruments are turned off. 
            
            #TODO: These loops aren't general enough. We'd like to be able to have a specified number of sweeps
            #would allow for more measurements, and would also allow us to forgo checks to skip set values for invalid sweeps. 
            t04 = time()
            for sweeper3i in sweeper3[2]:
                t03 = time()
                sweeper3[0].set(sweeper3i)
                for sweeper2i in sweeper2[2]:
                    t02 = time()
                    sweeper2[0].set(sweeper2i)
                    if sweeper1[0].isGASPSD(): #A power spectrum requires unique looping. 
                        t01 = time()
                        if abort():
                            raise sweeper1[0].LIRef.LabInstrumentError, 'Aborted'
                                
                        readData = sweeper1[0].get(sweeper1[2][0],sweeper1[2][-1], len(sweeper1[2]) )# the start and end need to be ignored.
                        if sweeper1[1].isNoiseSubtract():
                            readData = sweeper1[1].getNoiseSubtract(readData) # subtract off the noise if we can. 
                        
                        if abort():
                            raise sweeper1[0].LIRef.LabInstrumentError, 'Aborted'
                        
                        #we only need to measure these once here; running them through the loop is unecessary.
                        sweep3Get = sweeper3[1].get()
                        sweep2Get = sweeper2[1].get()
                        newData = []
                        if reader is not None: #we can read with the spec analyzer now
                            if reader.type != 'RT':
                                newData.append([reader.get()]*len(readData))
                            else:
                                R,T = reader.get()
                                newData.extend([[R]*len(readData), [T]*len(readData)])
                        
                        newData.extend( [readData, sweeper1[2]])
                        for sweep in (sweep2Get, sweep3Get): #only send in data that is not None
                            if sweep is not None:
                                newData.append([sweep]*len(readData))
                            else:
                                break
                        
                        data.addData(*newData)
                        emitter('Plot') # emit the plot signal
                        t1s.append( time() - t01)
                    else:
                        for sweeper1i in sweeper1[2]:
                            t01 = time()
                            if abort():
                                raise reader.LIRef.LabInstrumentError, 'Aborted'
                            sweeper1[0].set(sweeper1i)
                            if reader.type == 'RT': # i would like to avoid doing this check thousands of time but I'm not sure what to do. 
                                readerData = reader.get()
                            else:
                                readerData = (reader.get(),)
                            newData = list(readerData)
                            newData.extend([ sweeper1[1].get(),sweeper2[1].get(), sweeper3[1].get()])
                            for index in xrange(len(newData)): #we dont' wanna input any columns that we didn't use. 
                                if newData[index] is None:
                                    newData = newData[:index]
                                    break 
                            data.addData(*newData)
                            emitter('Plot') # emit the plot signal
                            t1s.append( time() - t01)
                    data.write()
                    t2s.append(time()-t02)
                t3s.append( time() - t03)
                            
        finally:
            tf4 = time()-t04
            sweeper3[0].off()
            sweeper2[0].off()
            sweeper1[0].off()
            emitter('Done')
            #used for debugging/ feel free to delete. 
            with open('config&data\LoopTimes.txt' , 'w') as TimeFile:
                if t3s and t2s:
                    TimeFile.write('%f\t%f\t%f\t%f\n'%(t1s.pop(0), t2s.pop(0), t3s.pop(0), tf4))
                while t3s:
                    TimeFile.write('%f\t%f\t%f\n'%(t1s.pop(0), t2s.pop(0), t3s.pop(0)))
                while t2s:
                    TimeFile.write('%f\t%f\n'%(t1s.pop(0), t2s.pop(0)))
                while t1s:
                    TimeFile.write('%f\n'%t1s.pop(0))
                
            
    except LabInstrument.LabInstrumentError, message:
        print message
        #showMessage(str(message))
    except LabData.DataError, message:
        print message
        #showMessage(str(message))
    else:
        pass
        #showMessage('')
