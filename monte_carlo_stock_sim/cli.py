from __future__ import annotations

import argparse
import json
from pathlib import Path

from monte_carlo_stock_sim.market_data import fetch_close_prices
from monte_carlo_stock_sim.plotting import save_plot
from monte_carlo_stock_sim.simulation import SimulationConfig, simulate_prices, summarize_simulations


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Monte Carlo stock price simulations.")
    parser.add_argument("ticker", help="Ticker symbol to simulate.")
    parser.add_argument("--lookback-days", type=int, default=365)
    parser.add_argument("--days", type=int, default=252)
    parser.add_argument("--simulations", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    prices = fetch_close_prices(args.ticker, args.lookback_days)
    config = SimulationConfig(days=args.days, simulations=args.simulations, seed=args.seed)
    simulations = simulate_prices(prices, config)
    summary = summarize_simulations(simulations)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / f"{args.ticker.upper()}_simulations.csv"
    png_path = args.output_dir / f"{args.ticker.upper()}_simulations.png"
    simulations.to_csv(csv_path, index=False)
    save_plot(simulations, args.ticker, png_path)

    print(json.dumps({"csv": str(csv_path), "plot": str(png_path), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
