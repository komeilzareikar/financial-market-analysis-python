"""Functions for downloading and preparing market-price data."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
import yfinance as yf


def download_prices(
    tickers: Sequence[str],
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """Download adjusted closing prices for one or more tickers."""

    ticker_list = list(tickers)

    if not ticker_list:
        raise ValueError("At least one ticker must be provided.")

    downloaded_data = yf.download(
        ticker_list,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    if downloaded_data.empty:
        raise ValueError(
            "No market data was downloaded. Check the tickers and dates."
        )

    if isinstance(downloaded_data.columns, pd.MultiIndex):
        prices = downloaded_data["Close"].copy()
    else:
        prices = downloaded_data[["Close"]].copy()
        prices.columns = ticker_list[:1]

    return prices.dropna(how="all")