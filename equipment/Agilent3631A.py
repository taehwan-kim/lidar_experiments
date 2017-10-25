#!/usr/bin/python
# DC3631A.py

# import the VISA module
import visa
import time
from numpy import average

class Agilent3631A:
    def __init__(self, gpib_address = 5, wait = 0.5, curr_lim_6v = 0.5, curr_lim_25v = 0.5):
        self.gpib = visa.instrument("GPIB::%d" % (gpib_address))
        self.wait = wait
        self.curr_lim_6v = curr_lim_6v
        self.curr_lim_25v = curr_lim_25v
        self.TurnSupplyOFF()
        
    def Set6V(self, voltage):
        self.gpib.write("APPL P6V, " + str(voltage) + "," + str(self.curr_lim_6v))
        #dcSupply.write('INST P6V')
        #dcSupply.write('VOLT '+str(voltage))
        #dcSupply.write('CURR 0.5')
        time.sleep(self.wait)

    def Set25V(self, voltage):
        self.gpib.write("APPL P25V, " + str(voltage) + "," + str(self.curr_lim_25v))
        time.sleep(self.wait)

    def TurnSupplyON(self):
        self.gpib.write("OUTP:STAT ON")    
        time.sleep(self.wait)

    def TurnSupplyOFF(self):
        self.gpib.write("OUTP:STAT OFF")      

    def MeasCurr6V(self, samples = 1):
        # Repeat measurement a number of times
        curr_raw = []
        for i in range(samples):
            curr_raw.append(float(self.gpib.ask_for_values("MEAS:CURR? P6V")[0]))        
        return average(curr_raw)

    def MeasCurrP25V(self, samples = 1):
        # Repeat measurement a number of times
        curr_raw = []
        for i in range(samples):
            curr_raw.append(float(self.gpib.ask_for_values("MEAS:CURR? P25V")[0]))        
        return average(curr_raw)
        
    def MeasCurrN25V(self, samples = 1):
        # Repeat measurement a number of times
        curr_raw = []
        for i in range(samples):
            curr_raw.append(float(self.gpib.ask_for_values("MEAS:CURR? N25V")[0]))        
        return average(curr_raw)
        
if __name__=='__main__':
    s = Agilent3631A()
    s.TurnSupplyON()
    for voltage in [0.1,0.5,0.8]:
        time.sleep(1)
        s.Set6V(voltage)
        s.Set25V(voltage)
    s.TurnSupplyOFF()
    for voltage in [0.1,0.5,0.8]:
        time.sleep(1)
        s.Set6V(voltage)
    s.TurnSupplyOFF()
