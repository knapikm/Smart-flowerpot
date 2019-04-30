from network import Sigfox
import socket
from struct import pack
import pycom
from utime import sleep
import measurements
from machine import idle

def _sigfox_payload():
    return bytes([(measurements.MSG_ID >> 8) & 0xff]) + bytes([(measurements.MSG_ID) & 0xff]) \
           + bytes([measurements.VOLTAGE]) + bytes([measurements.TEMP]) + bytes([measurements.MOIST])

def sigfox_send():
    sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1) # init Sigfox for RCZ1 (Europe)
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW) # create a Sigfox socket
    s.setblocking(True) # make the socket blocking
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
    try:
        print('Sigfox sending...')
        ret = s.send(_sigfox_payload())
        print('Sigfox done', ret)
        pycom.rgbled(0x003300)
        idle()
        sleep(0.3)
    except Exception as e:
        print('Sigfox error', e.args[0])
        pycom.rgbled(0x330000)
        idle()
        sleep(0.3)
        return 0
    s.setblocking(False)
    s.close()
    return ret

# await DOWNLINK message
#print(s.recv(32))
