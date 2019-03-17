from network import Bluetooth, WLAN
from pysense import Pysense
import ubinascii
import pycom
from utime import sleep
import sys
from machine import idle
from measurements import _battery
import topsis
from wifiAPI import wifi_connect, wifi_send, find_wifi
from bleAPI import gatt_connect, gatt_service, find_ble
from sigfoxAPI import sigfox_send
import logger


py = Pysense()
pycom.heartbeat(False)

sys.exit()
def debug_led(rgb, time):
    pycom.rgbled(rgb)
    idle()
    sleep(time)
    pycom.rgbled(0)

def start_deep_sleep():
    pycom.rgbled(0x000000)
    idle()
    sleep(1)

    debug_led(0xbb0000, 1)
    idle()
    sleep(0.5)

    debug_led(0x880000, 0.7)
    idle()
    sleep(0.4)

    debug_led(0x440000, 0.4)
    idle()
    sleep(0.4)

    debug_led(0x110000, 0.3)

def deep_sleep():
    print('Start deep sleep...')
    py.setup_int_pin_wake_up(False)
    py.setup_int_wake_up(False, False)
    py.setup_sleep(3600)  # 1 hour

    start_deep_sleep()

    py.go_to_sleep()

def find_networks(testCase=None):
    ble = find_ble()
    wifi = find_wifi()

    # TODO:  podmienky


    return ble, wifi

def battery_level(w, b, testCase=None):
    battery_perc = _battery(testCase=testCase)
    if battery_perc == -10000:
        pass
    list = [battery_perc - 100, battery_perc - 50, battery_perc - 30]
    for i in range(len(list)):
        if list[i] < 0:
            list[i] *= -1
            list[i] /= 2
    print(list)
    logger.BATTERY = list
    print(logger.BATTERY)


    if w == -10000:
        list[0] = 10000
    if b == -10000:
        list[1] = 10000
    return list

def order_networks(testCase=None):
    ble, wifi = find_networks(testCase=testCase)
    logger.RSSI = [wifi, ble, -90]
    weights = [7,10,2,5]
    dec_matrix = [[wifi, ble, -90], # rssi
                  battery_level(wifi, ble, testCase=testCase), # battery
                  [150000000, 260000, 100], # max data rate
                  [111, 95.9, 47]] # Current consumption

    dec_matrix = topsis.standardize(dec_matrix)
    dec_matrix = topsis.multiply_weights(dec_matrix, weights)
    sol = topsis.solutions(dec_matrix)
    results = topsis.det_ideal_sol(sol)
    print(wifi, ble, -90)
    print(results)
    logger.RES = results
    return results

def connect_and_send(network):
    # TODO: pridat casovace
    if network == 0: # wifi
        pycom.rgbled(0x003300)
        wifi_connect()
        ret = wifi_send()
        if ret == 1:
            pycom.rgbled(0x000000)
            logger.W = True
            return True
        else:
            debug_led(0x330000, 0.3)
            logger.W = False
            return False

    if network == 1: # ble
        pycom.rgbled(0x030033) # blue
        pycom.nvs_set('ble', 0)
        gatt_connect()
        gatt_service()

        for _ in range(10):
            idle()
            sleep(3)
            ble = pycom.nvs_get('ble')
            if ble == 1:
                debug_led(0x003300, 0.3)
                logger.B = True
                return True
        else:
            debug_led(0x330000, 0.3)
            logger.B = False
            return False

    if network == 2: # Sigfox
        pycom.rgbled(0x090114)
        ret = sigfox_send()
        pycom.rgbled(0x000000)
        if ret == 8:
            logger.S = True
            return True
        logger.S = False
        return False

def networks_loop(networks):
    while len(networks):
        net = networks.index(max(networks))
        if connect_and_send(net):
            id = pycom.nvs_get('msg_id')
            pycom.nvs_set('msg_id', id + 1)
            break
        del networks[net]
    else:
        pass # TODO: co ked ziadna siet nebola uspesna?

networks_loop(order_networks())
logger.write_log()
deep_sleep()
