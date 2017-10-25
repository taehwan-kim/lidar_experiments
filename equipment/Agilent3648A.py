#!/usr/bin/python
# DC3631A.py

# import the VISA module
import visa
import time
from numpy import average

class Agilent3648A:

    def __init__(self, gpib_address = 5, wait = 0.5, curr_lim1 = 0.8, curr_lim2 = 0.8):
        self.gpib = visa.instrument("GPIB::%d" % (gpib_address))
        self.wait = wait
        self.curr_lim1 = curr_lim1
        self.curr_lim2 = curr_lim2
        self.TurnSupplyOFF()
        
    def SetOut1(self, voltage):
        self.gpib.write("INST:SEL OUT1")
        self.gpib.write("APPL %.2f, %.3f" % (voltage, self.curr_lim1))
        time.sleep(self.wait)

    def SetOut2(self, voltage):
        self.gpib.write("INST:SEL OUT2")
        self.gpib.write("APPL %.2f, %.3f" % (voltage, self.curr_lim2))
        time.sleep(self.wait)

    def SetOut(self, channel, voltage):
        if channel < 1 or channel > 2:
            raise ValueError("Machine only has channels 1 and 2")
        self.gpib.write("INST:SEL OUT%d" % channel)
        if channel == 1:
            self.gpib.write("APPL %.2f, %.3f" % (voltage, self.curr_lim1))
        elif channel == 2:
            self.gpib.write("APPL %.2f, %.3f" % (voltage, self.curr_lim2))
        time.sleep(self.wait)

    def TurnSupplyON(self):
        self.gpib.write("OUTP:STAT ON")    
        time.sleep(self.wait)

    def TurnSupplyOFF(self):
        self.gpib.write("OUTP:STAT OFF")      

    def MeasCurr(self, channel, samples = 1):
        if channel < 1 or channel > 2:
            raise ValueError("Machine only has channels 1 and 2")
        # Select channel
        self.gpib.write("INST:SEL OUT%d" % channel)        
        # Repeat measurement a number of times
        curr_raw = []
        for i in range(samples):
            curr_raw.append(float(self.gpib.ask_for_values("MEAS:CURR?")[0]))        
        return average(curr_raw)
    
    def MeasCurrRaw(self, channel, samples = 1):
        if channel < 1 or channel > 2:
            raise ValueError("Machine only has channels 1 and 2")
        # Select channel
        self.gpib.write("INST:SEL OUT%d" % channel)        
        # Repeat measurement a number of times
        curr_raw = []
        for i in range(samples):
            curr_raw.append(float(self.gpib.ask_for_values("MEAS:CURR?")[0]))        
        return curr_raw

if __name__=='__main__':
    s = Agilent3648A(gpib_address = 5, wait = 0.5)
    s.TurnSupplyON()
    for voltage in [0.12,0.34,2.0]:
        time.sleep(1)
        s.SetOut(1, voltage)
        print "Current = %s" % float(s.MeasCurr(1)[0])
        s.SetOut(2, voltage)
        print "Current = %s" % float(s.MeasCurr(2)[0])
    for voltage in [0.88,0.77,2.0]:
        time.sleep(1)
        s.SetOut(2, voltage)
        print "Current = %s" % float(s.MeasCurr(2)[0])
    s.TurnSupplyOFF()



