from network import Bluetooth
from core import measurements
import time
import sys

'''
bluetooth = None
srv = None
char0_cb = None
char1_cb = None
char2_cb = None
char3_cb = None
'''

def conn_cb (bt_o):
    global bluetooth
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
        bluetooth.advertise(False)
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")
        bluetooth.advertise(True)

def char_read_cb_handler(chr):
    events = chr.events()
    if events & Bluetooth.CHAR_WRITE_EVENT:
        print('write', chr.value())
        # TODO: tu vypnut service aj BLE

def char_cb_handler(chr):
    print('read', chr)


def gatt_connect():
    global bluetooth
    bluetooth = Bluetooth()
    bluetooth.set_advertisement(name='SiPy')
    bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
    bluetooth.advertise(True)

def gatt_service():
    global bluetooth, srv, char0_cb, char1_cb, char2_cb, char3_cb
    srv = bluetooth.service(uuid=4321, isprimary=True, nbr_chars=4, start=False)

    id, temp, hum, light, press, voltage, moist = measurements()
    respChr = srv.characteristic(uuid=4560, value=0)
    idTempChr = srv.characteristic(uuid=4561, value="{}, {}".format(id, temp[1]))
    humPressChr = srv.characteristic(uuid=4562, value="{}, {}".format(hum, press))
    battMoistChr = srv.characteristic(uuid=4563, value="{}, {}".format(voltage, moist))

    char0_cb = respChr.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=char_cb_handler)
    char1_cb = idTempChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char_cb_handler)
    char2_cb = humPressChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char_cb_handler)
    char3_cb = battMoistChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char_cb_handler)
    srv.start()

'''
bluetooth.start_scan(20)
while bluetooth.isscanning():
    adv = bluetooth.get_adv()
    if adv:
        mac = ubinascii.hexlify(adv.mac)
        if mac == bytearray('b827ebeec52e'):
            name = bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
            print(mac, name, adv.rssi)
'''
