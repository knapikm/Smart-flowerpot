import pycom
#from machine import SD
#import os

pycom.wifi_on_boot(False)
pycom.heartbeat(False)
pycom.rgbled(0xFF8C00)

#sd = SD()
#os.mount(sd, '/sd')
