from utime import sleep
from machine import idle
import pycom
import json
from mqtt import MQTTClient, MQTTException
from network import WLAN

W = None
MQTT = None
B = None
GATT = None
S = None
RSSI = []
BATTERY = []
VOLTAGE = 0
RES = []

def mqtt_log(payload):
    #_AP = {'name': 'INFOTECH', 'pass': 'MU1nFotech28'}
    _AP = {'name': 'RPiAP-DP', 'pass': 'raspberry-pi.DP18-19'}

    wlan = WLAN(mode=WLAN.STA)
    wlan.disconnect()

    nets = wlan.scan()
    for net in nets:
        if net.ssid == _AP['name']:
            print('Wifi connecting...')
            wlan.connect(ssid=net.ssid, auth=(net.sec, _AP['pass']), timeout=60)
            while not wlan.isconnected():
                idle()
                sleep(1)
            break
    else:
        return False

    try:
        print('MQTT connecting...')
        client = MQTTClient("Sipy", server="192.168.56.1", port=1883)
        #client.set_callback(sub_cb)
        if client.connect() == -1:
            return False
        print('MQTT publish')
        #client.subscribe(topic="youraccount/.../...")
        client.publish(topic="sipy/log", msg=payload)
    except MQTTException as e:
        return False


def write_log(mqtt=False):
    id = pycom.nvs_get('msg_id') - 1
    log = json.dumps({
        "log": id,
        "topsis": {
            "rssi": RSSI,
            "battery": BATTERY,
            "voltage": VOLTAGE,
            "result": RES
        },
        "wifi": W,
        "ble": B,
        "sigfox": S
    })
    if mqtt:
        mqtt_log(log)
    f = open('/sd/log.txt', 'a') #create file (append mode)
    f.write(log + '\n')
    f.close()

'''
mqtt_log(''{"id": 1, "topsis": {"rssi": [1,2,3], "battery": 100, "voltage": 4.2, "result": [1,2,3]}, "wifi": True, "ble": None, "sigfox": None,}')
'''
