import unittest
import measurements
import wifiAPI
import bleAPI

class TemperatureTest(unittest.TestCase):
    def test_high_extreme(self):
        self.assertEqual(measurements._temp_sensor(86), -10000)

    def test_bottom_extreme(self):
        self.assertEqual(measurements._temp_sensor(-11), -10000)

    def test_exp(self):
        with self.assertRaises(Exception):
            measurements._temp_sensor(Exception())


class MoistureTest(unittest.TestCase):
    def test_negative_voltage(self):
        self.assertEqual(measurements._moist_sensor(-1), -10000)

    def test_exp(self):
        with self.assertRaises(Exception):
            measurements._moist_sensor(Exception())


class BatteryTest(unittest.TestCase):
    def test_negative_voltage(self):
        self.assertEqual(measurements._battery(-1), -10000)

    def test_exp(self):
        with self.assertRaises(Exception):
            measurements._battery(Exception())


class WiFiTest(unittest.TestCase):
    def test_positive_rssi(self):
        self.assertEqual(wifiAPI.find_wifi(1), -10000)

    def test_not_found(self):
        self.assertEqual(wifiAPI.find_wifi('Not found'), -10000)

    def test_exp(self):
        with self.assertRaises(Exception):
            wifiAPI.find_wifi(Exception())


class BleTest(unittest.TestCase):
    def test_positive_rssi(self):
        self.assertEqual(wifiAPI.find_wifi(1), -10000)

    def test_not_found(self):
        self.assertEqual(wifiAPI.find_wifi('Not found'), -10000)

    def test_exp(self):
        with self.assertRaises(Exception):
            wifiAPI.find_wifi(Exception())


if __name__=='__main__':
    unittest.main()
