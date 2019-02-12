from network import Sigfox
import socket
import struct
import pycom
import core

def sigfox_payload():
    id, temp, hum, press, voltage, moist = core.measurements()
    print(id, voltage, temp, moist)
    return bytes([(id >> 8) & 0xff]) + bytes([(id) & 0xff]) + bytearray(struct.pack("f", voltage)) \
           + bytes([temp]) + bytes([moist])

def sigfox_send():
    sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1) # init Sigfox for RCZ1 (Europe)
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW) # create a Sigfox socket
    s.setblocking(True) # make the socket blocking
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
    pycom.rgbled(0x002200)
    ret = s.send(sigfox_payload())
    print(ret)
    pycom.rgbled(0x000000)

    s.setblocking(False)
    s.close()
    return ret

# await DOWNLINK message
#print(s.recv(32))
