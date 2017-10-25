#!/usr/bin/python
# .py

# import the VISA module
import visa
import time
import matplotlib.pyplot as p
import numpy
import time


class powerMeter:
    def __init__(self,gpibAddress):
        self.gpib=gpibAddress
        self.powerA = 0
        self.powerB = 0
        self.readPower()
        self.visaHandle=0

    def readPower(self):
        self.visaHandle = visa.instrument("GPIB::"+str(self.gpib))
        self.powerA = float(self.visaHandle.ask(":READ1:SCAL:POW?"))
        self.powerB = float(self.visaHandle.ask(":READ2:SCAL:POW?"))
        self.powerBmA = self.powerB-self.powerA

if __name__=='__main__':
    myPowerMeter = powerMeter(gpibAddress=20)

    while(1):
        time.sleep(0.01)
        myPowerMeter.readPower()
        print myPowerMeter.powerBmA
