#!/usr/local/bin python

import time
import socket
import sys
import serial

# Python wrapper code for Jason Orcutt's external cavity laser (ECL)
# Note that the power WILL change as a function of wavelength (this is not regulated by anything)
class JasonECL:
    def __init__(self, com_port = 3, home = False, verbose = False):
        self.verbose = verbose
        self.ser = serial.Serial('COM%d' % com_port, 921600, timeout=1, xonxoff=True)

        self.pos_0 = 6.0
        self.pos_6 = 0.0

        # 12 August 2013 Calibration - Chen
        # LD Current = 300 mA
        self.pos_0_wav = 1161.6
        self.pos_6_wav = 1254.5        

        # # 12 June 2012 Calibration - JSO
        # # LD Current = 300 mA
        # self.pos_0_wav = 1161.5
        # self.pos_6_wav = 1253.5

        self.first = True
        self.last_pos = self.pos_0
        # Set an initial turn-on wavelength
        if home:
            self.ser.write("1OR\r\n")
            if self.verbose:
                print "Waiting 30 seconds for ECL to stabilize"
            time.sleep(30)

    # I hate destructors in languages with AGC, but here may be an appropriate place to use it
    def __del__(self):
        self.ser.close()
        
    # Set the wavelength
    def setLambda(self, wavelength):
        if (wavelength > self.pos_6_wav) or (wavelength < self.pos_0_wav):
            raise Exception("ECL wavelength must be between %.1f and %.1f" % (self.pos_0_wav, self.pos_6_wav))
        
        pos = (self.pos_6 - self.pos_0) * (wavelength - self.pos_0_wav) / (self.pos_6_wav - self.pos_0_wav) + self.pos_0
        if self.verbose:
            print "Setting to wavelength %.3f, position %.3f" % (wavelength, pos)
        self.ser.write("1PA%.3f\r\n" % pos)
        # If it is the first time I've used this laser, probably should wait a while as it moves to its wavelength
        if self.first:
            if self.verbose:
                print "Waiting 20 seconds to move laser to first location"
            time.sleep(20)
            self.first = False
        else:
            # It takes a while to move the actual laser, so I will set an extra wait time based on how far it is
            time.sleep(6 * abs(pos - self.last_pos))
        
        self.last_pos = pos
        
if __name__=='__main__':
    myLaser = JasonECL(com_port = 3, home = False, verbose = True)
    myLaser.setLambda(1180)
    for wavelength in range(11800,11900,5):
        myLaser.setLambda(float(wavelength)/10)
        time.sleep(1)