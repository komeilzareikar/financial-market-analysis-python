import pandas as pd
import pytest

from src.metrics import calculate_drawdown, calculate_metrics


def test_calculate_drawdown():
    returns = pd.Series([0.10, -0.20, 0.05])

    drawdown = calculate_drawdown(returns)

    assert drawdown.iloc[0] == pytest.approx(0.0)
    assert drawdown.iloc[1] == pytest.approx(-0.20)


def test_calculate_metrics_contains_expected_names():
    returns = pd.Series([0.01, -0.005, 0.02, 0.003])

    metrics = calculate_metrics(returns)

    expected_names = [
        "Total Return (%)",
        "Annual Return (%)",
        "Annual Volatility (%)",
        "Sharpe Ratio",
        "Maximum Drawdown (%)",
    ]

    assert list(metrics.index) == expected_names


def test_calculate_metrics_rejects_empty_returns():
    empty_returns = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        calculate_metrics(empty_returns)