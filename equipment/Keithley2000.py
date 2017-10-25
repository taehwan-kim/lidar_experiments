#!/usr/bin/python
# .py

import visa
import time
import numpy

class Keithley2000:
    def __init__(self, gpib_address = 17):
        self.gpib_address = gpib_address
        number_of_readings = 5
        self.gpib = visa.instrument("GPIB::" + str(self.gpib_address))
    
    def getCurrent(self, number_of_readings = 10, verbose = False):
        currents = self.getCurrentRaw(number_of_readings)
        if verbose:
            print "Current Standard deviation: ", numpy.std(currents)
            print "Current Average: ", numpy.average(currents)
            print "Current Median: ", numpy.median(currents)            
        return numpy.median(currents)
        
    def getCurrentRaw(self, number_of_readings = 10):
        self.gpib.write("*rst; status:preset; *cls")
        interval_in_ms = 1
        self.gpib.write("status:measurement:enable 512; *sre 1")
        self.gpib.write("sample:count %d" % number_of_readings)
        self.gpib.write("trigger:source bus")
        self.gpib.write("trigger:delay %f" % (interval_in_ms / 1000.0))
        self.gpib.write("trace:points %d" % number_of_readings)
        self.gpib.write("FUNCTION \'CURRENT:DC\'")
        self.gpib.write("trace:feed sense1; feed:control next")
        self.gpib.write("initiate")
        self.gpib.trigger()
        self.gpib.wait_for_srq()
        return self.gpib.ask_for_values("trace:data?")

    def getVoltage(self, number_of_readings = 10, verbose = 0):
        self.gpib.write("*rst; status:preset; *cls")
        interval_in_ms = 1
        self.gpib.write("status:measurement:enable 512; *sre 1")
        self.gpib.write("sample:count %d" % number_of_readings)
        self.gpib.write("trigger:source bus")
        self.gpib.write("trigger:delay %f" % (interval_in_ms / 1000.0))
        self.gpib.write("trace:points %d" % number_of_readings)
        self.gpib.write("FUNCTION \'VOLT:DC\'")
        self.gpib.write("trace:feed sense1; feed:control next")
        self.gpib.write("initiate")
        self.gpib.trigger()
        self.gpib.wait_for_srq()
        voltages = self.gpib.ask_for_values("trace:data?")
        averageVoltage = sum(voltages)/len(voltages)
        if verbose==1:
            print "Voltage Standard deviation: ", numpy.std(voltages)
            print "Voltage Average: ", averageVoltage
        return averageVoltage

if __name__=='__main__':
    s = Keithley2000()
    for i in range(10):
        print "Current: %f" % s.getCurrent()
        time.sleep(0.5)
