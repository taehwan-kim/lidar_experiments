# This program takes an eye diagram using the Agilent 83480A scope.

import time
from datetime import date
from math import *
from pylab import *
from numpy import *
from scipy import io
from scipy import optimize
from visa import *

SaveTitle = "test"
DataDirectory = "."

today = date.today()
DateString = date.isoformat(today)
OutFileBase = DataDirectory + "\\eye_" + SaveTitle + DateString

scope = instrument("GPIB::7", timeout = 10)
scope.clear()

##def takeWaveform(numPoints, samplingFrequency, pointsPerSample):
##
##    numCycles = (0.0+numPoints)/pointsPerSample
##    totaltime = numCycles/samplingFrequency
##    
##    scope.write(":ACQUIRE:TYPE AVERAGE")
##    scope.write(":WAVEFORM:SOURCE CHANNEL1")
##    scope.write(":WAVEFORM:FORMAT ASCII")
##    scope.write(":ACQUIRE:COUNT 1")
##    #scope.write(":AUTOSCALE")
##    scope.write(":DIGITIZE CHANNEL1")
##
##    numSets = numPoints/4095
##    diff = numPoints-numSets*4095
##    scope.write(":ACQUIRE:POINTS "+str(diff))
##    scope.write(":TIMEBASE:RANGE "+str(totaltime*(1-numSets/numPoints*4095.0)))
##    scope.write(":TIMEBASE:DELAY 0")
##    waveform = scope.ask_for_values(":WAVEFORM:DATA?")
##    scope.write(":ACQUIRE:POINTS 4095")
##    scope.write(":TIMEBASE:RANGE "+str(totaltime*4095.0/numPoints))
##    for i in range(numSets):
##        scope.write(":TIMEBASE:DELAY "+str(totaltime*4095.0*i/numPoints+diff/numPoints*totaltime))
##        newWF = scope.ask_for_values(":WAVEFORM:DATA?")
##        waveform = concatenate((waveform,newWF),axis=0)
##        
##    data = zeros((numPoints,2))
##    
##    for j in range(numPoints):
##        if waveform[j]<1:
##            data[j][1] = waveform[j]
##        data[j][0] = j*numCycles/samplingFrequency
##        
##    return data

def takeWaveform(numCycles, samplingFrequency, pointsPerSample):
    
    scope.write(":ACQUIRE:TYPE AVERAGE")
    scope.write(":WAVEFORM:SOURCE CHANNEL2")
    scope.write(":WAVEFORM:FORMAT ASCII")
    scope.write(":ACQUIRE:COUNT 1")
    #scope.write(":AUTOSCALE")
    scope.write(":DIGITIZE CHANNEL2")

    scantime = 2/samplingFrequency
    scope.write(":ACQUIRE:POINTS "+str(pointsPerSample))
    scope.write(":TIMEBASE:RANGE "+str(scantime))
    scope.write(":TIMEBASE:DELAY 0")            
    data = zeros((numCycles+1,pointsPerSample))
    for i in range(numCycles):
        newWF = scope.ask_for_values(":WAVEFORM:DATA?")
        data[i+1] = newWF
    
    for j in range(pointsPerSample):
        data[0][j] = j*scantime/pointsPerSample
        
    return data

wf = takeWaveform(100,100E6,4000)

#eye = takeEye(10,8,500)
eyefile = OutFileBase + '.mat'
io.savemat(eyefile,{'eye': wf})
