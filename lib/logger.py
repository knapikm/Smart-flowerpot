import pycom
import json

W = None
B = None
S = None
RSSI = []
BATTERY = []
VOLTAGE = 0
RES = []

def write_log():
    id = pycom.nvs_get('msg_id') - 1
    log = json.dumps({
        "log": id,
        "topsis": {
            "rssi": RSSI,
            "battery": BATTERY,
            "voltage": VOLTAGE,
            "result": RES
        },
        "wifi": W,
        "ble": B,
        "sigfox": S
    })
    f = open('/sd/log.txt', 'a') #create file (append mode)
    f.write(log + '\n')
    f.close()

'''
{"id": 1, "topsis": {"rssi": [1,2,3], "battery": 100, "voltage": 4.2, "result": [1,2,3]}, "wifi": True, "ble": None, "sigfox": None,}
'''
