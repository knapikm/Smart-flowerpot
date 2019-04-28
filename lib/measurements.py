from pysense import Pysense
from SI7006A20 import SI7006A20
from machine import Pin,ADC
import pycom
import logger


def _moist_sensor(testCase=None):
    voltage_ref = 4.096
    adc = ADC()
    apin = adc.channel(pin='P15',attn=ADC.ATTN_11DB)
    p_out = Pin('P9', mode = Pin.OUT, pull = Pin.PULL_DOWN)

    try:
        if isinstance(testCase, Exception):
            raise testCase
        p_out.value(1)
        volts = apin.value() / voltage_ref
        p_out.value(0)
    except Exception as e:
        return 143

    if testCase is not None:
        volts = testCase
    if volts < 0:
        return 143

    if volts >= 760:
        return 100
    else:
        perc = int((volts / 760.0) * 100)
    return perc

def _temp_sensor(testCase=None):
    min_temp = -10
    max_temp = 85
    py = Pysense()
    si = SI7006A20(pysense=py)
    try:
        if isinstance(testCase, Exception):
            raise testCase
        temp = int(si.temperature()) # from –10 to 85 degree celsius
    except Exception as e:
        return 143

    if testCase is not None:
        temp = testCase
    if temp < min_temp or temp > max_temp:
        return 143
    return temp

def _battery(testCase=None):
    py = Pysense()

    try:
        if isinstance(testCase, Exception):
            raise testCase
        voltage = int(py.read_battery_voltage()*1000)/1000.0
        logger.VOLTAGE = voltage
    except Exception as e:
        return 143

    if testCase is not None:
        voltage = testCase
    if voltage < 0:
        return 143

    if voltage > 4.4:
        perc = 100
    else:
        # % = (voltage - min) / (max - min)
        voltage -= 3.311
        perc = int((voltage / 0.8) * 100)
        if perc > 100:
            perc = 100
    return perc

def measurements():
    msg_id = pycom.nvs_get('msg_id')
    temp = _temp_sensor()
    perc = _battery()
    moist = _moist_sensor()

    print('Measurements:', msg_id, temp, perc, moist)
    return msg_id, temp, perc, moist
