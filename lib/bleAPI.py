from network import Bluetooth
from core import measurements

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='LoPy', service_uuid=b'1234567890123456')

def conn_cb (bt_o):
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")
​
bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
​
bluetooth.advertise(True)
​​
srv = bluetooth.service(uuid=4321, isprimary=True, nbr_chars=5, start=False)

temp, hum, light, press, voltage = measurements()
tempChr = srv.characteristic(uuid=4561, value=str(temp))
humChr = srv.characteristic(uuid=4562, value=str(hum))
lightChr = srv.characteristic(uuid=4563, value=str(light))
pressChr = srv.characteristic(uuid=4564, value=str(press))
voltChr = srv.characteristic(uuid=4565, value=str(voltage))

srv.start()

def char2_cb_handler(chr):
    print('read')

char1_cb = tempChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char2_cb_handler)
char2_cb = humChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char2_cb_handler)
char3_cb = lightChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char2_cb_handler)
char4_cb = pressChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char2_cb_handler)
char5_cb = voltChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char2_cb_handler)

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
