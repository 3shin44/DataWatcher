import yfinance as yf
import pandas as pd
from service.serverLogger.logger import loggerBox
"""
Yahoo Finance
https://pypi.org/project/yfinance/
"""

def yf_getTickerInfo(tickerNmae):
    ticker = yf.Ticker(tickerNmae)
    # get all stock info
    print(ticker.info)
    
    
def yf_getTickerPrice(symbol, period):
    data = None
    try: 
        # Create a Ticker object for the symbol
        ticker = yf.Ticker(symbol)
        # Get historical data for the specified date
        data = ticker.history(period)
    except Exception:
        loggerBox(f'yf_getTickerPrice error. {Exception}')
    finally:
        return data

def yf_downloadHistoryAsCSV(ticker, start, end):
    # Download data
    data = yf.download(ticker, start, end)

    # Create DataFrame
    df = pd.DataFrame(data)
    # Convert columns to float with two decimal places
    float_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close']
    df[float_cols] = df[float_cols].astype(float).round(2)
    
    # Add Ticker column 
    toTWTickerID = ticker.replace(".TW", "")
    df['Ticker'] = toTWTickerID

    # Set CSV file name
    exportName = toTWTickerID + "_history_data.csv"
    # Save DataFrame to CSV
    df.to_csv(exportName)
    return exportName