from datetime import datetime
# 專案內部PY引用路徑
import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from service.serverLogger.logger import reportBox
from service.dataFetcher.dataFetcher import *
from service.auth.getEnvVariable import getAuthConfig
from service.messageSender.LINE_Sender import sendLINEMsg
from dao.dbUtil import sqlQuery

# Moving Average Tracker
def maTracker():
    # get monitoring list
    getMonitoringList = getAuthConfig('maTrackerList')
    getMonitoringList = getMonitoringList.split(',')

    # get ma threshold and convert to int
    getMAThreshold = getAuthConfig('maTrackerThreshold')
    getMAThreshold = int(getMAThreshold)

    # generate report list
    reportList = []
    
    # analysis all stock, if any match, add to report list
    for ticker in getMonitoringList:
        tickerResult = analysisTicker(ticker, getMAThreshold)
        if(tickerResult is not None):
            reportList.append(tickerResult)

    # check report list is not empty, report detail to server and send simplify message
    if(len(reportList)):
        reportBox(reportList)
        sendLINEMsg(f'{datetime.now().strftime("%Y-%m-%d")}: maTracker found {len(reportList)} matches, remember check report')

# Analysis ticker is match ma threshold, return entire result or None
def analysisTicker(ticker='', maThreshold=1):
    reportTemplate = {
        'ticker': ticker,
        'currentPriceCLOSE': None,
        'currentPriceADJ': None,
        'maPriceCLOSE': None,
        'maPriceADJ': None
    }
    # update ticker name by code
    updateTickerName = getTickerName(ticker)
    if(updateTickerName is not None):
        reportTemplate['ticker'] = f'{updateTickerName[0]}({ticker})'
    
    # query current pirce
    currentPrice = queryNewestPrice(ticker)
    if(currentPrice is not None):
        #reportTemplate['currentPriceCLOSE']  = currentPrice[0]
        #reportTemplate['currentPriceADJ'] = currentPrice[0]
        reportTemplate['currentPriceCLOSE']  = round(currentPrice[0] ,2)
        #reportTemplate['currentPriceADJ'] = round(currentPrice[1] ,2)
        reportTemplate['currentPriceADJ'] = 30
    
    # query moving average
    maPrice = queryMovingAVG(ticker, maThreshold)
    if(maPrice is not None):
        reportTemplate['maPriceCLOSE']  = round(maPrice[0], 2)
        reportTemplate['maPriceADJ'] = round(maPrice[1], 2)


    # check all value is not None
    checkFlag = all(value is not None for value in reportTemplate.values())
    matchCloseFlag = reportTemplate['currentPriceCLOSE']  < reportTemplate['maPriceCLOSE'] 
    matchAdjFlag = reportTemplate['currentPriceADJ']  < reportTemplate['maPriceADJ']
    
    # if match condition, return report template 
    # very ugly style to return None or reach condition data
    if(checkFlag and (matchCloseFlag or matchAdjFlag)):
        return reportTemplate

    return None

# Query Moving Average(movingAvg) of Ticker
# return tuple (AVG_CLOSE, ADJ_CLOSE) or None
def queryMovingAVG(ticker='', movingAvg=1):
    sqlTemplate = \
        f"SELECT AVG(CLOSE) AS AVG_CLOSE, AVG(ADJ_CLOSE) AS AVG_ADJ" \
        f" FROM (" \
        f"    SELECT CLOSE, ADJ_CLOSE" \
        f"    FROM HIS_PRICE" \
        f"    WHERE TICKER = '{ticker}'" \
        f"    ORDER BY TRADE_DATE DESC" \
        f"    LIMIT {movingAvg}" \
        f" ) AS subquery;"

    return sqlQuery(sqlTemplate, False)
    

# Query ticker newest price
# return tuple (AVG_CLOSE, ADJ_CLOSE) or None
def queryNewestPrice(ticker=''):
    sqlTemplate = \
        f"SELECT CLOSE, ADJ_CLOSE" \
        f" FROM HIS_PRICE" \
        f" WHERE TICKER = '{ticker}'" \
        f" ORDER BY TRADE_DATE DESC" \
        f" LIMIT 1;" 

    return sqlQuery(sqlTemplate, False)

# get ticker name by ticker code
def getTickerName(ticker=''):
    sqlTemplate = \
        f"SELECT TICKER_NAME" \
        f" FROM TICKER_NAME" \
        f" WHERE TICKER='{ticker}';"
    
    return sqlQuery(sqlTemplate, False)
