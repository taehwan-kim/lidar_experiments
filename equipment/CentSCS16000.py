#!/usr/bin/python
# Pulse8133A.py

# import the VISA module
import visa
import time


class CentSCS16000:
    def __init__(self, gpib_address = 20):
        self.gpib_address = gpib_address
        # print "connecting to " + str(self.gpib_address)
        self.PG=visa.instrument("GPIB::" + str(self.gpib_address))

        # reset the instrument
        # print "Resetting Instrument"
        # self.PG.write('*RST')
        # opc = 0
        # while not opc:
            # opc = int(self.PG.ask("*OPC?"))
    
        # print "done"

        self.TurnOutOff()
        
        # Set the clock frequency to 1GHz
        
        self.PG.write(":SOUR:FREQ:PATH INT")
        self.SetFreq(1)
        
        # Set Delay Voltage
        self.PG.write(":OUTD:COUP DC")
        self.SetAmpOff(0.3,0.6,'Delay')
        self.SetPhase(0)

        # Set Subrate Voltage
        self.PG.write(":OUTS:COUP DC")
        self.SetAmpOff(0.3,0.6,'Subrate')
        self.SetSubrateDiv(1)
        

    #### SetAmpOff  ######################################
    # amp units are V, from 0.3 to 1.7
    # offset units are V from -2.4 to 2.4
    #######################################################
    def TurnOutOff(self):
        self.PG.write(':OUTD:OUTP OFF')
        self.PG.write(':OUTS:OUTP OFF')
    
    def TurnOutOn(self):
        self.PG.write(':OUTD:OUTP ON')
        self.PG.write(':OUTS:OUTP ON')
    
    def SetAmpOff(self, amp, offset, port='Delay'):
        if port=='Delay':
            portWr = 'OUTD'
        elif port=='Subrate':
            portWr = 'OUTS'
        else:
            portWr = -1
            
        if portWr==-1:
            print 'Invalid Port Type'
        else:
            # write to GPIB
            self.PG.write(':'+portWr+':AMPL'+str(amp))
            self.PG.write(':'+portWr+':OFFS'+str(offset))

    #### SetFreq ####
    # - GHz
    #################
    def SetFreq(self, freq, unit = 'GHz'):
        self.PG.write(":SOUR:FREQ %.3f%s" % (freq, unit))
        self.freq = freq

    #### SetSubrate ####
    def SetSubrateDiv(self,divider):
        self.PG.write(':OUTS:DIV ' + str(divider))

    #### SetPhase ####
    # - Set the phase of channel 2 relative to channel 1
    # - delay is computed from phase
    ##################
    def SetPhase(self, phase):
        uiSet = float(phase)/float(360)
        self.PG.write(":OUTD:DEL %.3fUI" % uiSet)

#### Main Program ####
# Run this to debug  #
######################
if __name__=='__main__':
    clocksource = CentSCS16000()
    freq = 2
    clocksource.SetFreq(freq)
    time.sleep(1)
    freq = 1.5
    clocksource.SetFreq(freq)  
    
    clocksource.TurnOutOn()
    
    for phase in range(-80
                       ,360,20):
        time.sleep(1)
        clocksource.SetPhase(phase)

    clocksource.TurnOutOff()
