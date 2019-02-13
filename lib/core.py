from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from machine import Pin,ADC
import pycom

py = Pysense()
si = SI7006A20(pysense=py)
lt = LTR329ALS01(pysense=py)
mp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters

adc = ADC()
apin = adc.channel(pin='P15',attn=ADC.ATTN_11DB)
p_out = Pin('P9', mode = Pin.OUT, pull = Pin.PULL_DOWN)

def moist_sensor():
    p_out.value(1)
    volts = apin.value()
    p_out.value(0)
    return volts / 4.096

def measurements():
    global py, mp, si, lt, acc

    id = pycom.nvs_get('msg_id')
    temp = int(si.temperature()*0.8)
    #hum = int(si.humidity()*100)/100.0
    #press = mp.pressure()
    voltage = int(py.read_battery_voltage()*1000)/1000.0
    moist = int(moist_sensor())
    print(id, temp, voltage, moist)
    return id, temp, voltage, moist
