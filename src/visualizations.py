"""Reusable financial visualisation functions."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_cumulative_returns(
    cumulative_returns: pd.DataFrame,
    title: str = "Cumulative Growth of $1",
):
    """Create a cumulative-return comparison chart."""

    fig, ax = plt.subplots(figsize=(12, 6))

    cumulative_returns.plot(ax=ax)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Growth of $1")
    ax.grid(alpha=0.3)

    fig.tight_layout()

    return fig


def plot_normalized_performance(
    normalized_data: pd.DataFrame,
    title: str = "Normalized Asset Performance",
):
    """Plot asset performance with every asset starting at 100."""

    fig, ax = plt.subplots(figsize=(12, 6))

    normalized_data.plot(ax=ax)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Starting Value = 100")
    ax.grid(alpha=0.3)

    fig.tight_layout()

    return fig



def plot_total_returns(
    total_returns: pd.Series,
    title: str = "Total Return by Asset",
):
    """Create a horizontal bar chart of total asset returns."""

    fig, ax = plt.subplots(figsize=(10, 6))

    total_returns.sort_values().plot(
        kind="barh",
        ax=ax,
    )

    ax.set_title(title)
    ax.set_xlabel("Total Return (%)")
    ax.grid(True)

    fig.tight_layout()

    return fig