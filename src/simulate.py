"""Monte Carlo tournament simulation engine."""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable

import numpy as np
import pandas as pd

from .bracket import REGION_ORDER, ROUND_ORDER, validate_field
from .model import win_probability

ADVANCEMENT_ROUNDS = ["R32", "S16", "E8", "F4", "Final", "Champion"]


def _pick_winner(team_a: pd.Series, team_b: pd.Series, rng: np.random.Generator) -> pd.Series:
    p_a = win_probability(team_a, team_b)
    if p_a == 0.5:
        # Explicit tie handling keeps equal-rating matchups unbiased and testable.
        return team_a if rng.random() < 0.5 else team_b
    return team_a if rng.random() < p_a else team_b


def _play_round(teams: list[pd.Series], rng: np.random.Generator) -> list[pd.Series]:
    if len(teams) == 1:
        return teams
    if len(teams) % 2:
        # Single-team bye support for future/custom brackets.
        teams = teams + [None]
    winners: list[pd.Series] = []
    for i in range(0, len(teams), 2):
        a, b = teams[i], teams[i + 1]
        if b is None:
            winners.append(a)
        else:
            winners.append(_pick_winner(a, b, rng))
    return winners


def simulate_once(teams: pd.DataFrame, rng: np.random.Generator) -> dict[str, list[str]]:
    validate_field(teams)
    reached: dict[str, list[str]] = defaultdict(list)
    region_champions: list[pd.Series] = []

    for region in REGION_ORDER:
        region_df = teams[teams["region"] == region].sort_values("slot")
        if region_df.empty:
            continue
        alive = [row for _, row in region_df.iterrows()]
        for round_name in ["R32", "S16", "E8", "F4"]:
            alive = _play_round(alive, rng)
            for winner in alive:
                reached[round_name].append(winner["team"])
        region_champions.extend(alive)

    finalists = _play_round(region_champions, rng)
    for winner in finalists:
        reached["Final"].append(winner["team"])
    champion = _play_round(finalists, rng)[0]
    reached["Champion"].append(champion["team"])
    return reached


def run_simulations(teams: pd.DataFrame, n_sims: int = 10000, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    counts = {round_name: Counter() for round_name in ADVANCEMENT_ROUNDS}

    for _ in range(n_sims):
        reached = simulate_once(teams, rng)
        for round_name, names in reached.items():
            counts[round_name].update(names)

    rows = []
    for _, team in teams.sort_values("slot").iterrows():
        row = {
            "team": team["team"],
            "region": team["region"],
            "seed": int(team["seed"]),
            "net_rating": round(float(team["adj_oe"] - team["adj_de"]), 2),
            "public_pick_pct": float(team.get("public_pick_pct", 0.0)),
            "actual_round": team.get("actual_round", "R64"),
        }
        for round_name in ADVANCEMENT_ROUNDS:
            row[f"p_{round_name}"] = counts[round_name][team["team"]] / n_sims
        rows.append(row)
    return pd.DataFrame(rows)
