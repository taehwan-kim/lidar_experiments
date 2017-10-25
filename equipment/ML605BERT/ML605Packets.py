
# Classes representing different types of packets to/from the FPGA

#--------------------------------------------------------------------------------------------------
# Bits transmitted to the GTX
#--------------------------------------------------------------------------------------------------
class GTXTxPacket:
    def __init__(self, \
        command                             = '0' * 4   , \
        address                             = '0' * 8   , \
        data                                = '0' * 16  , \
        filler                              = '0' * 0    ):

        # Define the port number for the BERT
        self.port_num                       = 65000
        
        self.filler                         = filler
        self.data                           = data
        self.address                        = address
        self.command                        = command

        # Output check
        if len(self.to_bits()) != self.length():
            raise ValueError("Error, expecting %d bits, got %d!" % (self.length(), str(len(self.to_bits()))))
    
    # Get scan chain length
    def length(self): 
        return 28
    
    # Construct bits from class
    def to_bits(self): 
        
        bits = self.filler
        bits += self.data
        bits += self.address
        bits += self.command
        
        # Return output
        return(bits)
    
    # Update the class from bits
    def update(self, bits): 
        
        # Check length of bits
        if len(bits) != self.length():
            raise ValueError("Error, expecting %d bits, got %d!" % (self.length(), len(bits)))
        
        # Update the bits in this class
        self.data           = bits[     0:16     ]
        self.address        = bits[     16:24    ]
        self.command        = bits[     24:28    ]
        self.filler         = '0' * 0
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Bits received from the GTX
#--------------------------------------------------------------------------------------------------
class GTXRxPacket:
    def __init__(self, \
        command                             = '0' * 4   , \
        address                             = '0' * 8   , \
        data                                = '0' * 16  , \
        filler                              = '0' * 0    ):

        # Define the port number for the BERT
        self.port_num                       = 65000
        
        self.filler                         = filler
        self.data                           = data
        self.address                        = address
        self.command                        = command

        # Output check
        if len(self.to_bits()) != self.length():
            raise ValueError("Error, expecting %d bits, got %d!" % (self.length(), str(len(self.to_bits()))))
    
    # Get scan chain length
    def length(self): 
        return 28
    
    # Construct bits from class
    def to_bits(self): 
        
        bits = self.filler
        bits += self.data
        bits += self.address
        bits += self.command
        
        # Return output
        return(bits)
    
    # Update the class from bits
    def update(self, bits): 
        
        # Check length of bits
        if len(bits) != self.length():
            raise ValueError("Error, expecting %d bits, got %d!" % (self.length(), len(bits)))
        
        # Update the bits in this class
        self.data           = bits[     0:16     ]
        self.address        = bits[     16:24    ]
        self.command        = bits[     24:28    ]
        self.filler         = '0' * 0                
#--------------------------------------------------------------------------------------------------

#==================================================================================================

#--------------------------------------------------------------------------------------------------
# Bits transmitted to the BERT
#--------------------------------------------------------------------------------------------------
class BERTTxPacket:
    def __init__(self, \
        TxDelay                             = '0' * 31  , \
        TxDelayStart                        = '0' * 1   , \
        RxBERStart                          = '0' * 1   , \
        RxBitCount                          = '0' * 55  , \
        RxBERCount                          = '0' * 55  , \
        filler                              = '0' * 0    ):

        # Define the port number for the BERT
        self.port_num                       = 65535
        
        self.filler                         = filler
        self.RxBERCount                     = RxBERCount
        self.RxBitCount                     = RxBitCount
        self.RxBERStart                     = RxBERStart
        self.TxDelayStart                   = TxDelayStart
        self.TxDelay                        = TxDelay

        # Output check
        if len(self.to_bits()) != self.length():
            raise ValueError("Error, expecting %d bits, got %d!" % (self.length(), str(len(self.to_bits()))))
    
    # Get scan chain length
    def length(self): 
        return 143
    
    # Construct bits from class
    def to_bits(self): 
        
        bits = self.filler
        bits += self.RxBERCount
        bits += self.RxBitCount
        bits += self.RxBERStart
        bits += self.TxDelayStart
        bits += self.TxDelay
        
        # Return output
        return(bits)
    
    # Update the class from bits
    def update(self, bits): 
        
        # Check length of bits
        if len(bits) != self.length():
            raise ValueError("Error, expecting %d bits, got %d!" % (self.length(), len(bits)))
        
        # Update the bits in this class
        self.RxBERCount     = bits[     0:55     ]
        self.RxBitCount     = bits[     55:110    ]
        self.RxBERStart     = bits[     110:111    ]
        self.TxDelayStart   = bits[     111:112    ]
        self.TxDelay        = bits[     112:143   ]
        self.filler         = '0' * 0
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Bits received from the BERT
#--------------------------------------------------------------------------------------------------
class BERTRxPacket:
    def __init__(self, \
        RxBitCount                          = '0' * 55  , \
        RxBERCount                          = '0' * 55  , \
        RxEyeDAC                            = '0' * 5   , \
        filler                              = '0' * 0    ):

        self.filler                         = filler
        self.RxEyeDAC                       = RxEyeDAC
        self.RxBERCount                     = RxBERCount
        self.RxBitCount                     = RxBitCount

        # Output check
        if len(self.to_bits()) != self.length():
            raise ValueError("Error, expecting %d bits, got %d!" % (self.length(), str(len(self.to_bits()))))
    
    # Get scan chain length
    def length(self): 
        return 115
    
    # Construct bits from class
    def to_bits(self): 
        
        bits = self.filler
        bits += self.RxEyeDAC
        bits += self.RxBERCount
        bits += self.RxBitCount
        
        # Return output
        return(bits)
    
    # Update the class from bits
    def update(self, bits): 
        
        # Check length of bits
        if len(bits) != self.length():
            raise ValueError("Error, expecting %d bits, got %d!" % (self.length(), len(bits)))
        
        # Update the bits in this class
        self.RxEyeDAC       = bits[     0:5     ]
        self.RxBERCount     = bits[     5:60    ]
        self.RxBitCount     = bits[     60:115  ]
        self.filler         = '0' * 0
#--------------------------------------------------------------------------------------------------
        