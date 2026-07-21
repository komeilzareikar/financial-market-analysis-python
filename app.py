from datetime import date

import pandas as pd
import streamlit as st

from src.data_loader import download_prices
from src.metrics import calculate_drawdown, calculate_metrics
from src.visualizations import (
    plot_correlation_matrix,
    plot_drawdowns,
    plot_normalized_performance,
    plot_portfolio_comparison,
    plot_portfolio_performance,
    plot_total_returns,
)
from src.portfolio import (
    calculate_cumulative_performance,
    calculate_equal_weight_returns,
)

DEFAULT_TICKERS = [
    "AAPL",
    "NVDA",
    "TSLA",
    "BTC-USD",
    "^GSPC",
    "GC=F",
]

# data caching

@st.cache_data(ttl=3600, show_spinner=False)
def load_market_data(
    tickers: tuple[str, ...],
    start_date: str,
    end_date: str,
):
    """Download and cache market data for one hour."""
    return download_prices(
        tickers,
        start_date=start_date,
        end_date=end_date,
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

if run_analysis:
    if not selected_tickers:
        st.error("Select at least one asset.")

    elif start_date >= end_date:
        st.error("The start date must be earlier than the end date.")

    else:
        try:
            with st.spinner("Downloading market data..."):
                prices = download_prices(
                    selected_tickers,
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat(),
                )

            st.success(
                f"Downloaded {len(prices):,} rows of market data."
            )

            st.subheader("Adjusted Closing Prices")

            st.dataframe(
                prices.tail(10),
                use_container_width=True,
            )

            # CSV downloads

            price_csv = prices.to_csv().encode("utf-8")

            st.download_button(
                label="Download Price Data",
                data=price_csv,
                file_name="market_prices.csv",
                mime="text/csv",
            )

            # financial metrics table

            daily_returns = prices.pct_change(
                fill_method=None
            ).dropna()

            asset_metrics = pd.DataFrame(
                {
                    ticker: calculate_metrics(daily_returns[ticker])
                    for ticker in daily_returns.columns
                }
            ).T

            st.subheader("Asset Performance Metrics")

            st.dataframe(
                asset_metrics.round(2),
                use_container_width=True,
            )

            # Download the metrics table

            metrics_csv = asset_metrics.round(2).to_csv().encode("utf-8")

            st.download_button(
                label="Download Asset Metrics",
                data=metrics_csv,
                file_name="asset_metrics.csv",
                mime="text/csv",
            )

            # summary metric cards

            st.subheader("Analysis Highlights")

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

            # normalised asset performance

            common_prices = prices.dropna()

            normalized_prices = (
                common_prices
                / common_prices.iloc[0]
                * 100
            )

            st.subheader("Normalised Asset Performance")

            performance_figure = plot_normalized_performance(
                normalized_prices,
                title="Normalised Asset Performance",
            )

            st.pyplot(performance_figure)

            # total-return chart

            st.subheader("Total Return by Asset")

            total_returns_figure = plot_total_returns(
                asset_metrics["Total Return (%)"],
                title="Total Return by Asset",
            )

            st.pyplot(total_returns_figure)
            
            # drawdown chart

            st.subheader("Drawdown Over Time")

            drawdowns = pd.DataFrame(
                {
                    ticker: calculate_drawdown(
                        daily_returns[ticker]
                    ) * 100
                    for ticker in daily_returns.columns
                }
            )

            drawdown_figure = plot_drawdowns(
                drawdowns,
                title="Drawdown Over Time",
            )

            st.pyplot(drawdown_figure)

            # correlation matrix

            st.subheader("Correlation Matrix")

            correlation_matrix = daily_returns.corr()

            correlation_figure = plot_correlation_matrix(
                correlation_matrix,
                title="Correlation Matrix of Daily Returns",
            )

            st.pyplot(correlation_figure)
            
            # equal-weight portfolio performance
            
            portfolio_assets = [
                ticker
                for ticker in selected_tickers
                if ticker != "^GSPC"
            ]

            if portfolio_assets:
                st.subheader("Equal-Weight Portfolio Performance")

                portfolio_returns = calculate_equal_weight_returns(
                    daily_returns,
                    portfolio_assets,
                )

                portfolio_cumulative = calculate_cumulative_performance(
                    portfolio_returns,
                    starting_value=100,
                )

                portfolio_figure = plot_portfolio_performance(
                    portfolio_cumulative,
                    title="Equal-Weight Portfolio Performance",
                )

                st.pyplot(portfolio_figure)

                st.caption(
                    "The portfolio gives equal weight to every selected asset "
                    "except the S&P 500 benchmark."
                )

                # equal-weight portfolio versus S&P 500 comparison chart
               
                if "^GSPC" in daily_returns.columns:
                    st.subheader("Equal-Weight Portfolio vs S&P 500")

                    benchmark_cumulative = calculate_cumulative_performance(
                        daily_returns["^GSPC"],
                        starting_value=100,
                    )

                    comparison = pd.concat(
                        [
                            portfolio_cumulative.rename(
                                "Equal-Weight Portfolio"
                            ),
                            benchmark_cumulative.rename("S&P 500"),
                        ],
                        axis=1,
                    ).dropna()

                    comparison = (
                        comparison
                        / comparison.iloc[0]
                        * 100
                    )

                    comparison_figure = plot_portfolio_comparison(
                        comparison,
                        title="Equal-Weight Portfolio vs S&P 500",
                    )

                    st.pyplot(comparison_figure)

                    # portfolio versus benchmark metrics table

                    portfolio_comparison_metrics = (
                        pd.DataFrame(
                            {
                                "Equal-Weight Portfolio":
                                    calculate_metrics(
                                        portfolio_returns
                                    ),
                                "S&P 500":
                                    calculate_metrics(
                                        daily_returns["^GSPC"]
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
                        "Select the S&P 500 (^GSPC) to compare it "
                        "with the portfolio."
                    )
            else:
                st.warning(
                    "Select at least one asset other than the S&P 500 "
                    "to construct a portfolio."
                )

        except ValueError as error:
            st.error(str(error))

        except Exception as error:
            st.error(
                f"Unable to download market data: {error}"
            )