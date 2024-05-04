import yfinance as yf
import pandas as pd

# 專案內部PY引用路徑
import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
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

def yf_downloadHistory(ticker, params):
    data = None
    try:
        # Download data
        downloadData = yf.download(ticker, **params)

        # Create DataFrame
        df = pd.DataFrame(downloadData)
        # Convert columns to float with two decimal places
        float_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close']
        df[float_cols] = df[float_cols].astype(float).round(2)
        
        # Add Ticker column 
        toTWTickerID = ticker.replace('.TW', '')
        df['Ticker'] = toTWTickerID
        # assign to result
        data = df
    except Exception:
        loggerBox(f'yf_getTickerPrice error. {Exception}')
    finally:
        return data
