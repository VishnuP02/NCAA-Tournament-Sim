"""Validation and comparison helpers."""
from __future__ import annotations

import pandas as pd

ROUND_POINTS = {"R64": 0, "R32": 1, "S16": 2, "E8": 3, "F4": 4, "Final": 5, "Champion": 6}


def add_validation_columns(results: pd.DataFrame) -> pd.DataFrame:
    df = results.copy()
    df["actual_points"] = df["actual_round"].map(ROUND_POINTS).fillna(0).astype(int)
    df["expected_points"] = (
        df["p_R32"] + df["p_S16"] + df["p_E8"] + df["p_F4"] + df["p_Final"] + df["p_Champion"]
    )
    df["seed_committee_gap"] = df["net_rating"].rank(ascending=False, method="min") - df["seed"].rank(method="first")
    df["model_public_title_gap"] = df["p_Champion"] * 100 - df["public_pick_pct"]
    return df


def summarize_validation(df: pd.DataFrame) -> dict[str, float]:
    top_title = df.sort_values("p_Champion", ascending=False).iloc[0]
    champion = df[df["actual_round"] == "Champion"].iloc[0]
    return {
        "top_model_title_favorite": top_title["team"],
        "top_model_title_probability": round(float(top_title["p_Champion"]), 4),
        "actual_champion": champion["team"],
        "actual_champion_model_probability": round(float(champion["p_Champion"]), 4),
        "spearman_expected_vs_actual": round(float(df["expected_points"].corr(df["actual_points"], method="spearman")), 4),
    }
