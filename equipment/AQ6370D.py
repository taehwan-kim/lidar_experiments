#!/usr/bin/python

import visa
import time
import numpy

class AQ6370D:
    def __init__(self, resourcemanager, gpib_address = 1, wait = 0.5):
        self.gpib_address = gpib_address
        self.resource = resourcemanager.open_resource("GPIB::" + str(self.gpib_address))
        self.wait = wait

    # def turnSourceOn(self):
        # self.resource.write(':output:state 1')
        # time.sleep(self.wait)

    # def turnSourceOff(self):
        # self.resource.write(':output:state 0')
        # time.sleep(self.wait)

    # def setCurrent(self, current, vlim):
        # # reset the device
        # self.resource.write('*RST')

        # # set voltage compliance
        # self.resource.write(':sense:function:on "voltage"')
        # self.resource.write(':sense:voltage:protection:level %f' % vlim)

        # # set the device to be a current source
        # self.resource.write(':source:function:mode current')
        # self.resource.write(':source:current:mode fixed')
        # self.resource.write(':source:current:level:amplitude %f' % current)

    def sweepOn(self, center, span, verbose = 1):
        self.resource.write('*rst')
        self.resource.write(':sens:band 0.02nm')
        self.resource.write(':sens:wav:span %dnm' % span)
        self.resource.write(':sens:wav:cent %dnm' % center)

        self.resource.write(':init:smod 1')
        self.resource.write(':init')
        # self.resource.write(':calc:category swth')
        # self.resource.write(':calc')


    def measPower(self, center, span, verbose = 1):

        self.resource.write('*rst')
        self.resource.write(':sens:band 0.02nm')
        self.resource.write(':sens:wav:span %dnm' % span)
        self.resource.write(':sens:wav:cent %dnm' % center)

        self.resource.write(':init:smod 1')
        self.resource.write(':init')
        self.resource.write(':calc:category pow')
        self.resource.write(':calc')

        datatemp = self.resource.query_ascii_values(':calc:data?', container = numpy.array)
        if verbose == 1:
            print datatemp

        return datatemp


    def measPeak(self, center, span, verbose = 1):

        self.resource.write('*rst')
        self.resource.write(':sens:band 0.02nm')
        self.resource.write(':sens:wav:span %dnm' % span)
        self.resource.write(':sens:wav:cent %dnm' % center)

        self.resource.write(':init:smod 1')
        self.resource.write(':init')
        self.resource.write(':calc:category swth')
        self.resource.write(':calc')

        # self.resource.write(':stat:pres')
        # self.resource.write('*cls')
        # self.resource.write(':stat:meas:enab 512')
        # self.resource.write('*sre 1')

        # self.resource.write(':trac:cle')
        # self.resource.write(':trac:poin %d' % number_of_readings)

        # self.resource.write(':sens:func "current"')
        # self.resource.write(':sens:func:conc on')

        # # self.resource.write(':trac:feed sense1')

        # self.resource.write(':trig:coun %d' % number_of_readings)
        # self.resource.write(':trig:del %f' % trigger_delay)
        # self.resource.write(':SYST:AZER:STAT OFF')
        # self.resource.write(':SYST:TIME:RES:AUTO ON')

        # self.resource.write(':TRAC:TST:FORM ABS')
        # self.resource.write(':trac:feed:cont next')

        # self.resource.write(':init')
        # self.resource.assert_trigger()
        # self.resource.wait_for_srq()

        datatemp = self.resource.query_ascii_values(':calc:data?', container = numpy.array)


        self.resource.write(':calc:category pow')
        self.resource.write(':calc')
        power = self.resource.query_ascii_values(':calc:data?', container = numpy.array)

        # li = range(0,datatemp.size)
        # currents = numpy.take(datatemp, [n for n in li if n % 5 == 1])
        if verbose == 1:
            print "Wavelength: %fnm, Power: %fdBm" % (1e9*datatemp[0], power[0]) 

        # averageCurrent = numpy.mean(currents)

        # if verbose==1:
            #print "Current Standard deviation: ", numpy.std(currents)
            # print "Current Average: ", averageCurrent

        return numpy.append(datatemp,power)


    # def measVoltage(self, number_of_readings = 10, trigger_delay = 0.1, verbose = 1):

        # self.resource.write(':stat:pres')
        # self.resource.write('*cls')
        # self.resource.write(':stat:meas:enab 512')
        # self.resource.write('*sre 1')

        # self.resource.write(':trac:cle')
        # self.resource.write(':trac:poin %d' % number_of_readings)

        # self.resource.write(':sens:func "voltage"')
        # self.resource.write(':sens:func:conc on')

        # # self.resource.write(':trac:feed sense1')

        # self.resource.write(':trig:coun %d' % number_of_readings)
        # self.resource.write(':trig:del %f' % trigger_delay)
        # self.resource.write(':SYST:AZER:STAT OFF')
        # self.resource.write(':SYST:TIME:RES:AUTO ON')

        # self.resource.write(':TRAC:TST:FORM ABS')
        # self.resource.write(':trac:feed:cont next')

        # self.resource.write(':init')
        # # self.resource.assert_trigger()
        # # self.resource.wait_for_srq()

        # datatemp = self.resource.query_ascii_values('trac:data?', container = numpy.array)

        # li = range(0,datatemp.size)
        # voltages = numpy.take(datatemp, [n for n in li if n % 5 == 0])

        # averageVoltage = numpy.mean(voltages)

        # if verbose==1:
            # #print "Current Standard deviation: ", numpy.std(currents)
            # print "Voltage Average: ", averageVoltage

        # return averageVoltage


        # # self.resource.write(':sense:voltage:protection:level %f' % vlim)



    # def getCurrent(self, number_of_readings = 10, verbose = 0):
        # # h = visa.instrument("GPIB::" + str(self.gpib_address))
        # # rm = visa.ResourceManager()

        # # self.resource.write(':*RST')
        # # setup the 2400 to generate an SRQ on buffer full 
        # self.resource.write(':*ESE 0')
        # self.resource.write(':*CLS')
        # self.resource.write(':STAT:MEAS:ENAB 512')
        # self.resource.write(':*SRE 1')
        # #% buffer set up
        # self.resource.write(':TRAC:CLE')
        # self.resource.write(':TRAC:POIN 10')    


        # self.resource.write(':SENS:FUNC "CURRENT"')
        # self.resource.write(':SENS:FUNC:CONC ON')
        # self.resource.write(':SENS:CURRENT:RANG:AUTO OFF')
        # #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # # IMPORTANT: if the unit goes into compliance, 
        # # adjust the compliance or the range value
        # #h.write(':SENS:VOLT:PROT:LEV 20') % voltage compliance
        # #h.write(':SENS:VOLT:RANG 20')   % volt measurement range
        # #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # self.resource.write(':SENS:CURRENT:NPLC 1')
        # #h.write(':FORM:ELEM:SENS VOLT,CURR')
        # self.resource.write(':TRIG:COUN 10')
        # self.resource.write(':TRIG:DEL 0')
        # self.resource.write(':SYST:AZER:STAT OFF')
        # self.resource.write(':SYST:TIME:RES:AUTO ON')
        # self.resource.write(':TRAC:TST:FORM ABS')
        # self.resource.write(':TRAC:FEED:CONT NEXT')
        # self.resource.write(':OUTP ON')
        # self.resource.write(':INIT')

        # #% Used the serail poll function to wait for SRQ
        # #val = [1];          % 1st instrument in the gpib object, not the gpib add
        # #spoll(obj1,val);    % keep control until SRQ
        # #fprintf(obj1,':TRAC:DATA?')

        # #% reset all the registers & clean up
        # #% if the registers are not properly reset, 
        # #% subsequent runs will not work!

        # current_data = self.resource.ask_for_values("trace:data?")

        # currentsum = 0
        # for i in range(0,len(current_data),5):
                # currentsum = currentsum + current_data[i+1]

        # averageCurrent = currentsum / number_of_readings
                
        # if verbose==1:
            # #print "Current Standard deviation: ", numpy.std(currents)
            # print "Current Average: ", averageCurrent
        # return averageCurrent



    # def getVoltage(self, number_of_readings = 10, verbose = 0):
        # # h = visa.instrument("GPIB::" + str(self.gpib_address))
        # self.resource.write("*rst; status:preset; *cls")
        # interval_in_ms = 1
        # self.resource.write("status:measurement:enable 512; *sre 1")
        # self.resource.write("sample:count %d" % number_of_readings)
        # self.resource.write("trigger:source bus")
        # self.resource.write("trigger:delay %f" % (interval_in_ms / 1000.0))
        # self.resource.write("trace:points %d" % number_of_readings)
        # self.resource.write("FUNCTION \'VOLT:DC\'")
        # self.resource.write("trace:feed sense1; feed:control next")
        # self.resource.write("initiate")
        # self.resource.trigger()
        # self.resource.wait_for_srq()
        # voltages = self.resource.ask_for_values("trace:data?")
        # averageVoltage = sum(voltages)/len(voltages)
        # if verbose==1:
            # print "Voltage Standard deviation: ", numpy.std(voltages)
            # print "Voltage Average: ", averageVoltage
        # return averageVoltage


if __name__=='__main__':
    rm = visa.ResourceManager()
    supply = AQ6370D(rm, gpib_address = 1, wait = 0.5)
    # print supply.getCurrent()
