from network import Bluetooth, WLAN
from pysense import Pysense
import ubinascii
import pycom
import utime
import sys
from machine import idle

import topsis
from wifiAPI import wifi_connect, wifi_send
from bleAPI import gatt_connect, gatt_service
from sigfoxAPI import sigfox_send
import logger

py = Pysense()
pycom.heartbeat(False)

def debug_led(rgb, time):
    pycom.rgbled(rgb)
    idle()
    utime.sleep(time)
    pycom.rgbled(0)

def start_deep_sleep():
    pycom.rgbled(0x000000)
    idle()
    utime.sleep(1)

    debug_led(0xbb0000, 1)
    idle()
    utime.sleep(0.5)

    debug_led(0x880000, 0.7)
    idle()
    utime.sleep(0.4)

    debug_led(0x440000, 0.4)
    idle()
    utime.sleep(0.4)

    debug_led(0x110000, 0.3)

def deep_sleep():
    print('Start deep sleep...')
    py.setup_int_pin_wake_up(False)
    py.setup_int_wake_up(False, False)
    py.setup_sleep(3600)  # 1 hour

    start_deep_sleep()

    py.go_to_sleep()

def networks_finder():
    ble = -10000
    wifi = -10000
    # TODO: pridat casovace

    wlan = WLAN(mode=WLAN.STA)
    wlan.disconnect()
    nets = wlan.scan()
    for net in nets:
        #if net.ssid == 'eduroam':
        if net.ssid == 'RPiAP-DP':
            #print(net, net[4])
            wifi = net[4]
            break
    wlan.deinit()

    bluetooth = Bluetooth()
    bluetooth.start_scan(5)
    while bluetooth.isscanning():
        adv = bluetooth.get_adv()
        if adv:
            mac = ubinascii.hexlify(adv.mac)
            if mac == bytearray('b827ebeec52e'):
                #name = bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
                #print(mac, name, adv.rssi)
                ble = adv.rssi
                bluetooth.stop_scan()
                break
    bluetooth.deinit()
    return ble, wifi

def battery_level(w, b):
    battery = py.read_battery_voltage()
    logger.VOLTAGE = battery
    if battery > 4.6:
        perc = 100
    else:
        # % = (voltage - min) / (max - min)
        battery -= 3.311792
        perc = battery / 0.8 * 100
    list = [perc - 100, perc - 50, perc - 30]
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

def order_networks():
    ble, wifi = networks_finder()
    logger.RSSI = [wifi, ble, -90]
    weights = [7,10,2,5]
    dec_matrix = [[wifi, ble, -90], # rssi
                  battery_level(wifi, ble), # battery
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
            utime.sleep(3)
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
            return
        del networks[net]

networks_loop(order_networks())
logger.write_log()
deep_sleep()
