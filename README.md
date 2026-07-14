# Financial Market Analysis in Python

## Project Overview

This project analyses and compares the performance of different financial assets using Python.

The goal is to compare return, volatility, drawdown, and risk-adjusted performance across stocks, cryptocurrency, the S&P 500, and gold.

## Assets Analysed

- Apple (AAPL)
- Nvidia (NVDA)
- Tesla (TSLA)
- Bitcoin (BTC-USD)
- S&P 500 (^GSPC)
- Gold (GC=F)

## Tools Used

- Python
- pandas
- NumPy
- matplotlib
- yfinance
- Google Colab
- GitHub

## Key Features

- Downloaded historical financial market data using `yfinance`
- Cleaned and prepared price data
- Normalised asset prices to compare performance fairly
- Calculated daily returns
- Calculated total returns
- Calculated annual volatility
- Calculated annual return
- Calculated Sharpe ratio
- Calculated maximum drawdown
- Visualised asset performance and drawdowns

## Key Questions

This project tries to answer:

1. Which asset had the highest total return?
2. Which asset was the most volatile?
3. Which asset had the best risk-adjusted return?
4. Which asset had the worst maximum drawdown?

## Results Summary

Based on the analysis:

- Nvidia had the highest total return.
- Tesla had the highest annual volatility.
- Nvidia had the best Sharpe ratio.
- Bitcoin had the worst maximum drawdown.

## What I Learned

Through this project, I practised:

- Python programming
- Working with financial data
- Data cleaning
- Data analysis with pandas
- Basic financial statistics
- Risk-return analysis
- Data visualisation with matplotlib
- Using GitHub for project presentation

## Future Improvements

Possible future improvements include:

- Add a correlation matrix
- Add portfolio comparison
- Add portfolio optimisation
- Build an interactive Streamlit dashboard
- Add more assets
- Compare different time periods
- Add benchmark analysis

## File

The main analysis is contained in:

`market_analysis.ipynb`
