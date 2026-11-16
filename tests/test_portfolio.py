import pandas as pd
import pytest

from src.portfolio import (
    calculate_cumulative_performance,
    calculate_equal_weight_returns,
)

def test_calculate_equal_weight_returns():
    returns = pd.DataFrame(
        {
            "AAPL": [0.10, 0.02],
            "NVDA": [0.20, -0.04],
        }
    )

    portfolio_returns = calculate_equal_weight_returns(
        returns,
        ["AAPL", "NVDA"],
    )

    assert portfolio_returns.iloc[0] == pytest.approx(0.15)
    assert portfolio_returns.iloc[1] == pytest.approx(-0.01)


def test_equal_weight_returns_rejects_empty_asset_list():
    returns = pd.DataFrame(
        {
            "AAPL": [0.01, 0.02],
        }
    )

    with pytest.raises(ValueError):
        calculate_equal_weight_returns(returns, [])


def test_equal_weight_returns_rejects_missing_asset():
    returns = pd.DataFrame(
        {
            "AAPL": [0.01, 0.02],
        }
    )

    with pytest.raises(ValueError):
        calculate_equal_weight_returns(
            returns,
            ["AAPL", "NVDA"],
        )








def test_calculate_cumulative_performance():
    returns = pd.Series(
        [0.10, -0.10],
        name="Portfolio",
    )

    cumulative = calculate_cumulative_performance(
        returns,
        starting_value=100,
    )

    assert cumulative.iloc[0] == pytest.approx(110.0)
    assert cumulative.iloc[1] == pytest.approx(99.0)
    assert cumulative.name == "Portfolio"


def test_cumulative_performance_rejects_empty_returns():
    empty_returns = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        calculate_cumulative_performance(empty_returns)


def test_cumulative_performance_rejects_invalid_starting_value():
    returns = pd.Series([0.01, 0.02])

    with pytest.raises(ValueError):
        calculate_cumulative_performance(
            returns,
            starting_value=0,
        )