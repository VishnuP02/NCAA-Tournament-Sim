"""Matplotlib visualizations for simulation output."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_probability_bar(results: pd.DataFrame, probability_col: str, title: str, output_path: str, top_n: int = 12) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    plot_df = results.sort_values(probability_col, ascending=False).head(top_n).iloc[::-1]
    plt.figure(figsize=(9, 6))
    plt.barh(plot_df["team"], plot_df[probability_col] * 100)
    plt.xlabel("Probability (%)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output, dpi=160)
    plt.close()
