#!/usr/bin/python
# Pulse8133A.py

# import the VISA module
import visa
import time


class Agilent8133A:
    def __init__(self, gpib_address = 25, wait = 0.0):
        self.gpib_address = gpib_address
        self.PG=visa.instrument("GPIB::" + str(self.gpib_address))
        self.wait = wait
            
    #### SetDelay #########################################
    # - Set the delay of channel 2 relative to channel 1
    # - delay is in ps
    #######################################################
    def SetDelay(self, delay, channel = 2):
        if not channel == 2:
            raise Error("81133A can only adjust delay on channel 2!")
        self.PG.write('del1 '+str(delay)+'ps')
        time.sleep(self.wait)

    def SetDutyCycle(self, duty_cycle):
        self.PG.write(':DCYC1 %.3f' % (duty_cycle))        
        time.sleep(self.wait)
        
    #### SetPhase ####
    # - Set the phase of channel 2 relative to channel 1
    # - delay is computed from phase
    ##################
    def SetPhase(self, phase,ClockFreq):
        rateFloat = float(ClockFreq)
        period = (1/rateFloat)*1000     # ps
        delay = ((float(phase))/360)*period
        print 'The phase is '+str(phase)+' and the delay is '+str(delay)
        self.SetDelay(delay)
        time.sleep(self.wait)
        
    #### SetFreq ####
    # - set the frequency of the AWG
    # - GHz
    #################
    def SetFreq(self, freq):
        SampleFreq=float(freq)
        self.PG.write(':FREQ ' + str(SampleFreq) +' GHz')   
        time.sleep(self.wait)

    '''
    def SetMag(Mag):
        inputMag=float(Mag)
        self.PG.write(':VOLT1 ' + str(inputMag))
        self.PG.write(':VOLT1:OFFS 0.0v')   
    '''
        


#### Main Program ####
# Run this to debug  #
######################
if __name__=='__main__':
    clocksource = Agilent8133A()
    ClockFreq = 2
    clocksource.SetFreq(ClockFreq)
    for delay in range(-100,100,10):
        time.sleep(1)
        clocksource.SetDelay(delay)
    ClockFreq = 1.5
    clocksource.SetFreq(ClockFreq)    
    for phase in range(-360,360,20):
        time.sleep(1)
        clocksource.SetPhase(phase,ClockFreq)


