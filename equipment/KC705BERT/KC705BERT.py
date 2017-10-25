
from KC705Packets import BERTTxPacket
from KC705Packets import BERTRxPacket

# Class with helper functions to control the BERT on the KC705

class KC705BERT:
    def __init__(self, eth, verbose = True):
        self.eth = eth

    # Delay the Tx PRBS by the set number of cycles
    def delay_tx(self, cycles):
        rx_packet = BERTRxPacket()
        self.eth.send(BERTTxPacket(TxDelay = binary_repr(cycles, 31), TxDelayStart = '1'))
        self.eth.recv(rx_packet)
        
    # Start the Rx Bit-error-rate checker
    def start_ber(self):
        rx_packet = BERTRxPacket()
        self.eth.send(BERTTxPacket(RxBERStart = '1'))
        self.eth.recv(rx_packet)
        
    # Read the rx bit-error-rate checker
    def read_ber(self, eye = False):
        rx_packet = BERTRxPacket()
        self.eth.send(BERTTxPacket())
        self.eth.recv(rx_packet)
        # Return the Eye DAC monitor value also if requested
        if eye:
            return (int(rx_packet.RxBERCount, 2), int(rx_packet.RxBitCount, 2), int(rx_packet.RxEyeDAC, 2))
        return (int(rx_packet.RxBERCount, 2), int(rx_packet.RxBitCount, 2))

    # Read the eye determined by the eye dac, as well as BER counts
    def read_eye_height(self, eye = False):
        rx_packet = BERTRxPacket()
        self.eth.send(BERTTxPacket())
        self.eth.recv(rx_packet)
        # Return the Eye DAC monitor value also if requested
        return (int(rx_packet.RxBERCount, 2), int(rx_packet.RxBitCount, 2), int(rx_packet.RxEyeDAC, 2))
        