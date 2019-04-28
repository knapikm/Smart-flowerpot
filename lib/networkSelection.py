from measurements import _battery
from topsis import closeness
from wifiAPI import wifi_connect, wifi_send, find_wifi
from bleAPI import gatt_connect, gatt_service, find_ble
from sigfoxAPI import sigfox_send
import sys
import logger
import pycom
from debugAPI import debug_led
from utime import sleep
from machine import idle


def _find_networks():
    return find_wifi(), find_ble()


def _battery_coef(w, b, testCase=None):
    battery_perc = _battery(testCase=testCase)
    if battery_perc == -10000:
        list = [-10000,-10000,-10000]
    else:
        list = [battery_perc - 100, battery_perc - 50, battery_perc - 30]
        for i in range(len(list)):
            if list[i] < 0:
                list[i] *= -1
                list[i] /= 2

        if w == -10000:
            list[0] = 10000
        if b == -10000:
            list[1] = 10000
    logger.BATTERY = list[:]

    return list


def _order_networks():
    wifi_rssi, ble_rssi = _find_networks()
    sigfox_rssi = -90
    logger.RSSI = [wifi_rssi, ble_rssi, sigfox_rssi]
    weights = [5,8,2,6]
    logger.WEIGHTS = weights[:]
    dec_matrix = [[wifi_rssi, ble_rssi, sigfox_rssi], # rssi
                  _battery_coef(wifi_rssi, ble_rssi), # battery coefficient
                  [16000000, 260000, 100], # max data rate
                  [111, 95.9, 47]] # current consumption
    result = closeness(dec_matrix, weights) # TOPSIS
    logger.RESULT = result[:]
    return result


def _connect_and_send(network):
    # TODO: pridat casovace
    if network == 0: # wifi
        pycom.rgbled(0x003300)
        if wifi_connect():
            if wifi_send() == 1:
                pycom.rgbled(0x000000)
                logger.W = True
                return True
            else:
                debug_led(0x330000, 0.3)
                logger.W = False
                return False
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
        if ret == 5:
            logger.S = True
            return True
        logger.S = False
        return False


def networks_loop():
    networks = _order_networks()
    #sys.exit()
    while len(networks):
        net = networks.index(max(networks))
        if _connect_and_send(net) is True:
            return
        else:
            networks[net] = -1
    else:
        pass # TODO: co ked ziadna siet nebola uspesna?
