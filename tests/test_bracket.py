import unittest

import numpy as np
import pandas as pd

from src.bracket import first_round_pairs, validate_field
from src.simulate import _play_round, run_simulations


class BracketTests(unittest.TestCase):
    def test_first_round_pairs_standard_region(self):
        df = pd.DataFrame({"slot": [1, 2, 3, 4]})
        self.assertEqual(first_round_pairs(df), [(1, 2), (3, 4)])

    def test_validate_rejects_non_power_of_two_region(self):
        df = pd.DataFrame({"region": ["East"] * 3, "slot": [1, 2, 3]})
        with self.assertRaises(ValueError):
            validate_field(df)

    def test_single_team_bye_advances(self):
        team = pd.Series({"team": "Bye Team", "adj_oe": 100, "adj_de": 95, "tempo": 65})
        winners = _play_round([team], np.random.default_rng(1))
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0]["team"], "Bye Team")

    def test_tie_ratings_do_not_always_pick_same_team(self):
        teams = pd.DataFrame([
            {"team": "A", "region": "East", "seed": 1, "slot": 1, "adj_oe": 110, "adj_de": 95, "tempo": 68},
            {"team": "B", "region": "East", "seed": 16, "slot": 2, "adj_oe": 110, "adj_de": 95, "tempo": 68},
        ])
        results = run_simulations(teams, n_sims=500, seed=42)
        p_a = float(results.loc[results["team"] == "A", "p_Champion"].iloc[0])
        self.assertGreater(p_a, 0.40)
        self.assertLess(p_a, 0.60)


if __name__ == "__main__":
    unittest.main()
