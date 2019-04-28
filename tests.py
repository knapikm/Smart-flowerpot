import unittest
import measurements
import wifiAPI
import bleAPI

class TemperatureTest(unittest.TestCase):
    def test_high_extreme(self):
        self.assertEqual(measurements._temp_sensor(86), 143)

    def test_bottom_extreme(self):
        self.assertEqual(measurements._temp_sensor(-11), 143)

    def test_exp(self):
        self.assertEqual(measurements._temp_sensor(Exception()), 143)


class MoistureTest(unittest.TestCase):
    def test_negative_voltage(self):
        self.assertEqual(measurements._moist_sensor(-1), 143)

    def test_exp(self):
        self.assertEqual(measurements._moist_sensor(Exception()), 143)


class BatteryTest(unittest.TestCase):
    def test_negative_voltage(self):
        self.assertEqual(measurements._battery(-1), 143)

    def test_exp(self):
        self.assertEqual(measurements._battery(Exception()), 143)


class WiFiTest(unittest.TestCase):
    def test_positive_rssi(self):
        self.assertEqual(wifiAPI.find_wifi(1), -10000)

    def test_not_found(self):
        self.assertEqual(wifiAPI.find_wifi('Not found'), -10000)

    def test_exp(self):
        self.assertEqual(wifiAPI.find_wifi(Exception()), -10000)


class BleTest(unittest.TestCase):
    def test_positive_rssi(self):
        self.assertEqual(bleAPI.find_ble(1), -10000)

    def test_not_found(self):
        self.assertEqual(bleAPI.find_ble('Not found'), -10000)

    def test_exp(self):
        self.assertEqual(bleAPI.find_ble(Exception()), -10000)


if __name__=='__main__':
    unittest.main()
