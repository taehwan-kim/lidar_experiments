#!/usr/bin/python
# DC3631A.py

# import the VISA module
import visa
import time

# Sample of 8164b command:         self.gpib.write(":SENS%d:POW:ATIME %d%s" % (1, avg_time, unit))
# Command: :SENSe[n]:[CHANnel[m]]:POWer:ATIMe?
# example: sens1:pow:atim?

# sets the wavelength : sour2:wav 1550NM
# [:SOURce[n]][:CHANnel[m]]:WAVelength[:CW[l]:FIXED[l]] 
# [:SOURce[n]][:CHANnel[m]]:WAVelength[:CW[l]:FIXED[l]]<wsp><value>[PM|NM|UM|MM|M]
# Sets the absolute wavelength of the output.

#[:SOURce[n]][:CHANnel[m]]:WAVelength:SWEep:STARt
#ex: wav:swe:star 1500nm

#[:SOURce[n]][:CHANnel[m]]:WAVelength:SWEep:STOP
#ex: wav:swe:stop 1550nm

class AgilentLaser:
    def __init__(self, gpib_address = 20):
        self.gpib = visa.instrument("GPIB::%d" % (gpib_address), timeout = 1)
        self.gpib.clear()

    def set_wavelength(self, wavelength):
#        try:
            self.gpib.write(":SOUR0:WAV %fNM" % (wavelength))
#            cur_wavelength = 0 
#            while (cur_wavelength < wavelength - 0.0001) or (cur_wavelength > wavelength + 0.0001) :
#                cur_wavelength = float(self.gpib.ask(":READ%d:CHAN%d:POW?" % (1, 1)))
#        except visa.VisaIOError as io_error:
#            print io_error
#            print "clearing gpib interface, retrying..."
#            self.gpib.clear()
#            self.set_wavelength(wavelength)

    def sweep_wavelength(self, start_wavelength, end_wavelength):
        self.gpib.write("WAV:SWE:STAR %fNM" % (start_wavelength))
        self.gpib.write("WAV:SWE:STOP %fNM" % (end_wavelength))
        self.gpib.write("WAV:SWE:MODE STEP")

    def read_wavelength(self):
        return float(self.gpib.ask(":WAV?"))
'''
def sweep(start_wavelength,end_wavelength,GPIBADDR):
    laser=visa.instrument("GPIB::"+str(GPIBADDR))
    gpib.write("SS "+str(start_wavelength))
    gpib.write("SE "+str(end_wavelength))
    gpib.write("SG")

def set_wavelength(set_wavelength,GPIBADDR):
    laser=visa.instrument("GPIB::"+str(GPIBADDR))
    gpib.write(":WAV "+str(set_wavelength))

def setFine(fineValue,GPIBADDR):
    laser=visa.instrument("GPIB::"+str(GPIBADDR))
    gpib.write(":WAV:FIN "+str(fineValue))

def TurnLaserON(GPIBADDR):
    laser=visa.instrument("GPIB::"+str(GPIBADDR))
    #gpib.write(":POW:STAT 1")
    gpib.write(":POW:SHUT 1")
    time.sleep(0.5) 

def TurnLaserOFF():
    time.sleep(0.5)      
'''

if __name__=='__main__':
    myLaser = AgilentLaser(gpibAddress=20)
    myLaser.set_wavelength(1540)
    for wavelength in range(15400,15600,5):
        time.sleep(0.5)
        myLaser.set_wavelength(float(wavelength)/10)
        time.sleep(0.5)
