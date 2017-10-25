#!/usr/bin/python
# Agilent81143A.py
# from Agilent3648A import *

# import the VISA module
import visa
import time

# Function generator
class Agilent81134A:

    def __init__(self, gpib_address = 30, wait = 0.5):
        self.gpib = visa.instrument("GPIB::%d" % (gpib_address))
        self.wait = wait

    # Quick configure of all pulse mode options
    def ConfigPulse(self, channel, freq, duty_cycle, delay, \
        amplitude, offset, time_unit = 'ps', freq_unit = 'GHz', volt_unit = 'mV'):
        # HI            = offset + ampl/2
        # LO            = offset - ampl/2
        
        self.SetPulse(channel)
        self.SetFreq(freq, freq_unit)
        self.SetDutyCycle(channel, duty_cycle)
        self.SetDelay(channel, delay, time_unit)
        self.SetOffAmp(channel, amplitude, offset, volt_unit)

    #### SetDelay #########################################
    # - Set the delay of channel 2 relative to channel 1
    # - delay is in ps
    #######################################################
    def SetDelay(self, channel, delay, unit = 'ps'):
        self.gpib.write(':DEL%d %f %s' % (channel, delay, unit))
        time.sleep(self.wait)

    #### SetFreq ####
    # - set the frequency of the AWG
    # - GHz
    #################
    def SetFreq(self, freq, unit = 'GHz'):
        self.gpib.write(':FREQ %.3f %s' % (freq, unit))   

    def SetPeriod(self, period, unit = 'ps'):
        self.gpib.write(':PER %.3f %s' % (period, time_unit))
        
    def SetData(self, channel, data):
        self.gpib.write(':FUNC:MODE'+str(channel)+' DATA')
        self.gpib.write(':DIG:PATT:LENG '+str(len(data)))
        self.gpib.write(':DIG'+str(channel)+':PATT #'+str(channel)+str(len(data))+str(data)+', DUAL')    

    def SetSquare(self, channel):
        self.gpib.write(':FUNC:MODE'+str(channel)+' SQU')

    def SetPulse(self, channel):
        self.gpib.write(':FUNC PATT')
        self.gpib.write(':FUNC:MODE'+str(channel)+' PULSE')

    def SetHighLow(self, channel, high, low, unit = 'V'):
        self.gpib.write(':VOLT%d:HIGH %0.3f %s' % (channel, high, unit))
        self.gpib.write(':VOLT%d:LOW %0.3f %s' % (channel, low, unit))
    
    def SetOffAmp(self, channel, amplitude, offset, unit = 'V'):
        self.gpib.write(':VOLT'+str(channel)+':AMPL %.3f %s' % (amplitude, unit))
        self.gpib.write(':VOLT'+str(channel)+':OFFSET %.3f %s' % (offset, unit))
        
    def SetDutyCycle(self, channel, duty_cycle):
        self.gpib.write(':DCYC'+str(channel)+' %.3f' % (duty_cycle))
        
    def SetPulseWidth(self, channel, width, unit = 'ps'):
        self.gpib.write(':WIDT'+str(channel)+' %.3f %s' % (width, unit))
        
    def TurnOn(self, channel):
        if channel < 1 or channel > 2:
            raise ValueError("Agilent 81134A has only channels 1 and 2!")
        self.gpib.write(':OUTP%d:NEG ON' % channel)
        self.gpib.write(':OUTP%d:POS ON' % channel)
        #if not self.central:
        #    self.CentralOn()
    
    def CentralOff(self):
        self.gpib.write(':OUTP:CENT OFF')
        self.central = 0
        
    def CentralOn(self):
        self.gpib.write(':OUTP:CENT ON')
        self.central = 1        

#### Main Program ####
# Run this to debug  #
######################
if __name__=='__main__':
    func_gen = Agilent81134A(gpib_address = 30, wait = 0.5)
    func_gen.TurnOn(1)
    func_gen.TurnOn(2)
    func_gen.SetHighLow(channel = 1, high = 500, low = 100, unit = 'mV')
    func_gen.SetHighLow(channel = 2, high = 0.6, low = 0.3)
    func_gen.SetSquare(channel = 1)
    func_gen.SetSquare(channel = 2)
    func_gen.SetDelay(channel = 1, delay = 0)
    func_gen.SetDelay(channel = 2, delay = 100, unit = 'ps')
    
    for clock_freq in [0.1, 0.2, 0.3, 0.3, 0.4, 0.5]:
        func_gen.SetFreq(clock_freq)
        time.sleep(1.0)        
    # for delay in range(-100,100,10):
        # time.sleep(0.5)
        # func_gen.SetDelay(1, delay)
    func_gen.CentralOff()
