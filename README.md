# Financial Market Analysis in Python

## Project Overview

This project analyses the historical performance and risk characteristics of several major financial assets from January 2020 through December 2025.

It compares stocks, Bitcoin, gold, and the S&P 500 using return, volatility, drawdown, correlation, and risk-adjusted performance metrics.

The project also constructs a daily-rebalanced equal-weight portfolio and compares its performance against the S&P 500 benchmark.

The analysis was first developed in a Jupyter notebook and then refactored into reusable Python modules with automated tests.

## Assets Analysed

- Apple (`AAPL`)
- Nvidia (`NVDA`)
- Tesla (`TSLA`)
- Bitcoin (`BTC-USD`)
- S&P 500 (`^GSPC`)
- Gold Futures (`GC=F`)

The equal-weight portfolio contains Apple, Nvidia, Tesla, Bitcoin, and gold. The S&P 500 is kept separate and used as the benchmark.

## Technologies Used

- Python
- pandas
- NumPy
- Matplotlib
- yfinance
- Jupyter Notebook
- pytest
- Git and GitHub
- Visual Studio Code

## Key Features

- Downloads historical market data using `yfinance`
- Cleans and prepares adjusted closing-price data
- Normalises asset prices for fair performance comparison
- Calculates daily asset returns
- Calculates total return and Annualised arithmetic return
- Calculates annualised volatility
- Calculates Sharpe ratio
- Calculates maximum drawdown
- Analyses correlations between asset returns
- Constructs a daily-rebalanced equal-weight portfolio
- Compares the portfolio against the S&P 500 benchmark
- Generates reusable Matplotlib visualisations
- Organises calculations into reusable Python modules
- Uses automated tests to verify financial calculations and error handling

## Key Questions

This project investigates:

1. Which asset produced the highest total return?
2. Which asset had the highest annualised volatility?
3. Which asset achieved the strongest risk-adjusted performance?
4. Which asset experienced the largest maximum drawdown?
5. How strongly were the assets correlated with one another?
6. How did the equal-weight portfolio perform compared with the S&P 500?
7. What return-and-risk trade-off did the portfolio provide relative to the benchmark?

## Results Summary

For the analysis period from January 2020 through December 2025:

- Nvidia (`NVDA`) produced the highest total return.
- Tesla (`TSLA`) had the highest annualised volatility.
- Nvidia achieved the highest Sharpe ratio, indicating the strongest risk-adjusted performance under the assumptions used in this project.
- Bitcoin (`BTC-USD`) experienced the largest maximum drawdown.

## Methodology and Assumptions

- Prices are downloaded from `yfinance` using automatically adjusted closing prices.
- Daily returns are calculated using percentage changes in asset prices.
- Annualised arithmetic return is estimated as the mean daily return multiplied by 252 trading days.
- Annualised volatility is calculated using daily standard deviation multiplied by the square root of 252.
- The Sharpe ratio assumes a risk-free rate of zero.
- The equal-weight portfolio assigns the same weight to each selected asset and is rebalanced daily.
- The analysis does not include transaction costs, taxes, slippage, or management fees.
- Results depend on the selected assets, dates, methodology, and available market data.

### Portfolio vs S&P 500

The daily-rebalanced equal-weight portfolio produced:

- Total return: `385.07%`
- Annualised return: `38.43%`
- Annualised volatility: `30.60%`
- Sharpe ratio: `1.26`
- Maximum drawdown: `-39.64%`

The S&P 500 benchmark produced:

- Total return: `82.93%`
- Annualised return: `15.03%`
- Annualised volatility: `20.68%`
- Sharpe ratio: `0.73`
- Maximum drawdown: `-21.58%`

The equal-weight portfolio substantially outperformed the S&P 500 and achieved a higher Sharpe ratio. However, this stronger performance came with higher volatility and a considerably deeper maximum drawdown.

Therefore, the portfolio delivered better risk-adjusted returns than the benchmark, but it was not the lower-risk investment.

## Project Structure

```text
financial-market-analysis-python/
├── market_analysis.ipynb
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── metrics.py
│   ├── portfolio.py
│   └── visualizations.py
└── tests/
    ├── test_metrics.py
    └── test_portfolio.py
```

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/komeilzareikar/financial-market-analysis-python.git
cd financial-market-analysis-python
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Open `market_analysis.ipynb` in Visual Studio Code or Jupyter Notebook, select the `.venv` Python environment, and run all cells.

## Running the Tests

Run the automated test suite from the project folder:

```bash
python -m pytest -v
```

The project currently contains nine automated tests covering:

- Financial metric calculations
- Drawdown calculations
- Equal-weight portfolio returns
- Cumulative portfolio performance
- Handling of empty or invalid inputs
- Handling of missing portfolio assets

## What I Learned

Through this project, I developed practical experience in:

- Writing Python for financial data analysis
- Working with pandas Series and DataFrames
- Downloading and preparing market data with `yfinance`
- Calculating return and risk metrics
- Understanding compounding, volatility, Sharpe ratio, and drawdown
- Comparing assets using normalised performance
- Constructing a daily-rebalanced equal-weight portfolio
- Comparing a portfolio against a market benchmark
- Creating reusable Matplotlib visualisation functions
- Refactoring notebook code into separate Python modules
- Writing automated tests with `pytest`
- Handling invalid inputs using exceptions
- Managing dependencies with a virtual environment and `requirements.txt`
- Using Git and GitHub to track and present project development

## Future Improvements

Planned improvements include:

- Build an interactive Streamlit dashboard
- Allow users to select assets and analysis dates
- Allow custom portfolio weights
- Add rolling volatility and rolling correlation analysis
- Include a configurable risk-free rate in the Sharpe ratio
- Add CAGR and Sortino ratio
- Add Value at Risk and other downside-risk measures
- Compare different rebalancing frequencies
- Add transaction costs and slippage
- Develop portfolio optimisation and strategy backtesting
- Support additional financial-data sources

## Disclaimer

This project is intended for educational and analytical purposes only. It does not constitute financial or investment advice.
