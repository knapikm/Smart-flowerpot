from network import Bluetooth
import measurements
import pycom
import ubinascii
import logger

GATT_CLIENT_MAC = 'b827ebeec52e'
ble = None
srv = None

def con_cb(bt_o):
    global ble
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
        ble.advertise(False)
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")
        ble.advertise(True)


def char_cb(chr):
    global srv
    events = chr.events()
    if events & Bluetooth.CHAR_READ_EVENT:
        print('read', chr)
    if events & Bluetooth.CHAR_WRITE_EVENT:
        print('write', chr.value())
        pycom.nvs_set('ble', 1)
        srv.stop()
        logger.GATT = True


def gatt_connect():
    global ble
    ble = Bluetooth()
    ble.set_advertisement(name='SiPy')
    ble.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=con_cb)
    ble.advertise(True)


def gatt_service():
    global ble, srv
    srv = ble.service(uuid=4321, isprimary=True, nbr_chars=3, start=False)

    respChr = srv.characteristic(uuid=4560, value=0)
    idTempChr = srv.characteristic(uuid=4561, value="{}, {}".format(measurements.MSG_ID, measurements.TEMP))
    battMoistChr = srv.characteristic(uuid=4562, value="{}, {}".format(measurements.VOLTAGE, measurements.MOIST))

    char0_cb = respChr.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=char_cb)
    char1_cb = idTempChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char_cb)
    char2_cb = battMoistChr.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char_cb)
    srv.start()


def find_ble(testCase=None):
    bluetooth = Bluetooth()
    try:
        if isinstance(testCase, Exception):
            raise testCase
        bluetooth.start_scan(5)
        while bluetooth.isscanning():
            adv = bluetooth.get_adv()
            if adv:
                mac = ubinascii.hexlify(adv.mac)
                if mac == bytearray(GATT_CLIENT_MAC):
                    #name = bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
                    #print(mac, name, adv.rssi)
                    if not testCase == 'Not found':
                        rssi = adv.rssi
                        bluetooth.stop_scan()
                        break
        else:
            rssi = -10000
        bluetooth.deinit()
    except Exception as e:
        return -10000

    if testCase is not None and not testCase == 'Not found':
        rssi = testCase
    if rssi >= 0:
        return -10000

    return rssi
