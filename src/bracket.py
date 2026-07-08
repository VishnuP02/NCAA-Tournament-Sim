"""Bracket representation and advancement helpers for a 64-team NCAA field."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

ROUND_ORDER = ["R64", "R32", "S16", "E8", "F4", "Final", "Champion"]
REGION_ORDER = ["East", "West", "South", "Midwest"]


@dataclass(frozen=True)
class Team:
    team: str
    region: str
    seed: int
    slot: int
    adj_oe: float
    adj_de: float
    tempo: float
    public_pick_pct: float = 0.0
    actual_round: str = "R64"

    @property
    def net_rating(self) -> float:
        return self.adj_oe - self.adj_de


def load_teams(path: str) -> pd.DataFrame:
    teams = pd.read_csv(path)
    required = {"team", "region", "seed", "slot", "adj_oe", "adj_de", "tempo"}
    missing = required - set(teams.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if teams["slot"].duplicated().any():
        dupes = teams.loc[teams["slot"].duplicated(), "slot"].tolist()
        raise ValueError(f"Duplicate bracket slots found: {dupes}")
    return teams.sort_values("slot").reset_index(drop=True)


def first_round_pairs(region_df: pd.DataFrame) -> list[tuple[int, int]]:
    """Return slot pairs in standard NCAA bracket order for a single region."""
    slots = region_df.sort_values("slot")["slot"].tolist()
    if len(slots) == 1:
        return []
    if len(slots) % 2:
        raise ValueError("A region must contain an even number of teams unless it is a single bye team.")
    return [(slots[i], slots[i + 1]) for i in range(0, len(slots), 2)]


def validate_field(teams: pd.DataFrame) -> None:
    if teams.empty:
        raise ValueError("Field cannot be empty.")
    for region, region_df in teams.groupby("region"):
        n = len(region_df)
        if n not in {1, 2, 4, 8, 16}:
            raise ValueError(f"Region {region} has {n} teams; expected a power-of-two region size.")
