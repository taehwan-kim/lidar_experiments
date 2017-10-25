#!/usr/bin/python

# import the VISA module
import visa
import time

#   This function generator actually consists of 3 components:
#   1. Agilent HP 70340A - Signal Generator: 
#       the clock source for 70843B
#   2. Agilent 70843B - Error Performance Analyser: 
#       take the clock from 70340B and set the desired pattern
#       or shape for clock or data output.
#   3. Agilent HP 70004A - Display: 
#       since the above two components have no display, this
#       display displays menu for it.

class Agilent70843B:
    def __init__(self, gpib_address_70340a=3, gpib_address_70843b=1, wait=0.5):
        self.gpib_70340a = visa.instrument("GPIB::%d" % (gpib_address_70340a))
        self.gpib_70843b = visa.instrument("GPIB::%d" % (gpib_address_70843b))
        self.wait = wait
        self.CentralOff()
    
    # turn clock off
    def CentralOff(self):
        self.gpib_70340a.write('OUTP:STAT OFF')

    # turn clock on
    def CentralOn(self):
        self.gpib_70340a.write('OUTP:STAT ON')

    # set clock frequency [GHz]
    def SetFreq(self,freq):
        self.gpib_70340a.write('FREQ ' + str(freq) + 'GHZ')
        self.gpib_70340a.write('POW:LEV 0.00DBM')
    
    # set clock property (amplitude and high-level)
    def ConfigPulse(self, amplitude=0.500, high_level=0.250):
        self.gpib_70843b.write('SOURce2:VOLTage:LEVel:IMMediate:AMPLitude ' + str(amplitude))
        self.gpib_70843b.write('SOURce2:VOLTage:LEVel:IMMediate:HIGH ' + str(high_level))

#### Main Program ####
# Run this to debug  #
######################
if __name__=='__main__':
    bert = Agilent70843B(gpib_address_70340a=3, gpib_address_70843b=1)

