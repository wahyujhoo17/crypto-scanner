import unittest
from scripts.scanner import calculate_wilder_rsi

class TestCryptoScanner(unittest.TestCase):
    def test_wilder_rsi_uptrend(self):
        # 20 continuously rising prices
        closes = [float(i) for i in range(1, 25)]
        rsi = calculate_wilder_rsi(closes, period=14)
        self.assertEqual(rsi, 100.0)

    def test_wilder_rsi_downtrend(self):
        # 20 continuously falling prices
        closes = [float(100 - i) for i in range(1, 25)]
        rsi = calculate_wilder_rsi(closes, period=14)
        self.assertEqual(rsi, 0.0)

    def test_wilder_rsi_mixed(self):
        closes = [10, 12, 11, 13, 15, 14, 16, 18, 17, 19, 21, 20, 22, 24, 23, 25]
        rsi = calculate_wilder_rsi(closes, period=14)
        self.assertTrue(50 <= rsi <= 90)

if __name__ == '__main__':
    unittest.main()
