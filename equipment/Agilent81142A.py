#!/usr/bin/python

# import the VISA module
import visa
import time

# Function generator
class Agilent81142A:
    
    # This machine does not seem to support anything other than SI units!
    # To make it work with current interface, we can adopt unit scaling factors for us to manually scale
    # things to SI

    def __init__(self, gpib_address = 30, wait = 0.5):
        self.gpib_address = gpib_address

        self.gpib = visa.instrument("GPIB::%d" % (gpib_address))
        self.wait = wait
        
        self.volt_unit_scale = dict()
        self.volt_unit_scale['V'] = 1
        self.volt_unit_scale['mV'] = 1e-3
        self.volt_unit_scale['uV'] = 1e-6

        self.freq_unit_scale = dict()
        self.freq_unit_scale['Hz'] = 1
        self.freq_unit_scale['MHz'] = 1e6
        self.freq_unit_scale['GHz'] = 1e9

        self.time_unit_scale = dict()
        self.time_unit_scale['s'] = 1
        self.time_unit_scale['us'] = 1e-6
        self.time_unit_scale['ns'] = 1e-9
        self.time_unit_scale['ps'] = 1e-12

    def ConfigClkOut(self, amp, offset, volt_unit = 'mV'):
        # HI            = offset + ampl/2
        # LO            = offset - ampl/2
        
        self.SetClkOutAmp(amp, volt_unit)
        self.SetClkOutOffset(offset, volt_unit) 
        time.sleep(self.wait)

    def ConfigDataOut(self, delay, duty_cycle, amp, offset, time_unit = 'ps', volt_unit = 'mV'):
        # HI            = offset + ampl/2
        # LO            = offset - ampl/2
        
        self.SetDataOutPulse()
        self.SetDataOutAmp(amp, volt_unit)
        self.SetDataOutOffset(offset, volt_unit) 
        self.SetDataOutDutyCycle(duty_cycle)
        self.SetDelay(delay, time_unit)
        time.sleep(self.wait)

    def SetDataOutPulse(self):
        self.gpib.write('OUTP1:FORM PULS')
    
    def SetDelay(self, delay, unit = 'ps', channel = 1):
        self.gpib.write('OUTP1:DEL %g' % (delay * self.time_unit_scale[unit]))

    def SetPhase(self,phase,ClockFreq):
        rateFloat = float(ClockFreq)
        period = (1/rateFloat)*1000     # ps
        #delay = ((float(phase)-180)/360)*period
        delay = ((float(phase)-0)/360)*period
        print 'The phase is '+str(phase)+' and the delay is '+str(delay)
        self.SetDelay(delay)

    def SetDataOutAmp(self, amp, unit = 'mV'):
        self.gpib.write('SOUR1:VOLT:LEV:IMM:AMPL %g' % (amp * self.volt_unit_scale[unit]))

    def SetDataOutHigh(self, high, unit = 'mV'):
        self.gpib.write('SOUR1:VOLT:LEV:IMM:HIGH %g' % (high * self.volt_unit_scale[unit]))

    def SetDataOutLow(self, low, unit = 'mV'):
        self.gpib.write('SOUR1:VOLT:LEV:IMM:LOW %g' % (low * self.volt_unit_scale[unit]))

    def SetDataOutOffset(self, offset, unit = 'mV'):
        self.gpib.write('SOUR1:VOLT:LEV:IMM:OFFS %g' % (offset * self.volt_unit_scale[unit]))
    
    def SetDataOutDutyCycle(self, duty_cycle):
        self.gpib.write('OUTP1:DCYC %g' % (duty_cycle))

    def SetClkFreq(self, freq, unit = 'GHz'):
        self.gpib.write('SOUR9:FREQ %g' % (freq * self.freq_unit_scale[unit]))

    def SetFreq(self, freq, unit = 'GHz'):
        self.SetClkFreq(freq, unit)

    def SetClkOutAmp(self, amp, unit = 'mV'):
        self.gpib.write('SOUR2:VOLT:LEV:IMM:AMPL %g' % (amp * self.volt_unit_scale[unit]))

    def SetClkOutHigh(self, high, unit = 'mV'):
        self.gpib.write('SOUR2:VOLT:LEV:IMM:HIGH %g' % (high * self.volt_unit_scale[unit]))

    def SetClkOutLow(self, low, unit = 'mV'):
        self.gpib.write('SOUR2:VOLT:LEV:IMM:LOW %g' % (low * self.volt_unit_scale[unit]))

    def SetClkOutOffset(self, offset, unit = 'mV'):
        self.gpib.write('SOUR2:VOLT:LEV:IMM:OFFS %g' % (offset * self.volt_unit_scale[unit]))
    
    def SetOutputOn(self):
        self.gpib.write('OUTP1:CENT CONN')

    def SetOutputOff(self):
        self.gpib.write('OUTP1:CENT DISC')

    def Reset(self):
        self.gpib.write('*RST')

    def ReadStatusByte(self):
        return self.gpib.ask_for_values("*STB?")[0]

#### Main Program ####
# Run this to debug  #
######################
if __name__=='__main__':
    func_gen = Agilent81142A(gpib_address = 30, wait = 0.5)    
    func_gen.Reset()
    func_gen.SetOutputOn()
    for i in range(0, 10):
        func_gen.SetClkFreq(1 + i * 0.5, unit = 'GHz')
        func_gen.SetDelay(i * 20, unit = 'ps')
        func_gen.SetDataOutOffset(i * 33, unit = 'mV')
        func_gen.SetDataOutAmp(i * 50, unit = 'mV')
        time.sleep(2)
    
    func_gen.SetOutputOff()
    
