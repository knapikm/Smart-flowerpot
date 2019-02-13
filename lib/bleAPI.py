from network import Bluetooth
import core
import time
import sys
import pycom

bluetooth = None
srv = None

def conn_cb (bt_o):
    global bluetooth
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
        bluetooth.advertise(False)
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")
        bluetooth.advertise(True)

def char_cb_handler(chr):
    global bluetooth, srv
    events = chr.events()
    if events & Bluetooth.CHAR_READ_EVENT:
        print('read', chr)
    if events & Bluetooth.CHAR_WRITE_EVENT:
        print('write', chr.value())
        pycom.nvs_set('ble', 1)
        srv.stop()

def gatt_connect():
    global bluetooth
    bluetooth = Bluetooth()
    bluetooth.set_advertisement(name='SiPy')
    bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
    bluetooth.advertise(True)

def gatt_service():
    global bluetooth, srv
    srv = bluetooth.service(uuid=4321, isprimary=True, nbr_chars=4, start=False)

    id, temp, voltage, moist = core.measurements()
    respChr = srv.characteristic(uuid=4560, value=0)
    idTempChr = srv.characteristic(uuid=4561, value="{}, {}".format(id, temp))
    battMoistChr = srv.characteristic(uuid=4563, value="{}, {}".format(voltage, moist))

    char0_cb = respChr.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=char_cb_handler)
    char1_cb = idTempChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char_cb_handler)
    char2_cb = battMoistChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char_cb_handler)
    srv.start()
