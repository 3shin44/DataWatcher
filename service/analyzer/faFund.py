from datetime import datetime, timedelta

# 專案內部PY引用路徑
import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from service.serverLogger.logger import loggerBox
from service.dataFetcher.dataFetcher import *
from service.auth.getEnvVariable import getAuthConfig
from service.messageSender.LINE_Sender import sendLINEMsg

"""
績效監看

提示訊息為公開資訊, 僅發送分析結果, 計算過程僅記錄於SERVER端供調閱
發送分析結果, 只回應"所有參數是否成功取得", 若成功取得再提供"距離門檻值差距"

"""

# 檢查績效結果 & 發送
def checkFaFundPerformance():
    try:
        # 取得計算用參數
        allParams = getAllParams()

        # 檢查所有參數是否成功取得
        checkFlag = all(value is not None for value in allParams.values())
        
        # 預設訊息
        sendMessage = f'{datetime.now().strftime("%Y-%m-%d")} 資料獲取失敗'
        # 計算結果
        if checkFlag:
            currentPerform = estimateUnsettle(allParams)
            sendMessage = f'{datetime.now().strftime("%Y-%m-%d")}: FaFund 距離設定門檻: {currentPerform}%'
        
        # 發送通知
        sendLINEMsg(sendMessage)
        
        loggerBox(f'checkFaFundPerformance success. ')
    except Exception:
        loggerBox(f'checkFaFundPerformance error. {Exception}')

# 產生計算參數物件
def getAllParams():
    # 計算參數物件
    allParams = {
        'recentPrice': None,
        'exRate1': None,
        'exRate2': None,
        'exRate3': None,
        'target': None,
        'feeRate': None
    }
    
    # 產生近五日 日期字串
    startDate = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    endDate= datetime.now().strftime("%Y-%m-%d")
    
    # recentPrice: 取得近5日報價, 並取最後一筆
    getTickerName = getAuthConfig('faTicker')
    priceDF = queryTickerPrice(getTickerName, startDate, endDate)
    if (priceDF is not None):
        allParams['recentPrice'] = priceDF.iloc[-1]['Close']
        
    # exRate1 取得第1種匯率
    getExType1 = getAuthConfig('faExType1')
    exRate1DF = queryExchangeRate(getExType1, startDate)
    if (exRate1DF is not None):
        allParams['exRate1'] = exRate1DF.iloc[-1]['spot_sell']
        
    # exRate2 取得第2種匯率
    getExType2 = getAuthConfig('faExType2')
    exRate2DF = queryOtherExchangeRate(getExType2, '5d')
    if (exRate2DF is not None):
        allParams['exRate2'] = exRate2DF.iloc[-1]['Close']
        
    # exRate3 取得第3種匯率
    getExType3 = getAuthConfig('faExType3')
    exRate3DF = queryOtherExchangeRate(getExType3, '5d')
    if (exRate3DF is not None):
        allParams['exRate3'] = exRate3DF.iloc[-1]['Close']
        
    # target 取得target資料
    getTarget = getAuthConfig('faTarget')
    targetDF = queryOtherExchangeRate(getTarget, '5d')
    if (targetDF is not None):
        allParams['target'] = targetDF.iloc[-1]['Close']
        allParams['feeRate'] = float(getAuthConfig('faFeeRate'))
    
    loggerBox(f'getAllParams: {allParams}')
    return allParams


# 計算距離設定值距離
def estimateUnsettle(allParam):
    getThreshold = float(getAuthConfig('faThreshold'))
    getCost = float(getAuthConfig('faCost'))
    currentValue = (allParam['recentPrice'] * float(getAuthConfig('faQty1')) * allParam['exRate1']) + \
                   (allParam['exRate2'] * float(getAuthConfig('faQty2')) * allParam['exRate1']) + \
                   (allParam['exRate3'] * float(getAuthConfig('faQty3')) * allParam['exRate1']) + \
                   (allParam['target'] * float(getAuthConfig('faFeeRate')))
    # to percentage
    performInPercent = ((currentValue - getCost)/getCost)*100
    # keep 2 digits
    performInPercent = round(performInPercent, 2)
    # return reuslt in 2 digits
    return round((performInPercent - getThreshold ), 2)