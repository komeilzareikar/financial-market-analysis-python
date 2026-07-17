"""Reusable financial performance calculations."""

from __future__ import annotations

import numpy as np
import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def calculate_drawdown(returns: pd.Series) -> pd.Series:
    """Calculate the drawdown series from periodic decimal returns."""
    clean_returns = returns.dropna()

    if clean_returns.empty:
        raise ValueError("Returns must contain at least one valid value.")

    cumulative_growth = (1 + clean_returns).cumprod()
    running_maximum = cumulative_growth.cummax()

    return cumulative_growth / running_maximum - 1


def calculate_metrics(
    returns: pd.Series,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> pd.Series:
    """Calculate common return and risk metrics."""
    clean_returns = returns.dropna()

    if clean_returns.empty:
        raise ValueError("Returns must contain at least one valid value.")

    total_return = (1 + clean_returns).prod() - 1
    annual_return = clean_returns.mean() * trading_days
    annual_volatility = clean_returns.std() * np.sqrt(trading_days)

    sharpe_ratio = (
        np.nan
        if annual_volatility == 0
        else annual_return / annual_volatility
    )

    maximum_drawdown = calculate_drawdown(clean_returns).min()

    return pd.Series(
        {
            "Total Return (%)": total_return * 100,
            "Annual Return (%)": annual_return * 100,
            "Annual Volatility (%)": annual_volatility * 100,
            "Sharpe Ratio": sharpe_ratio,
            "Maximum Drawdown (%)": maximum_drawdown * 100,
        }
    )