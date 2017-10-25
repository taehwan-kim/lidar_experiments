# This program takes an eye diagram using the Agilent 83480A scope.

import time
from datetime import date
from math import *
from pylab import *
from numpy import *
from visa import *




class Agilent83480A:
    def __init__(self, gpib_address = 7):
        self.gpib_address = gpib_address
        self.scope = instrument("GPIB::" + str(self.gpib_address), timeout = 30) #, values_format = single)
        self.scope.clear()
            
    def takeWaveform(self,numCycles = 100, pointsPerSample = 4000):
        
        self.scope.write(":SYS:HEAD OFF")
        self.scope.write(":ACQUIRE:POINTS %d" % pointsPerSample)    

        self.scope.write(":WAVEFORM:FORMAT WORD")
        #scope.write(":WAVEFORM:FORMAT ASCII")
        self.scope.write(":WAVEFORM:SOURCE CHANNEL1")

        self.scope.write(":TIM:RANG 1e-7")    

        self.scope.write(":DIGITIZE CHANNEL1")
        #waveform = array(scope.ask_for_values(":WAVEFORM:DATA?"))
        waveform = self.scope.ask(":WAVEFORM:DATA?")
        waveform = self.convertFile(waveform)
        #print waveform

        waveform = waveform[:,newaxis]

        time_step = self.scope.ask(":WAVEFORM:XINC?")
        print "Time Step:", time_step
        time_origin = self.scope.ask(":WAVEFORM:XOR?")
        print "Start Time:", time_origin
        time_span = self.scope.ask(":WAVEFORM:XRAN?")
        print "Time Span:", time_span

        for i in range(numCycles):
            #scope.clear()
            self.scope.write(":DIGITIZE CHANNEL1")
            newWF = self.scope.ask(":WAVEFORM:DATA?")
            newWF = self.convertFile(newWF)
            #newWF = array(scope.ask_for_values(":WAVEFORM:DATA?"))
            waveform = column_stack((waveform,newWF[:,newaxis]))

        return waveform

    def convertFile(self, waveform):
        prelength = len(waveform)%1000
        numPoints = (len(waveform)-prelength)/2
        data = zeros((numPoints,1))
        for index in range(numPoints):
            strval = waveform[prelength+2*index]+waveform[prelength+1+2*index]
            data[index] = struct.unpack(">h",strval)
        scaledData = float(self.scope.ask(":WAVEFORM:YINCREMENT?"))*data+float(self.scope.ask(":WAVEFORM:YORIGIN?"))
        return scaledData

##def takeEye(numWaveforms, numAvg, numPoints):
##
##    waveformSet = ones((numWaveforms+1,numPoints));
##    for i in range(numWaveforms):
##        waveformSet[i+1]=takeWaveform(numAvg, numPoints)
##        i=i+1
##    timeRange = scope.ask(":TIMEBASE:RANGE?")
##    spacing = float(timeRange)
##    times = arange(0,spacing,spacing/numPoints)
##    waveformSet[0] = times
##    return waveformSet

#wf = takeWaveform(100,4000)

#io.savemat(fileName,{'eye': wf})





