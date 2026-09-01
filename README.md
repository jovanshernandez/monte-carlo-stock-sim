# Monte Carlo Stock Simulator

CLI tool for generating Monte Carlo stock-price scenarios from recent market data. The project has been refactored from a hardcoded script into a small package with configurable inputs, deterministic simulation behavior, tests, and report outputs.

![monte-carlo-ibm](https://user-images.githubusercontent.com/15150787/200733068-7ff883a2-8565-480a-a311-1c0ad9a04099.jpg)

## What It Shows

- Configurable ticker, lookback window, simulation count, forecast horizon, and random seed
- Testable simulation logic separated from market-data fetching and plotting
- Deterministic runs for validation and troubleshooting
- CSV and PNG outputs suitable for repeatable analysis workflows
- Unit tests for simulation behavior and edge cases
- GitHub Actions workflow for pull-request validation

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest -q
monte-carlo-stock-sim MSFT --days 90 --simulations 250
```

Reports are written to `reports/` by default.

The legacy script entry point still works:

```bash
python monte-carlo.py MSFT
```

## Repository Layout

```text
monte_carlo_stock_sim/
  cli.py          Console entry point and report writer
  market_data.py  yfinance data retrieval
  plotting.py     PNG chart output
  simulation.py   Testable Monte Carlo logic
tests/
  test_simulation.py
```

## Resume Positioning

This is strongest as a supporting analytics project. For SRE, emphasize deterministic runs, troubleshooting, and reproducible outputs. For platform engineering, emphasize the conversion from a one-off analysis script into a reusable CLI with tests and CI.
