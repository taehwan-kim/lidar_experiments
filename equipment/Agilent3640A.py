#!/usr/bin/python

# import the VISA module
import visa
import time
from numpy import average

class Agilent3640A:

    def __init__(self, gpib_address = 25, wait = 0.5, curr_lim = 0.8):
        self.gpib = visa.instrument("GPIB::%d" % (gpib_address))
        self.wait = wait
        self.curr_lim = curr_lim
        self.TurnSupplyOFF()
        
    def SetOut(self, voltage):
        self.gpib.write("APPL %3f, %4f" % (voltage, self.curr_lim))
        time.sleep(self.wait)

    def TurnSupplyON(self):
        self.gpib.write("OUTP:STAT ON")    
        time.sleep(self.wait)

    def SetVoltageLow(self):
        self.gpib.write("SOUR:VOLT:RANG LOW")
        time.sleep(self.wait)

    def SetVoltageHigh(self):
        self.gpib.write("SOUR:VOLT:RANG HIGH")
        time.sleep(self.wait)

    def TurnSupplyOFF(self):
        self.gpib.write("OUTP:STAT OFF")      

    def MeasCurr(self, samples = 1):
        # Repeat measurement a number of times
        curr_raw = []
        for i in range(samples):
            curr_raw.append(float(self.gpib.ask_for_values("MEAS:CURR?")[0]))        
        return average(curr_raw)
        

if __name__=='__main__':
    s = Agilent3640A(gpib_address = 5, wait = 0.5)
    s.TurnSupplyON()
    s.SetVoltageLow()
    for voltage in [0.12,0.34,2.0]:
        time.sleep(1)
        s.SetOut(voltage)
        print "Current = %s" % float(s.MeasCurr())
    s.TurnSupplyOFF()



