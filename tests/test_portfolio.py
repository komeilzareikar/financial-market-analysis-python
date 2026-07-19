import pandas as pd
import pytest

from src.portfolio import calculate_equal_weight_returns


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