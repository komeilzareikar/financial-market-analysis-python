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








def plot_drawdowns(
    drawdowns: pd.DataFrame,
    title: str = "Drawdown Over Time",
):
    """Plot drawdown history for multiple assets."""

    fig, ax = plt.subplots(figsize=(12, 6))

    drawdowns.plot(ax=ax)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown (%)")
    ax.grid(True)

    fig.tight_layout()

    return fig





def plot_correlation_matrix(
    correlation_matrix: pd.DataFrame,
    title: str = "Correlation Matrix of Daily Returns",
):
    """Create an annotated correlation heatmap."""

    fig, ax = plt.subplots(figsize=(10, 8))

    image = ax.imshow(
        correlation_matrix,
        cmap="coolwarm",
        interpolation="nearest",
    )

    fig.colorbar(image, ax=ax, label="Correlation")

    ax.set_xticks(range(len(correlation_matrix.columns)))
    ax.set_xticklabels(
        correlation_matrix.columns,
        rotation=45,
        ha="right",
    )

    ax.set_yticks(range(len(correlation_matrix.index)))
    ax.set_yticklabels(correlation_matrix.index)

    ax.set_title(title)

    for row in range(len(correlation_matrix.index)):
        for column in range(len(correlation_matrix.columns)):
            ax.text(
                column,
                row,
                f"{correlation_matrix.iloc[row, column]:.2f}",
                ha="center",
                va="center",
            )

    fig.tight_layout()

    return fig


def plot_portfolio_performance(
    portfolio_cumulative: pd.Series,
    title: str = "Equal-Weight Portfolio Performance",
):
    """Plot the cumulative performance of a portfolio."""

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        portfolio_cumulative.index,
        portfolio_cumulative,
        label="Equal-Weight Portfolio",
        linewidth=2,
    )

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Starting Value = 100")
    ax.legend()
    ax.grid(True)

    fig.tight_layout()

    return fig



def plot_portfolio_comparison(
    comparison: pd.DataFrame,
    title: str = "Equal-Weight Portfolio vs S&P 500",
):
    """Compare portfolio performance with a benchmark."""

    fig, ax = plt.subplots(figsize=(12, 6))

    comparison.plot(
        ax=ax,
        linewidth=2,
    )

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Starting Value = 100")
    ax.legend()
    ax.grid(True)

    fig.tight_layout()

    return fig