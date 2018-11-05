from network import Bluetooth
import ubinascii
import pycom
from machine import Pin,ADC

pycom.heartbeat(False)

adc = ADC()
apin = adc.channel(pin='P15',attn=ADC.ATTN_11DB)
p_out = Pin('P9', mode = Pin.OUT, pull = Pin.PULL_DOWN)

def moist_sensor():
    p_out.value(1)
    volts = apin.value()
    p_out.value(0)
    return volts / 4.096

volts = int(moist_sensor())
print(volts)

'''
bluetooth = Bluetooth()
bluetooth.start_scan(20)
while bluetooth.isscanning():
    adv = bluetooth.get_adv()
    if adv:
        mac = ubinascii.hexlify(adv.mac)
        if mac == bytearray('b827ebeec52e'):
            name = bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
            print(mac, name, adv.rssi)
'''
