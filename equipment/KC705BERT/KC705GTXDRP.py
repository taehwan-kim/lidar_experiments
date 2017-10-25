
# Contains classes representing the various GTX DRP registers
class DRP_00:
    def __init__(self, bits):
        self.update(bits)
    
    def to_bits(self):
        bits = ''
        bits += self.PMA_RX_CFG
        return bits

    def update(self, bits):
        self.PMA_RX_CFG         = bits[0:16]
        
class DRP_17:
    def __init__(self, bits):
        self.update(bits)
    
    def to_bits(self):
        bits = ''
        bits += self.GEN_RXUSRCLK
        bits += self.RX_DATA_WIDTH
        bits += self.CHAN_BOND_SEQ_2_CFG
        bits += self.BIAS_CFG
        bits += self.RX_CLK25_DIVIDER
        bits += self.AC_CAP_DIS
        bits += self.GTX_CFG_PWRUP
        bits += self.OOBDETECT_THRESHOLD
        return bits

    def update(self, bits):
        self.GEN_RXUSRCLK           = bits[0:1]
        self.RX_DATA_WIDTH          = bits[1:4]
        self.CHAN_BOND_SEQ_2_CFG    = bits[4:5]
        self.BIAS_CFG               = bits[5:6]
        self.RX_CLK25_DIVIDER       = bits[6:11]
        self.AC_CAP_DIS             = bits[11:12]
        self.GTX_CFG_PWRUP          = bits[12:13]
        self.OOBDETECT_THRESHOLD    = bits[13:16]
    
class DRP_23:
    def __init__(self, bits):
        self.update(bits)
    
    def to_bits(self):
        bits = ''
        bits += self.RES_15
        bits += self.TX_CLK25_DIVIDER
        bits += self.TRANS_TIME_TO_P2
        return bits

    def update(self, bits):
        self.RES_15             = bits[0:1]
        self.TX_CLK25_DIVIDER   = bits[1:6]
        self.TRANS_TIME_TO_P2   = bits[6:16]

class DRP_1B:
    def __init__(self, bits):
        self.update(bits)
    
    def to_bits(self):
        bits = ''
        bits += self.RXPLL_DIVSEL_OUT
        bits += self.RXPLL_LKDET_CFG
        bits += self.RES_10_9
        bits += self.RX_CLK_SOURCE
        bits += self.RES_7
        bits += self.RXPLL_DIVSEL45_FB
        bits += self.RXPLL_DIVSEL_FB
        bits += self.RES_0
        return bits

    def update(self, bits):
        self.RXPLL_DIVSEL_OUT   = bits[0:2]
        self.RXPLL_LKDET_CFG    = bits[2:5]
        self.RES_10_9           = bits[5:7]
        self.RX_CLK_SOURCE      = bits[7:8]
        self.RES_7              = bits[8:9]
        self.RXPLL_DIVSEL45_FB  = bits[9:10]
        self.RXPLL_DIVSEL_FB    = bits[10:14]
        self.RES_0              = bits[15:16]

class DRP_1C:
    def __init__(self, bits):
        self.update(bits)
    
    def to_bits(self):
        bits = ''
        bits += self.RX_OVERSAMPLE_MODE
        bits += self.RES_14_6
        bits += self.RXPLL_DIVSEL_REF
        bits += self.RES_0
        return bits

    def update(self, bits):
        self.RX_OVERSAMPLE_MODE = bits[0:1]
        self.RES_14_6           = bits[1:10]
        self.RXPLL_DIVSEL_REF   = bits[10:15]
        self.RES_0              = bits[15:16]
        
        
class DRP_1F:
    def __init__(self, bits):
        self.update(bits)
    
    def to_bits(self):
        bits = ''
        bits += self.TXPLL_DIVSEL_OUT
        bits += self.TXPLL_LKDET_CFG
        bits += self.RES_10_9
        bits += self.TX_CLK_SOURCE
        bits += self.RES_7
        bits += self.TXPLL_DIVSEL45_FB
        bits += self.TXPLL_DIVSEL_FB
        bits += self.RES_0
        return bits

    def update(self, bits):
        self.TXPLL_DIVSEL_OUT   = bits[0:2]
        self.TXPLL_LKDET_CFG    = bits[2:5]
        self.RES_10_9           = bits[5:7]
        self.TX_CLK_SOURCE      = bits[7:8]
        self.RES_7              = bits[8:9]
        self.TXPLL_DIVSEL45_FB  = bits[9:10]
        self.TXPLL_DIVSEL_FB    = bits[10:14]
        self.RES_0              = bits[15:16]

class DRP_20:
    def __init__(self, bits):
        self.update(bits)
    
    def to_bits(self):
        bits = ''
        bits += self.TX_OVERSAMPLE_MODE
        bits += self.RES_14_6
        bits += self.TXPLL_DIVSEL_REF
        bits += self.RES_0
        return bits

    def update(self, bits):
        self.TX_OVERSAMPLE_MODE = bits[0:1]
        self.RES_14_6           = bits[1:10]
        self.TXPLL_DIVSEL_REF   = bits[10:15]
        self.RES_0              = bits[15:16]

class DRP_2D:
    def __init__(self, bits):
        self.update(bits)
    
    def to_bits(self):
        bits = ''
        bits += self.RX_EYE_OFFSET
        bits += self.DFE_CFG     
        return bits

    def update(self, bits):
        self.RX_EYE_OFFSET      = bits[0:8]
        self.DFE_CFG            = bits[8:16]
        
class DRP_2E:
    def __init__(self, bits):
        self.update(bits)
    
    def to_bits(self):
        bits = ''
        bits += self.DFE_CAL_TIME
        bits += self.RX_EYE_SCANMODE
        bits += self.RCV_TERM_VTTRX
        bits += self.RCV_TERM_GND
        bits += self.RCV_TERMINATION_OVRD
        bits += self.RES_5
        bits += self.TERMINATION_CTRL        
        return bits

    def update(self, bits):
        self.DFE_CAL_TIME           = bits[0:5]
        self.RX_EYE_SCANMODE        = bits[5:7]
        self.RCV_TERM_VTTRX         = bits[7:8]
        self.RCV_TERM_GND           = bits[8:9]
        self.RCV_TERMINATION_OVRD   = bits[9:10]
        self.RES_5                  = bits[10:11]
        self.TERMINATION_CTRL       = bits[11:16]
        
# Not a register, but contains a dictionary mapping codes
class PLLCodes:
    def __init__(self):
        self.divsel_out = dict()
        self.divsel_out[1] = '00'
        self.divsel_out[2] = '01'
        self.divsel_out[4] = '10'
        
        self.divsel45_fb = dict()
        self.divsel45_fb[5] = '1'
        self.divsel45_fb[4] = '0'
        
        self.divsel_fb = dict()
        self.divsel_fb[2] = '00000'
        self.divsel_fb[4] = '00010'
        self.divsel_fb[5] = '00011'    
    
        self.divsel_ref = dict()
        self.divsel_ref[1] = '10000'
        self.divsel_ref[2] = '00000'
        
