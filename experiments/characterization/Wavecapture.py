#!/usr/bin/python
# .py

from includes import *
import Keithley2400
import AQ6370D
import DSOX4104A
import visa
# import numpy
# import SANTEC510_v2
# import SANTEC210
# import JasonECL
# import PowerMeter

# Main thing
def wavecapture(file_name, numofsamples, wrange, wptnum, yrange, timpos):

    rm = visa.ResourceManager()
    scope = DSOX4104A.DSOX4104A(rm)
    # osa = AQ6370D.AQ6370D(rm, 1, 0.1) 
    # keithley = Keithley2400.Keithley2400(rm, 24, 0.1)
    scope.setTrigger(channel = "EXT", edge="pos")
    scope.setAcquisition(mode = "hres")

    scope.setChannelOption(channel=1, coupling="AC", bwlimit=0, display=1, impedance="FIFT", scale=yrange)
    scope.setChannelOption(channel=2, coupling="DC", bwlimit=0, display=0, impedance="ONEM", scale=1000.0)
    scope.setChannelOption(channel=3, coupling="DC", bwlimit=0, display=0, impedance="FIFT", scale=1000.0)
    scope.setChannelOption(channel=4, coupling="DC", bwlimit=0, display=0, impedance="FIFT", scale=1000.0)

    tmeas, wmeas = scope.takeWaveform(numCycles=numofsamples, channel=1, timerange=wrange, \
            wpoints=wptnum, wpointsmax=0, timeposition=timpos)


    # current = arange(start,stop,step)
    # measurement = zeros((5,len(current)))
    # measurement[0,:] = current
    # print current
    # wavelength = zeros(len(current))
    # voltage = zeros(len(current))
    # vlim = 10

    # for i in range(len(current)):
        # keithley.setCurrent(measurement[0,i], vlim)
        # keithley.turnSourceOn()
        # measurement[1,i] = keithley.measVoltage(5, 0.1, 1)

        # tempwav = zeros(5)
        # templw = zeros(5)
        # temppw = zeros(5)

        # for j in range(5):
            # temptemp = osa.measPeak(1530,20,1)
            # # print temptemp
            # # temptemp = osa.measPeak(1524,20,1)
            # tempwav[j] = temptemp[0]
            # templw[j] = temptemp[1]
            # temppw[j] = temptemp[3]
            # time.sleep(0.1)

        # # print temppw
        # # print temppw.mean()
        # measurement[2,i] = tempwav.mean()
        # measurement[3,i] = templw.mean()
        # measurement[4,i] = temppw.mean()
        # keithley.turnSourceOff()
    

    # losses = []
    # laser = JasonECL.JasonECL(com_port = 3, home = False, verbose = False)
    # laser = SANTEC510_v2.SantecLaser(gpibAddress=28)
    #laser = SANTEC210.Santec210()
    #laser.setLaserPower(3.5)

    # power_meter = PowerMeter.powerMeter(gpibAddress=24)        
    
    # for wavelength in wavelengths:
        # laser.setLambda(wavelength)
        # time.sleep(0.1)
        # power_meter.readPower()
        # time.sleep(0.05)
        # losses.append(power_meter.powerB)
        # print ("Wavelength: %f nm, Reading:%f dBm" % (wavelength, power_meter.powerB))
        # file_handle.write(str(wavelength)+','+str(power_meter.powerB)+'\n')
    sio.savemat(file_name+'.mat', {'wmeas':wmeas, 'tmeas':tmeas})

    # file_handle.close()
    # p.figure()
    # p.plot(measurement[0,:],measurement[1,:],'*-')
    # p.xlabel('Tuning Current (mA)')
    # p.ylabel('Voltage (V)')
    # p.savefig(file_name+'_voltage.png')
    # p.show()
    # p.close()

    # p.figure()
    # p.plot(measurement[0,:],measurement[2,:], 'o-')
    # p.xlabel('Tuning Current (mA)')
    # p.ylabel('Wavelength (nm)')
    # p.savefig(file_name+'_wavelength.png')
    # p.show()
    # p.close()

    # p.figure()
    # p.plot(measurement[0,:],measurement[3,:], 'o-')
    # p.xlabel('Tuning Current (mA)')
    # p.ylabel('FWHM (nm)')
    # p.savefig(file_name+'_fwhm.png')
    # p.show()
    # p.close()

    # p.figure()
    # p.plot(measurement[0,:],measurement[4,:], 'o-')
    # p.xlabel('Tuning Current (mA)')
    # p.ylabel('Laser Peak Power (dBm)')
    # p.savefig(file_name+'_power.png')
    # p.show()
    # p.close()
    # return measurement 


# Run the program
if __name__ == "__main__":
    
    if not len(sys.argv) == 6:
        print "USAGE:"  
        print "    Wavecapture numofsamples wrange wptnum yrange timpos"
        # label start stop step"
        sys.exit(1)

    dir_name='../data/laser/linewidth'
    # Create directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name) 
        
    date_time=str(datetime.datetime.now())
    # Create results directory
    file_name = "%s/result_%s-%s-%s" % (dir_name, date_time[0:10], date_time[11:13], date_time[14:16])
    # file_handle = open(file_name, 'w')
    wavecapture(file_name, int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))
    # print measured
    sys.exit(0)
