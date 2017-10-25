import socket
import time
from numpy import binary_repr

# ML605 Ethernet
# This is a very simple protocol that will send packets to the FPGA
# via ethernet. Right now, the FPGA is hardcoded to receive 64B
# (minimum length) ethernet packets

# Because windows is stupid and does not allow transmission of
# raw ethernet packets due to security concerns after Windows XP,
# this actually transmits a full IP/UDP header, which the FPGA will
# currently know to strip away to get at the data.

# The amount of payload available per ethernet packet is thus only
# 64B - 18B (ethernet header) - 20B (IPv4 Header) - 8B (UDP Header) = 18B
# Which is actually still a lot. I will probably work on making this
# interface a bit better in the future if higher throughput is needed

# Beware of the order in which bytes are received to avoid mistakes.
class ML605Ethernet:
    def __init__(self, max_payload_bytes = 18, verbose = True):

        self.fpga_ip = '169.254.1.0'
        self.rx_port = 65535
    
        self.max_payload_bytes = max_payload_bytes
        self.payload_bits = self.max_payload_bytes * 8        
        
        # Setup the the sockets used for sending and receiving
        self.tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        
        self.rx_socket.bind(('', self.rx_port))
        self.rx_socket.settimeout(0.2)
        # self.tx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.tx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # # Try pinging the FPGA via Ethernet
        # self.tx_socket.sendto('HELLO THERE FPGA!!', (self.fpga_ip, self.fpga_bert_port))
        # response = self.rx_socket.recv(100)
        # if not response == 'HELLO THERE FPGA!!':
            # raise Exception("Could not connect to FPGA");
    
    # Sends bits to the FPGA, will pad bits if the send bits is smaller than the payload size
    # The FPGA will receive the payload with the LSB delivered first
    # Padding is added to the MSB        
    def send(self, packet):
        bits = packet.to_bits()
        # Check payload size
        if len(bits) > self.payload_bits:
            raise Exception("Maximum ethernet payload bits (%d) exceeded (%d)" % 
                (self.payload_bits, len(bits)))
        # Pad with zeros
        bits = '0' * (self.payload_bits - len(bits)) + bits
        # This is a bit tricky, byte-ify everything
        bytes = ''
        for i in range(self.max_payload_bytes-1, -1, -1):
            byte = chr(int(bits[i*8:(i+1)*8], 2))
            bytes += byte
            
        # Send to the FPGA
        self.tx_socket.sendto(bytes, (self.fpga_ip, packet.port_num))

    # Receive bits from the FPGA, this will fill in all the fields of the
    # provided payload with the correct bits
    def recv(self, packet):
        
        dataseq = self.rx_socket.recv(8192)
        rdata = dataseq.encode('hex')
        rdata = list(rdata)
        # reverse in groups of 8
        bits_out = ''
        for i in range(self.max_payload_bytes-1, -1, -1):
            bits_out += binary_repr(int(rdata[i*2]+rdata[i*2+1], 16), 8)
        
        # Prune the top filler bits before creating class
        packet.update(bits_out[self.payload_bits - packet.length():])

    # def sync_fpga(self):    
        # self.send_bits(self.bits.to_bits())
    
        # dsize = int(ceil(len(rdata)/4.0))
        # rbuffer = ""
        # for i in range(dsize):
            # rdata[i*4], rdata[i*4+2] = rdata[i*4+2], rdata[i*4]
            # rdata[i*4+1], rdata[i*4+3] = rdata[i*4+3], rdata[i*4+1]
            # tmp = binary_repr(int(''.join(rdata[i*4:i*4+4]),16),16)
            # rbuffer += tmp
        # print int(rbuffer[1:32], 2)
        # print len(rbuffer)
        # print binary_repr
        
# HOST = '169.254.108.76'
# # rx_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# tx_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# rx_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # tx_s.bind(('255.255.255.255', 65534))
# rx_s.bind(('', 65534))
# tx_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# tx_s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# while True:
    # tx_s.sendto('FABAB' + '0'*13, ('255.255.255.255', 65534))
    # message = rx_s.recv(100)
    # print "Got data: %s" % repr(message)
    # time.sleep(2)

# # rx_s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
# # dst_addr = "\xff\xff\xff\xff\xff\xff"
# # src_addr = "\x01\x02\x03\x04\x05\x06"
# # ethertype = "\x08\x01"
# # payload = ("["*30)+"PAYLOAD"+("]"*30)
# # checksum = "\x1a\x2b\x3c\x4d"
# # rx_s.send(dst_addr+src_addr+ethertype+payload+checksum)
# # rx_s.sendto('A'*30, ('255.255.255.255', 65534))
# # rx_s.settimeout(5)
# # i = 0
# # while True:
    # # # if i % 3 == 0:
        # # # rx_s.sendto('B'*5, ('169.254.108.77', 65534))
        # # # message = rx_s.recvfrom(100)
        # # # print "Got data: %s" % repr(message)
    # # message = rx_s.recv(100)
    # # print "Got data: %s" % repr(message)
    # # i+= 1

# Runs the Bit-Error-Rate Checker    
if __name__=='__main__':
    eth = ML605Ethernet()
    tx_pack = ML605Packets.BERTTxPacket()
    # eth.send_bits('1' + binary_repr(1234567890, 31))
    # eth.bits.TxDelay = binary_repr(1234567890, 31)
    tx_pack.TxDelay = binary_repr(0, 31)
    tx_pack.RxBERStart = '1'
    tx_pack.TxDelayStart = '0'

    # Receive bits
    rx_pack = ML605Packets.BERTRxPacket()

    # Send to FPGA and tell it to start
    eth.send(tx_pack)
    # Receive from the FPGA
    eth.recv(rx_pack)

    while True:
        # Just monitor the BER, don't need to tell it to restart
        tx_pack.RxBERStart = '0'
        eth.send(tx_pack)
        # Receive from the FPGA
        eth.recv(rx_pack)
        print "Bit Count: %.2e Bit Errors: %.2e\r" % (int(rx_pack.RxBitCount, 2), int(rx_pack.RxBERCount, 2)),
        # Sleep for a while, ethernet is too fast
        time.sleep(0.05)        
        