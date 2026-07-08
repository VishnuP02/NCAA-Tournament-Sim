"""Probability model used by the simulator."""
from __future__ import annotations

import math
from typing import Mapping


def win_probability(team_a: Mapping, team_b: Mapping, spread_scale: float = 11.0) -> float:
    """Estimate P(team_a beats team_b) from adjusted efficiency ratings.

    Ratings are points per 100 possessions. We approximate expected game margin by
    converting net-rating difference to a typical game possession count, then pass
    the result through a logistic function. The scale parameter controls upset rate.
    """
    net_a = float(team_a["adj_oe"]) - float(team_a["adj_de"])
    net_b = float(team_b["adj_oe"]) - float(team_b["adj_de"])
    possessions = (float(team_a["tempo"]) + float(team_b["tempo"])) / 2.0
    expected_margin = (net_a - net_b) * possessions / 100.0
    return 1.0 / (1.0 + math.exp(-expected_margin / spread_scale))
