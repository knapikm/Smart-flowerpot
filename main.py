from pysense import Pysense
from networkSelection import networks_loop
import pycom
from logger import write_log
from debugAPI import deep_sleep_led
import sys
from measurements import measurements

py = Pysense()
pycom.heartbeat(False)

def deep_sleep():
    id = pycom.nvs_get('msg_id')
    pycom.nvs_set('msg_id', id + 1)
    print('Start deep sleep...')
    py.setup_int_pin_wake_up(True)
    py.setup_int_wake_up(False, True)
    #py.setup_sleep(3600)  # 1 hour
    py.setup_sleep(600)  # 10 min

    deep_sleep_led()
    py.go_to_sleep()

measurements()
networks_loop()
write_log(mqtt=True)
deep_sleep()
