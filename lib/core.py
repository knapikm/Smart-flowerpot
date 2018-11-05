from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from machine import Pin,ADC

py = Pysense()
mp = MPL3115A2(pysense=py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
si = SI7006A20(pysense=py)
lt = LTR329ALS01(pysense=py)
#acc = LIS2HH12(pysense=py)

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
    #moist = int(moist_sensor())

    return (temp_mp, temp_si), hum, light, press, voltage
