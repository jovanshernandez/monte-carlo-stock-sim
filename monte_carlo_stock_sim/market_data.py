from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import yfinance as yf


def fetch_close_prices(ticker: str, lookback_days: int = 365) -> pd.Series:
    if not ticker.strip():
        raise ValueError("ticker is required")
    if lookback_days <= 1:
        raise ValueError("lookback_days must be greater than 1")

    end = date.today()
    start = end - timedelta(days=lookback_days)
    data = yf.download(ticker.upper(), start=start.isoformat(), end=end.isoformat(), progress=False)
    if data.empty or "Close" not in data:
        raise ValueError(f"no close price data returned for {ticker}")
    return data["Close"]
