# NCAA Men's Tournament Monte Carlo Simulator

A portfolio-ready Python project that simulates the 2024 NCAA men's basketball tournament bracket thousands of times using pace-adjusted offensive and defensive efficiency ratings.

The goal is not to predict the future perfectly. The goal is to show how to design a reproducible simulation engine, convert team-strength ratings into game win probabilities, aggregate tournament outcomes, and validate the model against a real completed tournament.

## Why this project matters

This project is aimed at sports analytics, sports media, and data-focused interview conversations. It demonstrates:

- Monte Carlo simulation design
- Probabilistic game modeling
- Bracket advancement logic
- Validation against historical results
- Clean Python package structure
- Unit-tested core logic
- Reproducible CSV and chart outputs

## Data source

The included dataset is `data/teams_2024_synthetic.csv`.

It is a **synthetic fallback dataset** for the 2024 NCAA men's tournament field. It uses Torvik-style columns:

- `adj_oe`: adjusted offensive efficiency, points per 100 possessions
- `adj_de`: adjusted defensive efficiency, points allowed per 100 possessions
- `tempo`: estimated possessions per game
- `public_pick_pct`: synthetic bracket-pool title pick percentage used for model-vs-public comparison
- `actual_round`: actual 2024 tournament finish for validation

I intentionally did **not** scrape KenPom. KenPom is a paid/subscription analytics product, and scraping it would be inappropriate for a public GitHub portfolio.

Bart Torvik's T-Rank publishes public college basketball efficiency data and has public CSV/JSON endpoints, but this repo avoids live scraping by default. The project is structured so an allowed ratings export can replace the synthetic CSV as long as it keeps the same column schema.

## Modeling approach

For each game, the simulator computes each team's net rating:

```text
net_rating = adjusted_offensive_efficiency - adjusted_defensive_efficiency
```

Then it estimates expected game margin by converting the net-rating difference to an average game possession environment:

```text
expected_margin = (team_a_net - team_b_net) * average_tempo / 100
```

That margin is converted to a win probability with a logistic function:

```text
P(team_a wins) = 1 / (1 + exp(-expected_margin / spread_scale))
```

The simulator then plays the bracket round by round many times and records how often each team reaches:

- Round of 32
- Sweet 16
- Elite 8
- Final Four
- Championship game
- Champion

## Project structure

```text
.
├── data/
│   ├── README.md
│   └── teams_2024_synthetic.csv
├── notebooks/
│   └── demo.ipynb
├── outputs/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── bracket.py
│   ├── model.py
│   ├── simulate.py
│   ├── validate.py
│   └── visualize.py
├── tests/
│   ├── test_bracket.py
│   └── test_model.py
├── run_simulation.py
├── requirements.txt
└── README.md
```

## How to run

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the simulation:

```bash
python run_simulation.py --sims 10000 --seed 7
```

Run tests:

```bash
python -m unittest discover tests
```

## Example output

A typical run writes:

```text
outputs/simulation_results.csv
outputs/title_odds.png
outputs/final_four_odds.png
```

Example terminal output from a 10,000-simulation run:

```text
Simulation complete
Teams: 64 | Simulations: 10000 | Seed: 7
Wrote: outputs/simulation_results.csv
Validation summary:
  top_model_title_favorite: UConn
  top_model_title_probability: 0.1266
  actual_champion: UConn
  actual_champion_model_probability: 0.1266
  spearman_expected_vs_actual: 0.5654
```

## Model vs committee/public comparison

The output CSV includes comparison fields:

- `seed_committee_gap`: rough difference between model rating rank and seed rank
- `model_public_title_gap`: model title probability minus synthetic public title pick percentage

These fields highlight teams the model likes more or less than their seed/public popularity.

## Validation

The validation uses the actual 2024 tournament result labels in the dataset.

For each team, the project compares:

- simulated expected tournament advancement
- actual tournament finish
- whether the actual champion had a meaningful pre-tournament title probability

This is intentionally lightweight validation. A more advanced project could backtest many seasons, compare calibration buckets, and tune the spread scale using historical game outcomes.

## Known limitations

This model is intentionally honest about what it cannot capture:

- It does not know about injuries, suspensions, or late-season roster changes.
- It does not model matchup-specific style interactions beyond efficiency and tempo.
- It does not account for travel distance, crowd effects, or rest differences.
- It treats team strength as fixed at tournament start.
- It does not model in-game foul trouble, three-point variance, or coaching adjustments.
- The included ratings are synthetic fallback numbers, not official Torvik/KenPom data.
- A single-elimination tournament has extreme variance; a good model can still miss many individual games.

## Interview talking points

A good way to explain the project:

> I built a full bracket Monte Carlo simulator from scratch. Each game uses pace-adjusted offensive and defensive efficiency to estimate a win probability, then the simulator advances teams through the actual 2024 bracket thousands of times. The output is a probability distribution over round advancement and title odds. I also compare the model's favorites to seed/public expectations and validate against the real 2024 results.

