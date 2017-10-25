# This program takes an eye diagram using the Agilent 83480A scope.

import time
from datetime import date
from math import *
from pylab import *
from numpy import *
from visa import *


class DSOX4104A:
    def __init__(self, resourcemanager, wait = 0.5):

        self.scope = resourcemanager.open_resource("USB0::0x0957::0x17A0::MY56310453::INSTR")
        self.wait = wait
        self.scope.clear()

    def setTrigger(self, channel = 1, edge = "pos"):

        self.scope.write(":trig:sour chan%d" % channel)
        self.scope.write(":trig:slop %s" % edge)
    
    def setAcquisition(self, mode = "hres"):

        self.scope.write(":acq:type %s" % mode)

    def setChannelOption(self, channel = 1, coupling = "DC", bwlimit = 0, display = 1, \
            impedance = "FIFT", scale = 100.0):

        self.scope.write(":chan%d:bwl %d" % (channel, bwlimit))
        self.scope.write(":chan%d:coup %s" % (channel, coupling))
        self.scope.write(":chan%d:disp %s" % (channel, display))
        self.scope.write(":chan%d:imp %s" % (channel, impedance))
        self.scope.write(":chan%d:scal %fmV" % (channel, scale))

    def takeWaveform(self, numCycles = 1, channel = 1, timerange = 1e-7, wformat = "ascii", \
            wpoints = 4000, wpointsmax = 1):
        
        # self.scope.write(":SYS:HEAD OFF")
        if wpointsmax == 1:
            self.scope.write(":wav:poin:mode max")    
        else:
            self.scope.write(":wav:poin %d" % wpoints)    

        self.scope.write(":wav:form %s" % wformat)
        #scope.write(":WAVEFORM:FORMAT ASCII")
        self.scope.write(":wav:sour chan%d" % channel)

        self.scope.write(":tim:rang %g" % timerange)    

        time_step = float(self.scope.query(":wav:xinc?"))
        print "Time Step:", time_step
        time_origin = float(self.scope.query(":wav:xor?"))
        print "Start Time:", time_origin
        time_points = int(self.scope.query(":wav:poin?"))
        time_span = time_step * time_points
        print "Time Span:", time_span

        t = array([ii * time_step + time_origin for ii in range(time_points)])
        t = t[:,newaxis]

        # self.scope.write(":DIGITIZE CHANNEL1")
        #waveform = array(scope.ask_for_values(":WAVEFORM:DATA?"))

        self.scope.write(":sing")

        waveform = self.scope.query(":wav:data?")
        # remove preamble
        waveform = waveform[10:-1] 
        waveform = fromstring(waveform,dtype=float64,sep=',')
        waveform = waveform[:,newaxis]

        for i in range(numCycles-1):
            self.scope.clear()
            self.scope.write(":sing")
            newwave = self.scope.query(":wav:data?")
            newwave = newwave[10:-1]
            newwave = fromstring(newwave,dtype=float64,sep=',')
            # newWF = self.scope.ask(":WAVEFORM:DATA?")
            # newWF = self.convertFile(newWF)
            #newWF = array(scope.ask_for_values(":WAVEFORM:DATA?"))
            waveform = column_stack((waveform,newwave[:,newaxis]))

        return t, waveform

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





