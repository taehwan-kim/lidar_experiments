
from numpy import binary_repr

from ML605Packets import GTXTxPacket
from ML605Packets import GTXRxPacket
from ML605GTXDRP import *

# Class with helper functions to control an ML605 GTX transceiver
class ML605GTX:
    def __init__(self, eth, verbose = True):
        self.eth = eth
        self.pll_codes = PLLCodes()

    # Read a DRP register
    def read_drp(self, address):
        # Some checks
        if (address < 0) or (address > 255):
            raise Exception("DRP register addresses must be between 0 and 255")

        rx_packet = GTXRxPacket()
        self.eth.send(GTXTxPacket(command = '0000', address = binary_repr(address, 8)))
        self.eth.recv(rx_packet)
        return rx_packet.data
        
    # Write a DRP register
    def write_drp(self, address, data):
        # Some checks
        if (address < 0) or (address > 255):
            raise Exception("DRP register addresses must be between 0 and 255")
        if len(data) is not 16:
            raise Exception("Expecting 16 bits for data, got %d", len(data))
        
        rx_packet = GTXRxPacket()
        self.eth.send(GTXTxPacket(command = '0001', address = binary_repr(address, 8), data = data))
        self.eth.recv(rx_packet)
        return rx_packet.data
        
    # Resets the GTX transceiver
    def reset(self):
        rx_packet = GTXRxPacket()
        self.eth.send(GTXTxPacket(command = '1111'))
        self.eth.recv(rx_packet)
        return rx_packet.data        
    
    # Sets properties for the tx pll
    def set_tx_pll(self, divsel_out, divsel45_fb, divsel_fb, divsel_ref):
        # Read values of the DRP registers, so we know values of reserved fields
        drp_1f = DRP_1F(self.read_drp(0x1f))
        drp_20 = DRP_20(self.read_drp(0x20))
        
        # Set new values
        drp_1f.TXPLL_DIVSEL_OUT = self.pll_codes.divsel_out[divsel_out]
        drp_1f.TXPLL_DIVSEL45_FB = self.pll_codes.divsel45_fb[divsel45_fb]
        drp_1f.TXPLL_DIVSEL_FB = self.pll_codes.divsel_fb[divsel_fb]
        drp_20.TXPLL_DIVSEL_REF = self.pll_codes.divsel_ref[divsel_ref]
        
        # Write values
        self.write_drp(0x1f, drp_1f.to_bits())
        self.write_drp(0x20, drp_20.to_bits())
                
    # Sets properties for the rx pll
    def set_rx_pll(self, divsel_out, divsel45_fb, divsel_fb, divsel_ref):
        # Read values of the DRP registers, so we know values of reserved fields
        drp_1b = DRP_1B(self.read_drp(0x1b))
        drp_1c = DRP_1C(self.read_drp(0x1c))
        
        # Set new values
        drp_1b.RXPLL_DIVSEL_OUT = self.pll_codes.divsel_out[divsel_out]
        drp_1b.RXPLL_DIVSEL45_FB = self.pll_codes.divsel45_fb[divsel45_fb]
        drp_1b.RXPLL_DIVSEL_FB = self.pll_codes.divsel_fb[divsel_fb]
        drp_1c.RXPLL_DIVSEL_REF = self.pll_codes.divsel_ref[divsel_ref]
        
        # Write values
        self.write_drp(0x1b, drp_1b.to_bits())
        self.write_drp(0x1c, drp_1c.to_bits())
        
    # Sets the clk25 divider
    def set_clk25_div(self, div):
        # Check validity of divider
        if (div < 1) or (div > 32):
            raise Exception("CLK25_DIVIDER must be between 1 and 32")
        
        # Read values of the DRP registers, so we know values of reserved fields
        drp_17 = DRP_17(self.read_drp(0x17))
        drp_23 = DRP_23(self.read_drp(0x23))        
        
        # Set new values
        drp_17.RX_CLK25_DIVIDER = binary_repr(div - 1, 5)
        drp_23.RXPLL_DIVSEL45_FB = binary_repr(div - 1, 5)
        
        # Write values
        self.write_drp(0x17, drp_17.to_bits())
        self.write_drp(0x23, drp_17.to_bits())
        
    # Sets scan modes
    def set_eye_mode(self, mode):
        # Read DRP registers (2E for eye scan mode, 00 for CDR config)
        drp_2e = DRP_2E(self.read_drp(0x2e))
        drp_00 = DRP_00(self.read_drp(0x00))
        # Turn off eye mode
        if mode == 'off':
            drp_2e.RX_EYE_SCANMODE = '00'
            drp_00.PMA_RX_CFG = '1110000000001000'
        # Turn on horizontal eye scan mode
        elif mode == 'bath':
            drp_2e.RX_EYE_SCANMODE = '10'
            drp_00.PMA_RX_CFG = '1110000000000000'
        # Turn on full eye outline mode
        elif mode == 'eye':
            drp_2e.RX_EYE_SCANMODE = '01'
            drp_00.PMA_RX_CFG = '1110000000001000'
        else:
            raise Exception("Unknown eye mode: %s. Valid choices are 'off', 'bath', and 'eye'", mode)

        self.write_drp(0x00, drp_00.to_bits())        
        self.write_drp(0x2e, drp_2e.to_bits())        

    # Sets the phase of the receiver in eye sweep mode
    def set_eye_phase(self, phase_idx):
        if (phase_idx < 0) or (phase_idx > 255):
            raise Exception("Eye phase index must be between 0 (0 UI) and 255 (1.0 UI)")        
        drp_2d = DRP_2D(self.read_drp(0x2d))
        drp_2d.RX_EYE_OFFSET = binary_repr(phase_idx, 8)
        self.write_drp(0x2d, drp_2d.to_bits())
    