import pycom
from utime import sleep
from machine import idle

def debug_led(rgb, time):
    pycom.rgbled(rgb)
    idle()
    sleep(time)
    pycom.rgbled(0)

def _idle(time):
    idle()
    sleep(time)

def deep_sleep_led():
    pycom.rgbled(0x000000)
    _idle(1)

    debug_led(0xbb0000, 1)
    _idle(0.6)

    debug_led(0x880000, 0.7)
    _idle(0.5)

    debug_led(0x440000, 0.4)
    _idle(0.4)

    debug_led(0x110000, 0.3)
