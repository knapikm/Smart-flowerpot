from network import Sigfox
import socket
import struct
import pycom
pycom.rgbled(0x002200)
# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as DOWNLINK specified by 'True'
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)

# send values as little-endian and int, request DOWNLINK
a = s.send('test12345678')
print(a)
pycom.rgbled(0x000000)

# await DOWNLINK message
print(s.recv(32))
