import pycom
#from machine import SD
#import os

pycom.wifi_on_boot(False)
pycom.heartbeat(False)
pycom.rgbled(0xFF8C00)

id = pycom.nvs_get('msg_id')
if id is None:
    pycom.nvs_set('msg_id', 0)

#sd = SD()
#os.mount(sd, '/sd')
