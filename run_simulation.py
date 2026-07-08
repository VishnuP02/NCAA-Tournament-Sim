from __future__ import annotations

import argparse
from pathlib import Path

from src.bracket import load_teams
from src.simulate import run_simulations
from src.validate import add_validation_columns, summarize_validation
from src.visualize import save_probability_bar


def main() -> None:
    parser = argparse.ArgumentParser(description="Run NCAA tournament Monte Carlo simulations.")
    parser.add_argument("--teams", default="data/teams_2024_synthetic.csv")
    parser.add_argument("--sims", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--outdir", default="outputs")
    args = parser.parse_args()

    teams = load_teams(args.teams)
    results = run_simulations(teams, n_sims=args.sims, seed=args.seed)
    results = add_validation_columns(results)

    outdir = Path(args.outdir)
    outdir.mkdir(exist_ok=True)
    csv_path = outdir / "simulation_results.csv"
    results.sort_values("p_Champion", ascending=False).to_csv(csv_path, index=False)
    save_probability_bar(results, "p_Champion", "2024 NCAA Men's Tournament: Simulated Title Odds", outdir / "title_odds.png")
    save_probability_bar(results, "p_F4", "2024 NCAA Men's Tournament: Simulated Final Four Odds", outdir / "final_four_odds.png")

    summary = summarize_validation(results)
    print("Simulation complete")
    print(f"Teams: {len(teams)} | Simulations: {args.sims} | Seed: {args.seed}")
    print(f"Wrote: {csv_path}")
    print("Validation summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print("\nTop 10 title odds:")
    cols = ["team", "region", "seed", "net_rating", "p_Champion", "public_pick_pct", "actual_round"]
    print(results.sort_values("p_Champion", ascending=False)[cols].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
