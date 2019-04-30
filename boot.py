import pycom
from machine import SD
import os

pycom.wifi_on_boot(False)
pycom.heartbeat(False)
pycom.rgbled(0x331C00)

id = pycom.nvs_get('msg_id')
if id is None or id == 65535:
    pycom.nvs_set('msg_id', 0)

#sd = SD()
#os.mount(sd, '/sd')
