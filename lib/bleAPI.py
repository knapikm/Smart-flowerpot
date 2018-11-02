import time​
import ubinascii
from network import Bluetooth

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='LoPy', service_uuid=b'1234567890123456')
​
py = Pysense()
mp = MPL3115A2(pysense=py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
si = SI7006A20(pysense=py)
lt = LTR329ALS01(pysense=py)
acc = LIS2HH12(pysense=py)

def measurements():
    global py, mp, si, lt, acc
    temp_mp = int(mp.temperature()* 100)/100.0 #bytearray(int(mp.temperature()* 10)/10.0))
    mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
    #alt = mp.altitude()
    press = mpp.pressure()
    temp_si = int(si.temperature()* 100)/100.0
    hum = int(si.humidity()*100)/100.0
    #dewPoint = (si.dew_point()*100)/100.0
    light = lt.light()
    #acc
    voltage = py.read_battery_voltage()
    return (temp_mp, temp_si), hum, light, press, voltage



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
​
srv1 = bluetooth.service(uuid=b'1234567890123456', isprimary=True, nbr_chars=5, start=False)
chr1 = srv1.characteristic(uuid=b'ab34567890123456', value=5)
srv1.stop()
​
char1_read_counter = 0
def char1_cb_handler(chr):
    global char1_read_counter
    char1_read_counter += 1
​
    events = chr.events()
    if  events & Bluetooth.CHAR_WRITE_EVENT:
        print("Write request with value = {}".format(chr.value()))
    else:
        if char1_read_counter < 3:
            print('Read request on char 1')
        else:
            return 'ABC DEF'
​
char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)
​
srv2 = bluetooth.service(uuid=4321, isprimary=True)
​
chr2 = srv2.characteristic(uuid=4567, value=prepare_payload_for_publish())
srv2.start()

char2_read_counter = 0xF0
def char2_cb_handler(chr):
    global char2_read_counter
    char2_read_counter += 1
    if char2_read_counter > 0xF1:
        return char2_read_counter
​
char2_cb = chr2.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char2_cb_handler)

bluetooth.start_scan(20)
while bluetooth.isscanning():
    adv = bluetooth.get_adv()
    if adv:
        mac = ubinascii.hexlify(adv.mac)
        if mac == bytearray('b827ebeec52e'):
            name = bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
            print(mac, name, adv.rssi)
