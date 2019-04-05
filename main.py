from pysense import Pysense
from networkSelection import networks_loop
import pycom
from utime import sleep
from machine import idle
from logger import write_log

py = Pysense()
pycom.heartbeat(False)

def debug_led(rgb, time):
    pycom.rgbled(rgb)
    idle()
    sleep(time)
    pycom.rgbled(0)

def _idle(time):
    idle()
    sleep(time)

def _deep_sleep_led():
    pycom.rgbled(0x000000)
    _idle(1)

    debug_led(0xbb0000, 1)
    _idle(0.6)

    debug_led(0x880000, 0.7)
    _idle(0.5)

    debug_led(0x440000, 0.4)
    _idle(0.4)

    debug_led(0x110000, 0.3)

def deep_sleep():
    print('Start deep sleep...')
    py.setup_int_pin_wake_up(False)
    py.setup_int_wake_up(False, False)
    py.setup_sleep(3600)  # 1 hour

    _deep_sleep_led()
    py.go_to_sleep()


networks_loop()
write_log(mqtt=True)
deep_sleep()
