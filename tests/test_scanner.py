import unittest
from scripts.scanner import calculate_wilder_rsi, calculate_risk_reward, is_valid_long

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
        self.assertEqual(calculate_wilder_rsi(closes), 50.0)

    def test_wilder_rsi_insufficient_data(self):
        closes = [10.0, 12.0, 11.0]
        rsi = calculate_wilder_rsi(closes, period=14)
        self.assertEqual(rsi, 50.0)

    def test_calculate_risk_reward(self):
        # Entry 100, TP 110, SL 95 -> Risk 5, Reward 10 -> R:R = 2.0
        rr = calculate_risk_reward(entry=100.0, target=110.0, stop=95.0)
        self.assertEqual(rr, 2.0)

    def test_calculate_risk_reward_invalid_stop(self):
        # Stop above entry -> Risk <= 0 -> R:R = 0.0
        rr = calculate_risk_reward(entry=100.0, target=110.0, stop=105.0)
        self.assertEqual(rr, 0.0)

    def test_is_valid_long_accepts_good_setup(self):
        valid = is_valid_long(
            entry=100.0,
            tp1=110.0,
            sl=95.0,
            rr=2.0,
            trend_4h=True,
            rsi_1h=55.0,
            trend_1h=True
        )
        self.assertTrue(valid)

    def test_is_valid_long_rejects_low_rr(self):
        valid = is_valid_long(
            entry=100.0,
            tp1=101.0,
            sl=99.0,
            rr=1.0,  # Below 1.5 threshold
            trend_4h=True,
            rsi_1h=55.0,
            trend_1h=True
        )
        self.assertFalse(valid)

    def test_is_valid_long_rejects_bearish_4h(self):
        valid = is_valid_long(
            entry=100.0,
            tp1=110.0,
            sl=95.0,
            rr=2.0,
            trend_4h=False,  # Bearish 4H trend
            rsi_1h=55.0,
            trend_1h=True
        )
        self.assertFalse(valid)

if __name__ == '__main__':
    unittest.main()
