#!/usr/bin/python
# .py

# import the VISA module
import visa
import time
import matplotlib.pyplot as p
import numpy
import math
import time
import re

# Code for Agilent 8164B mainframe, with a laser setup on module 0
# and power meter setup on module 1
class Agilent8164B:
    def __init__(self, gpib_address = 20, verbose = True):

        self.verbose = verbose

        # Logging features don't work with the old pyvisa
        self.legacy = (float(visa.__version__) < 1.6)

        if self.legacy:
            self.gpib = visa.instrument("GPIB::%d" % (gpib_address))
        else:
            self.gpib = visa.ResourceManager().open_resource("GPIB::%d" % (gpib_address))

        self.gpib.clear()

    def set_avg_time(self, avg_time, unit = 'ms'):
        self.gpib.write(":SENS%d:POW:ATIME %d%s" % (1, avg_time, unit))

    def read_power(self, read_1 = True, read_2 = True):

        if read_1 or read_2:
            pow_1 = float(self.gpib.ask(":READ%d:CHAN%d:POW?" % (1, 1)))
        if read_2:
            pow_2 = float(self.gpib.ask(":FETC%d:CHAN%d:POW?" % (1, 2)))
        
        if read_1 and read_2:
            return (pow_1, pow_2)
        if read_1 and not read_2:
            return pow_1
        if read_2 and not read_1:
            return pow_2        

        return 0

    def arm_log_power(self, samples = 16, avg_time = 0.001, slot = 1, ext_trig = True):

        if avg_time < 0.0001:
            raise Exception("Average time (%f) cannot be smaller than 0.0001!" % (avg_time))
        if samples > 20001 or samples < 1:
            raise Exception("Number of samples (%d) must be between 1 and 20001" % (samples))
        if self.legacy:
            raise Exception("Logging of power not supported in PyVISA versions prior to 1.6!")
        
        # Stop anything before starting new one
        self.gpib.write(":SENS%d:FUNC:STAT LOGG,STOP" % (slot))
         
        # A lot of parameters you have to set the same for both channels by setting channel 1
        self.gpib.write(":SENS%d:FUNC:PAR:LOGG %d,%f" % (slot, samples, avg_time))
        self.gpib.write(":SENS%d:POW:RANGE:AUTO 1" % (slot))
        self.gpib.write(":TRIG%d:INP %s" % (slot, "SME" if ext_trig else "IGN"))

        if self.verbose: 
            out_str = self.gpib.ask(":SENS%d:FUNC:PAR:LOGG?" % (slot))
            res = re.search('([\+\-\w]+),([\+\.\-\w]+)', out_str)

            if not res:
                raise Exception("Could not successfully write power meter logging" + \
                    " configuration to instrument, check slot number?")

            print "Arming power meter logging with %d samples with %f second averaging time..." % \
                (int(res.group(1)), float(res.group(2)))
            
        # Arm the instrument
        self.gpib.write(":SENS%d:FUNC:STAT LOGG,STAR" % (slot))
    
    # Poll the instrument to see if it is done, then return the data 
    def get_log_power(self,  slot = 1, dbm = True, \
            log_1 = True, log_2 = True):

        # Set timeout to be infinite as it waits for the instrument to acquire the data 
        old_timeout = self.gpib.timeout
        self.gpib.timeout = None

        # Poll the instrument until it is done
        stat = ""
        while "COMPLETE" not in stat:
            time.sleep(0.05)
            stat = self.gpib.ask(":SENS%d:FUNC:STAT?" % (slot))

        # Set the old timeout back
        self.gpib.timeout = old_timeout

        if self.verbose:
            print "Logging Complete!"

        if log_1:
            data1 = self.gpib.query_binary_values("SENS%d:CHAN%d:FUNC:RES?" % (slot, 1))
            if dbm:
                for i in range(len(data1)):
                    data1[i] = 10 * math.log10(data1[i]) + 30
        if log_2:
            data2 = self.gpib.query_binary_values("SENS%d:CHAN%d:FUNC:RES?" % (slot, 2))
            if dbm:
                for i in range(len(data2)):
                    data2[i] = 10 * math.log10(data2[i]) + 30

        if log_1 and log_2:
            return (data1, data2)
        if log_1:
            return data1
        if log_2:
            return data2

if __name__=='__main__':
    power_meter = Agilent8164B(gpib_address=20)

    temp = power_meter.log_power(samples = 20001, avg_time = 0.005, slot = 1, \
        ext_trig = True, dbm = True, \
        log_1 = False, log_2 = True)

    for i in range(len(temp)):
        print "%d: %f dBm" % (i, temp[i])
    #print power_meter.read_power(read_1 = False, read_2 = True)
