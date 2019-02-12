from network import Bluetooth
from network import WLAN
from pysense import Pysense
from topsis import standardize, multiply_weights, solutions, det_ideal_sol
from wifiAPI import wifi_connect, wifi_send
from bleAPI import gatt_connect, gatt_service
from sigfoxAPI import sigfox_send
import ubinascii
import pycom

py = Pysense()
pycom.heartbeat(False)

def networks_finder():
    ble = -1000
    wifi = -1000
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

    return ble, wifi

def battery_level():
    battery = py.read_battery_voltage()
    if battery > 4.6:
        perc = 100
    else:
        battery -= 3.311792
        perc = battery / 0.8
    list = [perc - 100, perc - 50, perc - 30]
    for i in range(len(list)):
        if list[i] < 0:
            list[i] *= -1
            list[i] /= 2
    return list

def find_best_net():
    ble, wifi = networks_finder()

    weights = [7,8,2,6]
    dec_matrix = [[wifi, ble, -90], # rssi
                  battery_level(), # battery
                  [150000000, 260000, 100], # max data rate
                  [111, 95.9, 47]] # Current consumption

    dec_matrix = standardize(dec_matrix)
    dec_matrix = multiply_weights(dec_matrix, weights)
    sol = solutions(dec_matrix)
    results = det_ideal_sol(sol)
    print(results)
    return results
    # TODO: pripojenie k naj siete
    # TODO: odmeranie a odoslanie velicin

def connect_and_send(networks):
    net = networks.index(max(networks))
    net = 1
    if net == 0: # wifi
        wifi_connect()
        ret = wifi_send()
        if ret == 1:
            id = pycom.nvs_get('msg_id')
            pycom.nvs_set('msg_id', id + 1)

    if net == 1: # ble
        gatt_connect()
        gatt_service()

    if net == 2:
        ret = sigfox_send()
        if ret == 8:
            id = pycom.nvs_get('msg_id')
            pycom.nvs_set('msg_id', id + 1)

connect_and_send(find_best_net())
