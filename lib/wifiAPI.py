import time
import machine
from mqtt import MQTTClient
from network import WLAN
import json
from core import measurements

client = None
wlan = None

def prepare_payload_for_publish():
    id, temp, voltage, moist = measurements()
    return json.dumps( { "id": id, "temperature": temp, "battery": voltage, "moisture": moist, "network": 1 } )


def wifi_connect():
    global client, wlan

    wlan = WLAN(mode=WLAN.STA)
    wlan.disconnect()

    nets = wlan.scan()
    for net in nets:
        if net.ssid == 'INFOTECH':
        #if net.ssid == 'RPiAP-DP':
            print('Wifi connecting...')
            wlan.connect(ssid=net.ssid, auth=(net.sec, 'MU1nFotech28'), timeout=5000)
            #wlan.connect(ssid=net.ssid, auth=(net.sec, 'raspberry-pi.DP18-19'), timeout=5000)
            while not wlan.isconnected():
                machine.idle()
                time.sleep(1)

            print('MQTT connecting...')
            client = MQTTClient(client_id="5bc8d724c03f971859b7747b", server="things.ubidots.com", user="A1E-rHXnsEnsjpZKKSlf8khOxgZwnXKkE3", password="A1E-rHXnsEnsjpZKKSlf8khOxgZwnXKkE3", port=1883)
            #client.set_callback(sub_cb)
            client.connect()
            #client.subscribe(topic="youraccount/.../...")

            return 1

    return None


def wifi_send():
    print('Wifi sending...')
    ret = client.publish(topic=b"/v1.6/devices/sipy", msg=prepare_payload_for_publish(), qos=1)
    wlan.disconnect()
    return ret
