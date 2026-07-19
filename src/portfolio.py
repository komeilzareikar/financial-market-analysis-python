"""Reusable portfolio calculation functions."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


def calculate_equal_weight_returns(
    returns: pd.DataFrame,
    assets: Sequence[str],
) -> pd.Series:
    """Calculate returns for a daily-rebalanced equal-weight portfolio."""

    asset_list = list(assets)

    if not asset_list:
        raise ValueError("At least one portfolio asset must be provided.")

    missing_assets = [
        asset for asset in asset_list
        if asset not in returns.columns
    ]

    if missing_assets:
        raise ValueError(
            f"Assets are missing from the returns data: {missing_assets}"
        )

    selected_returns = returns[asset_list].dropna()

    if selected_returns.empty:
        raise ValueError(
            "No valid return data is available for the selected assets."
        )

    portfolio_returns = selected_returns.mean(axis=1)
    portfolio_returns.name = "Equal-Weight Portfolio"

    return portfolio_returns