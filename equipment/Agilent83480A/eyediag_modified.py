# This program takes an eye diagram using the Agilent 83480A scope.

import time
from datetime import date
from math import *
from pylab import *
from numpy import *
#from scipy import io
#from scipy import optimize
from visa import *

SaveTitle = "15414_body_MD_R1_S6_09_12_100s_p4"
DataDirectory = "C:\Python25"

timeTuple = time.localtime()
eyeFile = "eye--%s--%d#%d#%d--%d#%d#%d.mat" % (SaveTitle,timeTuple[0],timeTuple[1],timeTuple[2],timeTuple[3],timeTuple[4],timeTuple[5])
fileName = DataDirectory+"\\"+eyeFile

scope = instrument("GPIB::7", timeout = 30) #, values_format = single)
scope.clear()

def takeWaveform(numCycles, pointsPerSample):
    
    scope.write(":SYS:HEAD OFF")
    scope.write(":ACQUIRE:POINTS %d" % pointsPerSample)    

    scope.write(":WAVEFORM:FORMAT WORD")
    #scope.write(":WAVEFORM:FORMAT ASCII")
    scope.write(":WAVEFORM:SOURCE CHANNEL1")

    scope.write(":TIM:RANG 1e-7")    

    scope.write(":DIGITIZE CHANNEL1")
    #waveform = array(scope.ask_for_values(":WAVEFORM:DATA?"))
    waveform = scope.ask(":WAVEFORM:DATA?")
    waveform = convertFile(waveform)
    #print waveform

    waveform = waveform[:,newaxis]

    time_step = scope.ask(":WAVEFORM:XINC?")
    print "Time Step:", time_step
    time_origin = scope.ask(":WAVEFORM:XOR?")
    print "Start Time:", time_origin
    time_span = scope.ask(":WAVEFORM:XRAN?")
    print "Time Span:", time_span

    for i in range(numCycles):
        #scope.clear()
        scope.write(":DIGITIZE CHANNEL1")
        newWF = scope.ask(":WAVEFORM:DATA?")
        newWF = convertFile(newWF)
        #newWF = array(scope.ask_for_values(":WAVEFORM:DATA?"))
        waveform = column_stack((waveform,newWF[:,newaxis]))

    return waveform

def convertFile(waveform):
    prelength = len(waveform)%1000
    numPoints = (len(waveform)-prelength)/2
    data = zeros((numPoints,1))
    for index in range(numPoints):
        strval = waveform[prelength+2*index]+waveform[prelength+1+2*index]
        data[index] = struct.unpack(">h",strval)
    scaledData = float(scope.ask(":WAVEFORM:YINCREMENT?"))*data+float(scope.ask(":WAVEFORM:YORIGIN?"))
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

wf = takeWaveform(100,4000)

#io.savemat(fileName,{'eye': wf})
