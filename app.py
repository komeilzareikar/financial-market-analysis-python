from datetime import date

import pandas as pd
import streamlit as st

from src.data_loader import download_prices
from src.metrics import calculate_drawdown, calculate_metrics
from src.portfolio import (
    calculate_cumulative_performance,
    calculate_equal_weight_returns,
)
from src.visualizations import (
    plot_correlation_matrix,
    plot_drawdowns,
    plot_normalized_performance,
    plot_portfolio_comparison,
    plot_portfolio_performance,
    plot_total_returns,
)


DEFAULT_TICKERS = [
    "AAPL",
    "NVDA",
    "TSLA",
    "BTC-USD",
    "^GSPC",
    "GC=F",
]


@st.cache_data(ttl=3600, show_spinner=False)
def load_market_data(
    tickers: tuple[str, ...],
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """Download and cache market data for one hour."""
    return download_prices(
        tickers,
        start_date=start_date,
        end_date=end_date,
    )


def calculate_asset_metrics(
    daily_returns: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate the project metrics for every asset."""
    return pd.DataFrame(
        {
            ticker: calculate_metrics(daily_returns[ticker])
            for ticker in daily_returns.columns
        }
    ).T


def calculate_asset_drawdowns(
    daily_returns: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate percentage drawdowns for every asset."""
    return pd.DataFrame(
        {
            ticker: calculate_drawdown(daily_returns[ticker]) * 100
            for ticker in daily_returns.columns
        }
    )


def show_analysis_highlights(
    asset_metrics: pd.DataFrame,
) -> None:
    """Display four headline results."""
    highest_return_asset = asset_metrics[
        "Total Return (%)"
    ].idxmax()

    most_volatile_asset = asset_metrics[
        "Annual Volatility (%)"
    ].idxmax()

    best_sharpe_asset = asset_metrics[
        "Sharpe Ratio"
    ].idxmax()

    worst_drawdown_asset = asset_metrics[
        "Maximum Drawdown (%)"
    ].idxmin()

    highlight_columns = st.columns(4)

    with highlight_columns[0]:
        st.metric(
            "Highest Total Return",
            highest_return_asset,
            (
                f"{asset_metrics.loc[highest_return_asset, 'Total Return (%)']:.2f}%"
            ),
        )

    with highlight_columns[1]:
        st.metric(
            "Highest Volatility",
            most_volatile_asset,
            (
                f"{asset_metrics.loc[most_volatile_asset, 'Annual Volatility (%)']:.2f}%"
            ),
        )

    with highlight_columns[2]:
        st.metric(
            "Best Sharpe Ratio",
            best_sharpe_asset,
            (
                f"{asset_metrics.loc[best_sharpe_asset, 'Sharpe Ratio']:.2f}"
            ),
        )

    with highlight_columns[3]:
        st.metric(
            "Worst Drawdown",
            worst_drawdown_asset,
            (
                f"{asset_metrics.loc[worst_drawdown_asset, 'Maximum Drawdown (%)']:.2f}%"
            ),
        )


st.set_page_config(
    page_title="Financial Market Analysis",
    page_icon="📈",
    layout="wide",
)

st.title("Financial Market Analysis")

st.write(
    """
    Analyse the historical performance, risk, and correlations of major
    financial assets.
    """
)

st.sidebar.header("Analysis Settings")

selected_tickers = st.sidebar.multiselect(
    "Select assets",
    options=DEFAULT_TICKERS,
    default=DEFAULT_TICKERS,
)

start_date = st.sidebar.date_input(
    "Start date",
    value=date(2020, 1, 1),
)

end_date = st.sidebar.date_input(
    "End date",
    value=date(2026, 1, 1),
)

run_analysis = st.sidebar.button(
    "Run Analysis",
    type="primary",
    use_container_width=True,
)

if not run_analysis:
    st.info(
        "Choose the assets and dates in the sidebar, then click "
        "**Run Analysis**."
    )

elif not selected_tickers:
    st.error("Select at least one asset.")

elif start_date >= end_date:
    st.error("The start date must be earlier than the end date.")

else:
    try:
        with st.spinner("Downloading market data..."):
            prices = load_market_data(
                tuple(selected_tickers),
                start_date.isoformat(),
                end_date.isoformat(),
            )

            # Keep only dates for which every selected asset has a price.
            common_prices = prices.dropna()

            if len(common_prices) < 2:
                raise ValueError(
                    "Not enough common price data is available for "
                    "the selected assets and dates."
            )

            # Calculate returns after aligning all assets to common dates.
            daily_returns = common_prices.pct_change(
                fill_method=None
            ).dropna()

            if daily_returns.empty:
                raise ValueError(
                    "Not enough return data is available for "
                    "the selected assets and dates."
                )

            asset_metrics = calculate_asset_metrics(daily_returns)
            drawdowns = calculate_asset_drawdowns(daily_returns)
            correlation_matrix = daily_returns.corr()

            normalized_prices = (
            common_prices
            / common_prices.iloc[0]
            * 100
            )

        st.success(
            f"Downloaded {len(prices):,} rows of market data "
            f"for {len(prices.columns)} asset(s)."
        )

        overview_tab, asset_tab, risk_tab, portfolio_tab, data_tab = (
            st.tabs(
                [
                    "Overview",
                    "Asset Analysis",
                    "Risk Analysis",
                    "Portfolio",
                    "Raw Data",
                ]
            )
        )

        with overview_tab:
            st.subheader("Analysis Highlights")
            show_analysis_highlights(asset_metrics)

            st.subheader("Asset Performance Metrics")

            st.dataframe(
                asset_metrics.round(2),
                use_container_width=True,
            )

            metrics_csv = (
                asset_metrics
                .round(2)
                .to_csv()
                .encode("utf-8")
            )

            st.download_button(
                label="Download Asset Metrics",
                data=metrics_csv,
                file_name="asset_metrics.csv",
                mime="text/csv",
            )

            st.caption(
                "Annual return is calculated as mean daily return "
                "multiplied by 252. The Sharpe ratio assumes a "
                "risk-free rate of zero."
            )

        with asset_tab:
            st.subheader("Normalised Asset Performance")

            performance_figure = plot_normalized_performance(
                normalized_prices,
                title="Normalised Asset Performance",
            )

            st.pyplot(performance_figure)

            st.subheader("Total Return by Asset")

            total_returns_figure = plot_total_returns(
                asset_metrics["Total Return (%)"],
                title="Total Return by Asset",
            )

            st.pyplot(total_returns_figure)

        with risk_tab:
            st.subheader("Drawdown Over Time")

            drawdown_figure = plot_drawdowns(
                drawdowns,
                title="Drawdown Over Time",
            )

            st.pyplot(drawdown_figure)

            st.subheader("Correlation Matrix")

            correlation_figure = plot_correlation_matrix(
                correlation_matrix,
                title="Correlation Matrix of Daily Returns",
            )

            st.pyplot(correlation_figure)

        with portfolio_tab:
            portfolio_assets = [
                ticker
                for ticker in daily_returns.columns
                if ticker != "^GSPC"
            ]

            if portfolio_assets:
                st.subheader(
                    "Equal-Weight Portfolio Performance"
                )

                portfolio_returns = (
                    calculate_equal_weight_returns(
                        daily_returns,
                        portfolio_assets,
                    )
                )

                portfolio_cumulative = (
                    calculate_cumulative_performance(
                        portfolio_returns,
                        starting_value=100,
                    )
                )

                portfolio_figure = (
                    plot_portfolio_performance(
                        portfolio_cumulative,
                        title=(
                            "Equal-Weight Portfolio Performance"
                        ),
                    )
                )

                st.pyplot(portfolio_figure)

                st.caption(
                    "The portfolio gives equal weight to every "
                    "selected asset except the S&P 500 benchmark."
                )

                if "^GSPC" in daily_returns.columns:
                    st.subheader(
                        "Equal-Weight Portfolio vs S&P 500"
                    )

                    benchmark_cumulative = (
                        calculate_cumulative_performance(
                            daily_returns["^GSPC"],
                            starting_value=100,
                        )
                    )

                    comparison = pd.concat(
                        [
                            portfolio_cumulative.rename(
                                "Equal-Weight Portfolio"
                            ),
                            benchmark_cumulative.rename(
                                "S&P 500"
                            ),
                        ],
                        axis=1,
                    ).dropna()

                    comparison = (
                        comparison
                        / comparison.iloc[0]
                        * 100
                    )

                    comparison_figure = (
                        plot_portfolio_comparison(
                            comparison,
                            title=(
                                "Equal-Weight Portfolio "
                                "vs S&P 500"
                            ),
                        )
                    )

                    st.pyplot(comparison_figure)

                    portfolio_comparison_metrics = (
                        pd.DataFrame(
                            {
                                "Equal-Weight Portfolio":
                                    calculate_metrics(
                                        portfolio_returns
                                    ),
                                "S&P 500":
                                    calculate_metrics(
                                        daily_returns[
                                            "^GSPC"
                                        ]
                                    ),
                            }
                        ).T
                    )

                    st.subheader(
                        "Portfolio vs Benchmark Metrics"
                    )

                    st.dataframe(
                        portfolio_comparison_metrics.round(2),
                        use_container_width=True,
                    )

                else:
                    st.info(
                        "Select the S&P 500 (^GSPC) to compare "
                        "it with the portfolio."
                    )

            else:
                st.warning(
                    "Select at least one asset other than the "
                    "S&P 500 to construct a portfolio."
                )

        with data_tab:
            st.subheader("Adjusted Closing Prices")

            st.dataframe(
                prices.tail(10),
                use_container_width=True,
            )

            st.caption(
                "The table shows the latest ten available rows. "
                "The downloaded CSV contains the complete dataset."
            )

            price_csv = prices.to_csv().encode("utf-8")

            st.download_button(
                label="Download Price Data",
                data=price_csv,
                file_name="market_prices.csv",
                mime="text/csv",
            )

    except ValueError as error:
        st.error(str(error))

    except Exception as error:
        st.error(
            f"Unable to complete the analysis: {error}"
        )