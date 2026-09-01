import pandas as pd
import pytest

from monte_carlo_stock_sim.simulation import SimulationConfig, simulate_prices, summarize_simulations


def test_simulation_shape_is_configurable() -> None:
    prices = pd.Series([100, 101, 99, 102, 104])
    result = simulate_prices(prices, SimulationConfig(days=10, simulations=3, seed=7))

    assert result.shape == (11, 3)
    assert list(result.columns) == ["simulation_1", "simulation_2", "simulation_3"]


def test_summary_contains_terminal_distribution() -> None:
    simulations = pd.DataFrame({"a": [100, 105], "b": [100, 95]})
    summary = summarize_simulations(simulations)

    assert summary["mean_terminal_price"] == 100
    assert summary["median_terminal_price"] == 100


def test_rejects_flat_prices() -> None:
    with pytest.raises(ValueError, match="non-zero volatility"):
        simulate_prices(pd.Series([100, 100, 100]), SimulationConfig())
