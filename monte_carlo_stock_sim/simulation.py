from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SimulationConfig:
    days: int = 252
    simulations: int = 500
    seed: int | None = 42

    def validate(self) -> None:
        if self.days <= 0:
            raise ValueError("days must be positive")
        if self.simulations <= 0:
            raise ValueError("simulations must be positive")


def simulate_prices(prices: pd.Series, config: SimulationConfig) -> pd.DataFrame:
    """Generate simulated price paths from historical close prices."""
    config.validate()
    clean_prices = prices.dropna().astype(float)
    if len(clean_prices) < 2:
        raise ValueError("at least two prices are required")
    if (clean_prices <= 0).any():
        raise ValueError("prices must be positive")

    returns = clean_prices.pct_change().dropna()
    daily_volatility = float(returns.std())
    if daily_volatility <= 0:
        raise ValueError("historical returns must have non-zero volatility")

    rng = np.random.default_rng(config.seed)
    shocks = rng.normal(0, daily_volatility, size=(config.days, config.simulations))
    paths = np.empty((config.days + 1, config.simulations))
    paths[0, :] = float(clean_prices.iloc[-1])

    for day in range(1, config.days + 1):
        paths[day, :] = paths[day - 1, :] * (1 + shocks[day - 1, :])

    return pd.DataFrame(paths, columns=[f"simulation_{i + 1}" for i in range(config.simulations)])


def summarize_simulations(simulations: pd.DataFrame) -> dict[str, float]:
    terminal = simulations.iloc[-1]
    return {
        "mean_terminal_price": float(terminal.mean()),
        "median_terminal_price": float(terminal.median()),
        "p05_terminal_price": float(terminal.quantile(0.05)),
        "p95_terminal_price": float(terminal.quantile(0.95)),
    }
