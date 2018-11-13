import pycom
import time
import machine
from mqtt import MQTTClient

def prepare_payload_for_publish():
    temp, hum, light, press, voltage = measurements()
    payload = {"temperature": {"mp": temp[0], "si": temp[1]},
               "humidity": hum,
               "light": {"red": light[0], "blue": light[1]},
               "pressure": press,
               "battery": voltage
              }
    payload = json.dumps(payload)
    return payload

pycom.heartbeat(False)
pycom.rgbled(0x001000)

from network import WLAN
wlan = WLAN(mode=WLAN.STA)
wlan.disconnect()

nets = wlan.scan()

for net in nets:
    #if net.ssid == 'eduroam':
    if net.ssid == 'RPiAP-DP':
        print('Network found!')
        print(net, net[4])
        #wlan.connect(ssid='eduroam', auth=(WLAN.WPA2_ENT, 'xknapik@stuba.sk', 'ota92Lis'), identity='xknapik@stuba.sk') #, ca_certs='/flash/cert/TrustedRoot.pem')
        wlan.connect(ssid=net.ssid, auth=(net.sec, 'raspberry-pi.DP18-19'), timeout=5000)
        while not wlan.isconnected():
            time.sleep(1)
        print('WLAN connection succeeded!')
        break

nets = wlan.scan()

for net in nets:
    #if net.ssid == 'eduroam':
    if net.ssid == 'RPiAP-DP':
        print(net, net[4])

client = MQTTClient(client_id="5bc8d724c03f971859b7747b", server="things.ubidots.com", user="A1E-rHXnsEnsjpZKKSlf8khOxgZwnXKkE3", password="A1E-rHXnsEnsjpZKKSlf8khOxgZwnXKkE3", port=1883)
#client.set_callback(sub_cb)
client.connect()
#client.subscribe(topic="youraccount/feeds/lights")

#client.publish(topic=b"/v1.6/devices/sipy", msg='{"test": 3}')
pycom.rgbled(0x000000)

#while wlan.isconnected():
time.sleep(5)
    #print(wlan.ifconfig())
#print('WLAN connection end...!')

wlan.disconnect()