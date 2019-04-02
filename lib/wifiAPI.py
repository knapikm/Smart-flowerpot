from utime import sleep
from machine import idle
from mqtt import MQTTClient
from network import WLAN
import json
from measurements import measurements

client = None
wlan = None
WIFI_AP = {'name': 'RPiAP-DP', 'pass': 'raspberry-pi.DP18-19'}
#WIFI_AP = {'name': 'INFOTECH', 'pass': 'MU1nFotech28'}

def _prepare_payload_for_publish():
    id, temp, voltage, moist = measurements()
    return json.dumps( { "id": id, "temperature": temp, "battery": voltage, "moisture": moist, "network": 1 } )


def wifi_connect():
    global client, wlan

    wlan = WLAN(mode=WLAN.STA)
    wlan.disconnect()

    nets = wlan.scan()
    for net in nets:
        if net.ssid == WIFI_AP['name']:
            print('Wifi connecting...')
            wlan.connect(ssid=net.ssid, auth=(net.sec, WIFI_AP['pass']), timeout=5000)
            while not wlan.isconnected():
                idle()
                sleep(1)

            print('MQTT connecting...')
            client = MQTTClient(client_id="5bc8d724c03f971859b7747b", server="things.ubidots.com", user="A1E-rHXnsEnsjpZKKSlf8khOxgZwnXKkE3", password="A1E-rHXnsEnsjpZKKSlf8khOxgZwnXKkE3", port=1883)
            #client.set_callback(sub_cb)
            client.connect()
            #client.subscribe(topic="youraccount/.../...")
            return 1

    return None


def wifi_send():
    global client, wlan
    print('Wifi sending...')
    ret = client.publish(topic=b"/v1.6/devices/sipy", msg=_prepare_payload_for_publish(), qos=1)
    wlan.disconnect()
    return ret


def find_wifi(testCase=None):
    wlan = WLAN(mode=WLAN.STA)
    try:
        if isinstance(testCase, Exception):
            raise testCase
        wlan.disconnect()
        nets = wlan.scan()
        for net in nets:
            if net.ssid == WIFI_AP['name']:
                #print(net, net[4])
                if not testCase == 'Not found':
                    rssi = net[4]
                    break
        else:
            rssi = -10000
        wlan.deinit()
    except Exception as e:
        if isinstance(testCase, Exception):
            raise e
        return -10000

    if testCase is not None and not testCase == 'Not found':
        rssi = testCase
    if rssi > 0:
        return -10000

    return rssi
