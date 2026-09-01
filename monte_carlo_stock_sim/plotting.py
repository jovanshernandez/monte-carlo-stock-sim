from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_plot(simulations: pd.DataFrame, ticker: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 7))
    simulations.plot(ax=ax, legend=False, alpha=0.25)
    ax.axhline(simulations.iloc[0, 0], color="black", linewidth=1, linestyle="--", label="Last close")
    ax.set_title(f"Monte Carlo Simulation: {ticker.upper()}")
    ax.set_xlabel("Trading day")
    ax.set_ylabel("Simulated price")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)
