# Imports all libraries
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# Gets information about which stock from user and downloads historical stock data from Yahoo Finance. 
ticker = input("Enter a stock ticker: ").upper()
ticker2 = input("Enter a second stock ticker (press Enter if not comparing): ").upper()

period = input("Enter a period (6mo, 1y, 2y, 5y): ")
data = yf.download(ticker, period=period, interval="1d")
data.columns = data.columns.droplevel(1)
if ticker2:
    data2 = yf.download(ticker2, period=period, interval="1d")
    data2.columns = data2.columns.droplevel(1)
    if not data2.empty:
        data2["Daily Return"] = data2["Close"].pct_change()
        data2 = data2.dropna()
        data2["20 Day Volatility"] = data2["Daily Return"].rolling(window=20).std()

if data.empty:
    print("Invalid ticker")
    exit()

if ticker2 and data2.empty:
    print("Invalid second ticker")
    exit()


filename = ticker + ".csv"
data.to_csv(filename)
print()
print("CSV has been successfully saved")


# Daily Return Calculations
data["Daily Return"] = data["Close"].pct_change()
data = data.dropna()
median_return = data["Daily Return"].median()

# Moving Average Calculations
data["20 Day MA"] = data["Close"].rolling(window=20).mean()
data["50 Day MA"] = data["Close"].rolling(window=50).mean()
data["100 Day MA"] = data["Close"].rolling(window=100).mean()
data["MA Difference"] = data["20 Day MA"] - data["50 Day MA"]
data["Golden Cross"] = ((data["MA Difference"] > 0) & (data["MA Difference"].shift(1) <= 0))
data["Death Cross"] = ((data["MA Difference"] < 0) & (data["MA Difference"].shift(1) >= 0))
golden_cross_dates = data[data["Golden Cross"]].index
death_cross_dates = data[data["Death Cross"]].index

# Volatility Calculations
volatility = data["Daily Return"].mean()
data["20 Day Volatility"] = data["Daily Return"].rolling(window=20).std()
highest_volatility = data["20 Day Volatility"].max()
highest_volatility_date = data["20 Day Volatility"].idxmax()
lowest_volatility = data["20 Day Volatility"].min()
lowest_volatility_date = data["20 Day Volatility"].idxmin()
high_volatility = data[data["20 Day Volatility"] > 0.02]

# Averages
average_volatility = data["20 Day Volatility"].mean()
average_volatility_2 = data2["20 Day Volatility"].mean()
average_return = data["Daily Return"].mean()
average_close = data["Close"].mean()
average_volume = data["Volume"].mean()

# Largest Gains and Losses
largest_gain = data["Daily Return"].max()
largest_gain_date = data["Daily Return"].idxmax()
lowest_loss = data["Daily Return"].min()
lowest_loss_date = data["Daily Return"].idxmin()

# Start and End 
start_price = data["Close"].iloc[0]
end_price = data["Close"].iloc[-1]
cumulative_return = (end_price - start_price) / start_price

# Calculates Maxmimum Drawdown
data['Peak'] = data["Close"].cummax()
data["Drawdown"] = (data["Close"] - data["Peak"]) / data["Peak"]
maximum_drawdown = data["Drawdown"].min()
maximum_drawdown_date = data["Drawdown"].idxmin()


# Calculates all positive and negative days calculations
positive_days = 0
negative_days = 0
flat_days = 0

for daily_return in data["Daily Return"]:
    if daily_return > 0:
        positive_days += 1
    elif daily_return < 0:
        negative_days += 1
    elif daily_return == 0:
        flat_days += 1

total_days = positive_days + negative_days + flat_days

positive_percentage = (positive_days / total_days) * 100
negative_percentage = (negative_days / total_days) * 100
flat_percentage = (flat_days / total_days) * 100

large_gains = 0
large_losses = 0

for daily_return in data["Daily Return"]:
    if daily_return > 0.02:
        large_gains += 1
        
    elif daily_return < -0.02:
        large_losses += 1

# Calculates all volume calculations
average_volume = data["Volume"].mean()
median_volume = data["Volume"].median()

highest_volume = data["Volume"].max()
highest_volume_date = data["Volume"].idxmax()

lowest_volume = data["Volume"].min()
lowest_volume_date = data["Volume"].idxmin()

# Calculates the winning and loosing streaks
current_gain = 0
longest_gain = 0

for daily_return in data["Daily Return"]:
    if daily_return > 0:
        current_gain += 1

        if current_gain > longest_gain:
            longest_gain = current_gain
    
    else:
        current_gain = 0

current_loss = 0
longest_loss = 0

for daily_return in data["Daily Return"]:
    if daily_return < 0:
        current_loss += 1

        if current_loss > longest_loss:
            longest_loss = current_loss
    
    else:
        current_loss = 0



# Prints the full report
print("Stock Performance Summary")
print()

print(f"Ticker: {ticker}")
print(f"Trading Days: {len(data)}")
print()
print()

print("All Daily Return Calculations:")
print(f"Average Daily Return: {average_return:.2%}")
print(f"Median Daily Return: {median_return:.2%}")
print()
print(f"Largest Daily Gain: {largest_gain:.2%}")
print(f"Date: {largest_gain_date}")
print()
print(f"Largest Daily Loss {lowest_loss:.2%}")
print(f"Date: {lowest_loss_date}")
print()
print(f"Cumulative Return: {cumulative_return:.2%}")
print()
print()

print("All Positive and Negative Day Calculations:")
print(f"Positive Return Days: {positive_days}")
print(f"Negative Return Days: {negative_days}")
print(f"Flat Days: {flat_days}")
print(f"Total Days: {total_days}")
print()
print(f"Positive Days Percentage: {positive_percentage:.2f}%")
print(f"Negative Days Percentage: {negative_percentage:.2f}%")
print(f"Flat Days Percentage: {flat_percentage:.2f}%")
print()
print(f"Days above +2%: {large_gains}")
print(f"Days above -2%: {large_losses}")
print()
print()


print("All Volume Calculations:")
print(f"Average Trading Volume: {average_volume:,.0f}")
print(f"Median Trading Volume: {median_volume:,.0f}")
print(f"Highest Trading Volume: {highest_volume:,.0f}")
print(f"Date: {highest_volume_date}")
print(f"Lowest Trading Volume: {lowest_volume:,.0f}")
print(f"Date: {lowest_volume_date}")
print()

print("Winning and Loosing Streaks: ")
print(f"Longest winning streak: {longest_gain}")
print(f"Longest loosing streak: {longest_loss}")
print()
print()


print("Moving Average Crossovers:")
print("Golden Cross Dates:")
for date in golden_cross_dates:
    print(date)
print()
print("Death Cross Dates:")
for date in death_cross_dates:
    print(date)
print()
print()

print("Volatility Analysis:")
print(f"Daily Volatility: {volatility:.2%}")
print(f"Average 20 Day Volatility: {average_volatility:.2%}")
print()
print()

print("Rolling Volatility:")
print(f"Highest 20 Day Volatility: {highest_volatility:.2%}")
print(f"Date: {highest_volatility_date}")
print(f"Lowest 20 Day Volatility: {lowest_volatility:.2%}")
print(f"Date: {lowest_volatility_date}")
print()
print()

print("Drawdown Analysis: ")
print(f"Maximum Drawdown: {maximum_drawdown:.2%}")
print(f"Occured On: {maximum_drawdown_date}")

# Basic closing price graph
def plot_stock_price(data, ticker, average_close):
    plt.figure(figsize=(14,7))
    plt.plot(data.index, data["Close"])
    plt.axhline(average_close, color="red", label="Average Closing Price")
    plt.legend()
    plt.title(f"{ticker} Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    filename = ticker + "_price_chart.png"
    plt.savefig(filename)
    plt.show()
    plt.close()

# Daily Return Graph
def plot_daily_returns(data, ticker):
    plt.figure(figsize=(14,7))
    positive_data = data[data["Daily Return"] > 0]
    negative_data = data[data["Daily Return"] < 0]
    plt.plot(data.index, data["Daily Return"])
    plt.axhline(0, color="red", label="Zero Return")
    plt.legend()
    plt.title(f"{ticker} Daily Return")
    plt.xlabel("Date")
    plt.ylabel("Daily Return")
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.grid()
    plt.tight_layout()
    filename = ticker + "_daily_returns.png"
    plt.savefig(filename)
    plt.show()
    plt.close()

# Daily Return Distribution 
def plot_return_histogram(data, ticker):
    plt.figure(figsize=(14,7))
    plt.hist(data["Daily Return"], bins=30, alpha=0.7, edgecolor="black")
    plt.title(f"{ticker} Distribution of Daily Returns")
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency")
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    plt.grid()
    plt.tight_layout()
    filename = ticker + "_returns_histogram.png"
    plt.savefig(filename)
    plt.show()
    plt.close()

# Volume Graph
def plot_volume(data, ticker):
    plt.figure(figsize=(14,7))
    plt.plot(data.index, data["Volume"])
    plt.axhline(average_volume, color="red", label="Average Volume")
    plt.legend()
    plt.title(f"{ticker} Volume (Millions)")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    filename = ticker + "_volume_chart.png"
    plt.savefig(filename)
    plt.show()
    plt.close()

# Comparing closing price graph
def plot_compare_stocks(data, data2, ticker, ticker2):
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data["Close"], label=ticker)
    plt.plot(data2.index, data2["Close"], label=ticker2)
    plt.title(f"{ticker} vs {ticker2} Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = ticker + "_vs_" + ticker2 + ".png"
    plt.savefig(filename)
    plt.show()
    plt.close()

# Moving Averages Graph
def plot_moving_averages(data, ticker, average_close):
    plt.figure(figsize=(14,7))

    print()
    print("Which moving averages do you want?")
    print("1 - 20 Day")
    print("2 - 50 Day")
    print("3 - 100 Day")
    print("4 - All")

    ma_choice = input("Selection: ").upper()

    plt.plot(data.index, data["Close"], color = "blue", label="Close Price")

    if ma_choice == "1":
        plt.plot(data.index, data["20 Day MA"], color = "orange", label="20 Day Moving Average")
    elif ma_choice == "2":
        plt.plot(data.index, data["50 Day MA"], color = "red", label="50 day Moving Average")
    elif ma_choice == "3":
        if data["100 Day MA"].isna().all():
            print("100 Day Moving Average unavailable")
            plt.close()
            return
        else:
            plt.plot(data.index, data["100 Day MA"], color="green", label="100 Day Moving Average")
    elif ma_choice == "4":
        plt.plot(data.index, data["20 Day MA"], color="orange", label="20 Day Moving Average")
        plt.plot(data.index, data["50 Day MA"], color="red", label="50 Day Moving Average")
        if data["100 Day MA"].isna().all():
            print("100 Day Moving Average unavailable")
            plt.close()
            return
        else:
            plt.plot(data.index, data["100 Day MA"], color="green", label="100 Day Moving Average")
    else:
        print("Invalid choice.")
        plt.close()
        return

    golden_data = data[data["Golden Cross"]]
    death_data = data[data["Death Cross"]]

    plt.scatter(golden_data.index, golden_data["20 Day MA"], color="green", s=40, marker="o", label="Golden Cross")
    plt.scatter(death_data.index, death_data["20 Day MA"], color="red", s=40, marker="o", label = "Death Cross")

    plt.axhline(average_close, color="black", label="Average Closing Price")
    plt.legend()
    plt.title(f"{ticker} Closing Price with Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    filename = ticker + "_moving_averages.png"
    plt.savefig(filename)
    plt.show()
    plt.close()

# Volatility Graph
def plot_volatility(data, ticker):
    plt.figure(figsize=(14,7))
    plt.plot(data.index, data["20 Day Volatility"])
    plt.axhline(average_volatility, color="red", label="Average Volatility")
    plt.title(f"{ticker} 20 Day Rolling Volatility")
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.xticks(rotation=45)
    plt.scatter(high_volatility.index, high_volatility["20 Day Volatility"], color="green", s=10, label="Above 2%")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    filename = ticker + "_volatility_chart.png"
    plt.savefig(filename)
    plt.show()
    plt.close()

# Comparing volatility Graph
def plot_volatility_two(data, data2, ticker, ticker2):
    plt.figure(figsize=(14,7))
    plt.plot(data.index, data["20 Day Volatility"], label=ticker, color="blue")
    plt.axhline(average_volatility, color="blue", label=ticker + " Average Volatility")
    plt.plot(data2.index, data2["20 Day Volatility"], label=ticker2, color="red")
    plt.axhline(average_volatility_2, color="red", label=ticker2 + " Average Volatility")
    plt.title(f"{ticker} vs {ticker2} 20 Day Rolling Volatility")
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    filename = ticker + "_vs_" + ticker2 + "_volatility_chart.png"
    plt.savefig(filename)
    plt.show()
    plt.close()

# Prints the graphing selection
while True:
    print()
    print("Choose a chart:")
    print("1 - Closing Price")
    print("2 - Daily Returns")
    print("3 - Daily Return Distribution")
    print("4 - Volume")
    print("5 - Compare Two Stocks")
    print("6 - Moving Averages")
    print("7 - Volatility")
    print("8 - Volatility (2 stocks)")
    print("Q - Quit")

    choice = input("Selection: ").upper()

    if choice == "1":
        plot_stock_price(data, ticker, average_close)

    elif choice == "2":
        plot_daily_returns(data, ticker)

    elif choice == "3":
        plot_return_histogram(data, ticker)

    elif choice == "4":
        plot_volume(data, ticker)

    elif choice == "5":
        if ticker2:
            plot_compare_stocks(data, data2, ticker, ticker2)
        else:
            print("No second stock was entered.")

    elif choice == "6":
        plot_moving_averages(data, ticker, average_close)

    elif choice == "7":
        plot_volatility(data, ticker)
    
    elif choice == "8":
        if ticker2:
            plot_volatility_two(data, data2, ticker, ticker2)
        else:
            print("No second stock was entered.")
    elif choice == "Q":
        print("Exiting program.")
        break

    else:
        print("Invalid choice. Try again.")