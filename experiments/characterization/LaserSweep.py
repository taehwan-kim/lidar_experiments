#!/usr/bin/python
# .py

from includes import *
import SANTEC510_v2
import SANTEC210
import JasonECL
import PowerMeter

# Main thing
def sweep_laser(file_handle, start, stop, step):

    wavelengths = frange(start, stop, step)
    losses = []
    laser = JasonECL.JasonECL(com_port = 3, home = False, verbose = False)
    # laser = SANTEC510_v2.SantecLaser(gpibAddress=28)
    #laser = SANTEC210.Santec210()
    #laser.setLaserPower(3.5)

    power_meter = PowerMeter.powerMeter(gpibAddress=24)        
    
    for wavelength in wavelengths:
        laser.setLambda(wavelength)
        time.sleep(0.1)
        power_meter.readPower()
        time.sleep(0.05)
        losses.append(power_meter.powerB)
        print ("Wavelength: %f nm, Reading:%f dBm" % (wavelength, power_meter.powerB))
        file_handle.write(str(wavelength)+','+str(power_meter.powerB)+'\n')

    file_handle.close()

    p.figure()
    p.plot(wavelengths,losses,'-')
    p.xlabel('Wavelength')
    p.ylabel('Loss (dB)')
    p.savefig(file_name+'.png')
    p.show()
    p.close()

# Run the program
if __name__ == "__main__":
    
    if not len(sys.argv) == 6:
        print "USAGE: start, stop, step are in nm"  
        print "    LaserSweep chip label start stop step"
        sys.exit(1)

    dir_name='../../../data/EOS18/sweeps/%s' % sys.argv[1]
    # Create directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name) 
        
    date_time=str(datetime.datetime.now())
    # Create results directory
    file_name = "%s/%s_%snm-%snm_%s-%s-%s.csv" % (dir_name, sys.argv[2], sys.argv[3], sys.argv[4], \
        date_time[0:10], date_time[11:13], date_time[14:16])
    file_handle = open(file_name, 'w')
    sweep_laser(file_handle, float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))
    sys.exit(0)
