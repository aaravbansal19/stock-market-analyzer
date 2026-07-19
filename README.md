# Stock Market Analyzer

A python based financial data analysis tool which analyzes historical stock performance using Yahoo Finance data. 

Features
- Historical stock data using yfinance
-  Daily return statistical calculations
- Volatility analysis
- Rolling 20-day volatility
- Moving Averages (20, 50, and 100 days)
- Golden Cross and Death Cross detection
- Maxmimum Drawback
- Volume analysis
- Stock comparison
- Data visualization of all data calculations with matplotlib

Technologies Used 
- Python
- Pandas
- Numpy
- Matplotlib
- yfinance

Example Metrics 
The program calculates:
- Average Daily Return
- Median Daily Return
- Largest gains and losses
- Cumulative return - Winning and loosing streaks
- Trading volume statistics
- Volatility trends
- Maxmimum drawdown

Purpose 
This project explores quantitative finance concepts: 
- Risk measurement
- Market volatility
- Technical indicators
- Time series analysis 

## Example Usage

Run the program:

```bash
python3 stock_analyzer.py
```

Example input:

```text
Enter a stock ticker: AAPL
Enter a second stock ticker (press Enter if not comparing): MSFT
Enter a period (6mo, 1y, 2y, 5y): 2y
```

Example output:

```text
Stock Performance Summary

Ticker: AAPL
Trading Days: 500

Average Daily Return: 0.10%
Median Daily Return: 0.12%

Largest Daily Gain: 15.33%
Date: 2025-04-09

Largest Daily Loss: -9.25%
Date: 2025-04-03

Cumulative Return: 50.07%

Positive Return Days: 272
Negative Return Days: 227

Average 20 Day Volatility: 1.60%

Maximum Drawdown: -33.36%

Golden Cross Dates:
2024-12-03
2025-03-06
2025-06-05
```


## Visualizations

### Closing Price Analysis

![Closing Price](images/AAPL_price_chart.png)

### Moving Average Analysis

![Moving Averages](images/AAPL_moving_averages.png)

### Daily Return Distribution

![Daily Returns](images/AAPL_returns_histogram.png)

### Volatility Analysis

![Volatility](images/AAPL_volatility_chart.png)
