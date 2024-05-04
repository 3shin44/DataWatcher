from datetime import datetime, timedelta
# 專案內部PY引用路徑
import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from service.serverLogger.logger import loggerBox
from service.auth.getEnvVariable import getAuthConfig
from service.dataFetcher.yahooFinance import yf_downloadHistory
from service.messageSender.LINE_Sender import sendLINEMsg
from dao.dbUtil import sqlExecutor

# SYNC Stock price to local DB
# params refes : https://github.com/ranaroussi/yfinance/wiki/Tickers
def syncStockPrice(params):
    try:
        # get stock list from .env
        getStockList = generateSyncList()
        
        # add postfix for yahoo finance API
        getStockList = [stock + '.TW' for stock in getStockList]
        loggerBox(f'getStockList: {getStockList}')
        
        # fetch stock price and insert to db
        for stock in getStockList:
            # get data from yahoo finance API
            newStockPrices = yf_downloadHistory(stock, params)
            if(newStockPrices is not None):
                insertDB(newStockPrices)
                
        # 發送通知
        loggerBox(f'syncStockPrice success')
        sendMessage = f'{datetime.now().strftime("%Y-%m-%d")}: Sync total {len(getStockList)} stocks ({params}) completed'
        sendLINEMsg(sendMessage)
    except Exception:
        loggerBox(f'syncStockPrice error. {Exception}')
        sendLINEMsg(f'{datetime.now().strftime("%Y-%m-%d")}: Sync failed.')


# Get stock list from .env (convert string to list)
def generateSyncList():
    stockList = getAuthConfig('syncStockList')
    stockList = stockList.split(',')
    return stockList


# insert to table with existance check
def insertDB(dataSet):
    # from dataFrame generate sql insert syntax
    for index, row in dataSet.iterrows():
        # format datetime to YYYY-MM-DD
        date_value = index
        date_value = date_value.strftime('%Y-%m-%d')
        # generate SQL insert template
        sqlTempalte = \
            f"INSERT INTO HIS_PRICE " \
            f"(TRADE_DATE, OPEN, HIGH, " \
            f"LOW, CLOSE, ADJ_CLOSE, " \
            f"VOLUME, TICKER) " \
            f"SELECT " \
            f"'{date_value}', {row['Open']}, {row['High']}, " \
            f"{row['Low']}, {row['Close']}, {row['Adj Close']}, " \
            f"{row['Volume']}, \'{row['Ticker']}\'" \
            f" WHERE NOT EXISTS ( " \
            f"SELECT 1 FROM HIS_PRICE " \
            f"WHERE TICKER = '{row['Ticker']}' AND TRADE_DATE = '{date_value}' " \
            f");"
        sqlExecutor(sqlTempalte)