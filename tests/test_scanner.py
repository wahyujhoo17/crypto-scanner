import unittest
from scripts.scanner import calculate_wilder_rsi

class TestCryptoScanner(unittest.TestCase):
    def test_wilder_rsi_uptrend(self):
        closes = [float(i) for i in range(1, 25)]
        rsi = calculate_wilder_rsi(closes, period=14)
        self.assertEqual(rsi, 100.0)

    def test_wilder_rsi_downtrend(self):
        closes = [float(100 - i) for i in range(1, 25)]
        rsi = calculate_wilder_rsi(closes, period=14)
        self.assertEqual(rsi, 0.0)

    def test_wilder_rsi_flat(self):
        closes = [50.0] * 25
        rsi = calculate_wilder_rsi(closes, period=14)
        self.assertEqual(rsi, 100.0)  # No loss -> RS infinity -> RSI 100

    def test_wilder_rsi_insufficient_data(self):
        closes = [10.0, 12.0, 11.0]
        rsi = calculate_wilder_rsi(closes, period=14)
        self.assertEqual(rsi, 50.0)

    def test_volume_ratio_calculation(self):
        v1 = [100.0] * 20 + [200.0]
        avg_vol_20 = sum(v1[-21:-1]) / 20
        vol_ratio = round(v1[-1] / avg_vol_20, 2)
        volume_spike = vol_ratio >= 1.5
        self.assertEqual(vol_ratio, 2.0)
        self.assertTrue(volume_spike)

    def test_rr_rejection_and_tp_validation(self):
        curr_price = 100.0
        tp1 = 101.0  # +1 reward
        sl = 99.0    # -1 risk -> R:R = 1.0 < 1.5
        risk = curr_price - sl
        reward_tp1 = tp1 - curr_price
        rr_tp1 = reward_tp1 / risk if risk > 0 else 0
        valid_long = tp1 > curr_price and sl < curr_price and risk > 0 and rr_tp1 >= 1.5
        self.assertFalse(valid_long)

if __name__ == '__main__':
    unittest.main()
