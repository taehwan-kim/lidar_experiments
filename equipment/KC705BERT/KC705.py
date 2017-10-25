import socket
import time
import matplotlib.pyplot as p
from numpy import binary_repr

from KC705Ethernet import *
from KC705BERT import *
from KC705GTX import *

from KC705GTXDRP import *

# Python control interface for the ML705 FPGA
# Beware of the order in which bytes are received to avoid mistakes.
class KC705:
    def __init__(self):
        # Initialize ethernet connection
        self.eth = KC705Ethernet()
        # Create BERT and GTX helper classes
        self.bert = KC705BERT(self.eth)
        self.gtx = KC705GTX(self.eth)
        
    # Sweeps a receive bathtub
    def sweep_bathtub(self, max_bits = 1e8, phases = range(0, 2**8), verbose = False):
        # Set to bathtub mode
        self.gtx.set_eye_mode('bath')
        # Sweep phase
        ber = []
        for phase_idx in phases:
            # Set phase
            self.gtx.set_eye_phase(phase_idx)
            # Begin bit-error-rate check
            self.bert.start_ber()            
            # Check BER            
            (ber_count, bit_count) = self.bert.read_ber()
            # Keep checking until we hit the desired number of bits
            while (bit_count < max_bits) and (ber_count == 0):
                (ber_count, bit_count) = self.bert.read_ber()
            # Add to output
            ber.append(float(ber_count) / float(bit_count))
            if verbose:
                print "Phase: %3d, Bits = %3.2e, BER = %3.2e" % (phase_idx, bit_count, float(ber_count) / float(bit_count))

        self.gtx.set_eye_mode('off')
        
        return (phases, ber)
        
    # Sweeps a receive eye
    def sweep_eye_outline(self, phases = range(0, 2**8), verbose = False):

        # Set to bathtub mode
        self.gtx.set_eye_mode('eye')

        # Sweep phase
        ber = []
        heights = []
        for phase_idx in phases:
            # Set phase
            self.gtx.set_eye_phase(phase_idx)
            # Begin bit-error-rate check
            self.bert.start_ber()     
            # Check Eye Height            
            (ber_count, bit_count, eye_height) = self.bert.read_eye_height()
            # Add to output
            ber.append(float(ber_count) / float(bit_count))
            heights.append(eye_height)
            if verbose:
                print "Phase: %3d, Bits = %3.2e, BER = %3.2e, Eye Height = %d" % (phase_idx, bit_count, float(ber_count) / float(bit_count), eye_height)

        self.gtx.set_eye_mode('off')
        
        return (phases, heights)

    def run_ber(self, min_bits = 0, max_bits = 1e12):
        # Start the BER run
        self.bert.start_ber()     
        # Check BER            
        (ber_count, bit_count) = self.bert.read_ber()
        # Keep checking until we hit the desired number of bits
        while (bit_count < max_bits) and (bit_count < min_bits or ber_count == 0):
            (ber_count, bit_count) = self.bert.read_ber()
            time.sleep(0.02)
            if (bit_count != 0):
                print "Bits = %3.2e, BER = %3.2e\r" % (bit_count, float(ber_count) / float(bit_count)),
        print "Bits = %3.2e, BER = %3.2e" % (bit_count, float(ber_count) / float(bit_count))
        
        return (bit_count, ber_count)        
            
# Runs the Bit-Error-Rate Checker    
if __name__=='__main__':
    # Test setup
    bits_bath = 1e6;
    bits_long = 1e12;
    plot = True
    # Phases to sweep over
    phases = range(0, 2**8, 8)

    # Convert phases to UI
    ui_phases = []
    for phase in phases:
        ui_phases.append(float(phase) / 256.0)

    fpga = KC705()    
    # fpga.gtx.set_clk25_div(div = 10)    
    # fpga.gtx.set_tx_pll(divsel_out = 2, divsel45_fb = 4, divsel_fb = 4, divsel_ref = 2)
    # fpga.gtx.set_rx_pll(divsel_out = 2, divsel45_fb = 4, divsel_fb = 4, divsel_ref = 2)
    # Do a bathtub sweep
    
    #QPLL_REFCLK_DIV[4:0] = DRP 0x33 [15:11]
    #QPLL_FBDIV[9:0] = DRP 0x36 [9:0]
    #QPLL_FBDIV_RATIO[0] = DRP 0x37 [6]
    
    #QPLL_CFG[6] selects the QPLL frequency band    
    #QPLL_CFG[15:0] = DRP 0x32 [15:0]
    #QPLL_CFG[26:16] = DRP 0x33 [10:0]
    
    fpga.gtx.write_drp(4, 0x32, '000000011' + '1' '000001') # Lower Band (5.93Gbps - 8.0Gbps)
    # fpga.gtx.write_drp(4, 0x32, '000000011' + '0' '000001') # Upper Band (9.8Gbps - 12.5Gbps)	
    fpga.gtx.write_drp(4, 0x33, '10000' + '00001101000') # REFCLK_DIV = 1
    # fpga.gtx.write_drp(4, 0x33, '00000' + '00001101000') # REFCLK_DIV = 2
    # fpga.gtx.write_drp(4, 0x33, '00001' + '00001101000') # REFCLK_DIV = 3
    # fpga.gtx.write_drp(4, 0x33, '00010' + '00001101000') # REFCLK_DIV = 4
    # fpga.gtx.write_drp(4, 0x33, '00011' + '00001101000') # REFCLK_DIV = 5
    # fpga.gtx.write_drp(4, 0x36, '000000' + '0000100000') # FBDIV = 16
    # fpga.gtx.write_drp(4, 0x36, '000000' + '0000110000') # FBDIV = 20
    fpga.gtx.write_drp(4, 0x36, '000000' + '0001100000') # FBDIV = 32
    # fpga.gtx.write_drp(4, 0x36, '000000' + '0010000000') # FBDIV = 40    
    # fpga.gtx.write_drp(4, 0x36, '000000' + '0011100000') # FBDIV = 64
    # fpga.gtx.write_drp(4, 0x36, '000000' + '0100100000') # FBDIV = 80
    # fpga.gtx.write_drp(4, 0x36, '000000' + '0101110000') # FBDIV = 100
    print fpga.gtx.read_drp(4, 0x032)
    print fpga.gtx.read_drp(4, 0x033)
    print fpga.gtx.read_drp(4, 0x036)
	
	# Data rate = PLLCLK_in * FBDIV / REFCLK_DIV
    
	# Note this reset doesn't do jack sometimes, need to go in and manually reset
    fpga.gtx.reset()        
    
    # (useless, errors) = fpga.sweep_bathtub(max_bits = bits_bath, phases = phases, verbose = True)
    
    # # Get rid of zeros, so that it may be plotted on semilog axis
    # for i in range(len(errors)):
        # errors[i] = max(1 / bits_bath, errors[i])
    
    # if plot:
        # p.figure()
        # p.semilogy(ui_phases, errors)    

    # (useless, heights) = fpga.sweep_eye_outline(phases = phases, verbose = True)
    
    # # Mirror the eye opening plot, so it actually looks like an eye outline
    # eye_top = []
    # eye_bot = []
    # for i in range(len(heights)):
        # eye_top.append(float(heights[i]) / 2.0)
        # eye_bot.append(float(-heights[i]) / 2.0)
    
    # if plot:
        # p.figure()
        # p.plot(ui_phases, eye_top)
        # p.plot(ui_phases, eye_bot)
        
    #fpga.run_ber(bits_long)
    #time.sleep(1)

    # if plot:
        # p.show()
