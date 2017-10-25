#!/usr/bin/python
# DC3631A.py

# import the VISA module
import visa
import time


class SantecLaser:
    def __init__(self, gpib_address = 28, verbose = False):
        
        # Check python version
        self.legacy = (float(visa.__version__) < 1.6)
        
        if self.legacy:
            self.gpib = visa.instrument("GPIB::%d" % (gpib_address))
        else:
            self.gpib = visa.ResourceManager().open_resource("GPIB::%d" % (gpib_address))
        self.gpib.clear()

    # Sets the output trigger behavior for the santec
    # Modes: 0 = none, 1 = stop, 2 = start, 3 = step
    # Step size given in nanometers (0.005 - 1.0)
    def set_out_trigger(self, mode = 3, step = 0.005):
        # Since the step size is affected by the sweep speed, set the sweep speed first
        self.gpib.write(":WAV:SWE:SPE %.1f" % (step * 1000))
        
        self.gpib.write(":TRIG:OUTP %d" % (mode))
        self.gpib.write(":TRIG:OUTP:STEP %.3f" % (step))

    def set_wavelength(self, wavelength):
        try:
            self.gpib.write(":WAV %f" % (wavelength))
            cur_wavelength = 0 
            while (cur_wavelength < wavelength - 0.0001) or (cur_wavelength > wavelength + 0.0001) :
                cur_wavelength = float(self.gpib.ask(":WAV?"))
            time.sleep(0.025)       
 
        except visa.VisaIOError as io_error:
            print io_error
            print "clearing gpib interface, retrying..."
            self.gpib.clear()
            self.set_wavelength(wavelength)

    # speed is given in nm/s
    # mode 0 = step operation, one way
    # mode 1 = continuous operation, one way
    # mode 2 = step operation, two way
    # mode 3 = continuous operation, two way
    # Note that speed in nm/s also affects the trigger step wavelength at a
    # ratio of 1000 to 1 (maximum 1 trigger every ms). 5 nm/s gives the finest trigger 
    def sweep_wavelength(self, start_wavelength, stop_wavelength, speed=5, two_way=False):
        self.gpib.write(":WAV:SWE:MOD %d" % (3 if two_way else 1))
        self.gpib.write(":WAV:SWE:SPE %.1f" % (speed))
        self.gpib.write(":WAV:SWE:STAR %.3f" % (start_wavelength))
        self.gpib.write(":WAV:SWE:STOP %.3f" % (stop_wavelength))
        self.gpib.write(":WAV:SWE 1")

    def read_wavelength(self):
        return float(self.gpib.ask(":WAV?"))

    def get_wavelength_range(self):
        return (1260, 1360)

    def is_valid_wavelength(self, wavelength):
        wave_range = self.get_wavelength_range()
        return (wavelength >= wave_range[0]) and (wavelength <= wave_range[1])

    def is_valid_wavelength_step(self, step):
        return step >= 0.005

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
    myLaser = SantecLaser(gpib_address=28)
    #myLaser.set_wavelength(1290)
    myLaser.set_out_trigger(mode=3, step=0.005)
    myLaser.sweep_wavelength(1260.0, 1360.0, two_way=False)
    time.sleep(0.5)
