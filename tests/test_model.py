import unittest

from src.model import win_probability


class WinProbabilityTests(unittest.TestCase):
    def test_equal_ratings_are_coin_flip(self):
        a = {"adj_oe": 110, "adj_de": 95, "tempo": 68}
        b = {"adj_oe": 110, "adj_de": 95, "tempo": 68}
        self.assertAlmostEqual(win_probability(a, b), 0.5)

    def test_better_team_has_higher_probability(self):
        a = {"adj_oe": 120, "adj_de": 90, "tempo": 68}
        b = {"adj_oe": 105, "adj_de": 100, "tempo": 68}
        self.assertGreater(win_probability(a, b), 0.5)
        self.assertLess(win_probability(b, a), 0.5)


if __name__ == "__main__":
    unittest.main()
