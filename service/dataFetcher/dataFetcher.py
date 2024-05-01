from service.dataFetcher.finMind import *
from service.dataFetcher.yahooFinance import *
"""
獲取資料單一接口, 之後若目前資料來源失效再換

應定義INPUT與OUTPUT, 後續應使用PANDAS統一資料操作介面
"""

# 取得美股個股報價
def queryTickerPrice(ticker, startDate, endDate):
    return fm_getUSStockPrice(ticker, startDate, endDate)


# 取得匯率
def queryExchangeRate(currency, startData):
    return fm_getExchangeRate(currency, startData)


# 取得其他類型匯率報價
def queryOtherExchangeRate(currency, period):
    return yf_getTickerPrice(currency, period)