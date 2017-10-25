#!/usr/bin/python
# SANTEC210.py

# import the VISA module
import visa
import time

class Santec210:
    def __init__(self):
        #self.gpib = gpibAddress
        self.laserType='Santec 210'
        self.gpib1=20
        self.gpib2=29
        self.gpib3=22
        self.gpib4=23
        self.santec1=visa.instrument("GPIB::"+str(self.gpib1), term_chars="\r\n")
        self.santec2=visa.instrument("GPIB::"+str(self.gpib2), term_chars="\r\n")
        self.santec3=visa.instrument("GPIB::"+str(self.gpib3), term_chars="\r\n")
        self.santec4=visa.instrument("GPIB::"+str(self.gpib4), term_chars="\r\n")
        self.santec1.write("LO")
        self.santec2.write("LO")
        self.santec3.write("LO")
        self.santec4.write("LO")
        
        self.santec1.write("ATE")
        self.santec2.write("ATE")
        self.santec3.write("ATE")
        self.santec4.write("ATE")
        
        
        self.active=0
        
    def setLaserPower(self,LaserPower):
        self.santec1.write("OP %.2f" % LaserPower)
        self.santec2.write("OP %.2f" % LaserPower)
        self.santec3.write("OP %.2f" % LaserPower)
        self.santec4.write("OP %.2f" % LaserPower)

    def setLambda(self,setLambda):
        if setLambda < 1630.000001 and setLambda > 1530 :
            self.santec1.write("SW 4")
            self.santec4.write("WA %.3f" % setLambda)
            if self.active != 4:
                self.active = 4
                time.sleep(1.00)
        elif setLambda < 1530.1 and setLambda > 1440 :
            self.santec1.write("SW 3")
            self.santec3.write("WA %.3f" % setLambda)
            if self.active != 3:
                self.active = 3
                time.sleep(1.00)
        elif setLambda < 1440.1 and setLambda > 1355 :
            self.santec1.write("SW 2")
            self.santec2.write("WA %.3f" % setLambda)
            if self.active != 2:
                self.active = 2
                time.sleep(1.00)
        elif setLambda < 1355.1 and setLambda > 1259.999999 :
            self.santec1.write("SW 1")
            self.santec1.write("WA %.3f" % setLambda)
            if self.active != 1:
                self.active = 1
                time.sleep(1.00)
        else :
            print "error wave out of range"


    def TurnLaserON(self):
        #laser=visa.instrument("GPIB::"+str(self.gpib))
        pass
        '''
        laser.write("DCL")
        time.sleep(2)
        # operate in automatic power control mode
        print laser.write("AF")
        time.sleep(0.5)  
        print laser.write("LO")
        time.sleep(1)
        print laser.read()
        print laser.write("WA 1522.22")
        time.sleep(0.5)
        print laser.read()
        time.sleep(0.5) 
        print laser.write("OP 1")
        print laser.read()
        time.sleep(0.5) 
        '''

'''
def sweep(startLambda,endLambda,GPIBADDR):
    laser=visa.instrument("GPIB::"+str(GPIBADDR))
    laser.write("SS "+str(startLambda))
    laser.write("SE "+str(endLambda))
    laser.write("SG")

def setLambda(setLambda,GPIBADDR):
    laser=visa.instrument("GPIB::"+str(GPIBADDR))
    laser.write(":WAV "+str(setLambda))

def setFine(fineValue,GPIBADDR):
    laser=visa.instrument("GPIB::"+str(GPIBADDR))
    laser.write(":WAV:FIN "+str(fineValue))

def TurnLaserOFF():
    time.sleep(0.5)      
'''

if __name__=='__main__':
    myLaser = Santec210()
    myLaser.TurnLaserON()

    # Max Power Output
    #myLaser.setLaserPower(10.8)
    # Turn Off
    #myLaser.setLaserPower(-25)

    # Set Power
    #myLaser.setLaserPower(-25.00)
    myLaser.setLaserPower(7.50)

    # Set Wavelength
    myLaser.setLambda(1290.66)
    # for i in range(128000, 129000):
        # print float(i) / 100.0
        # time.sleep(0.1)
        # myLaser.setLambda(float(i) / 100.0)        

