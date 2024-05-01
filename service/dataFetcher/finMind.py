import requests
import pandas as pd
from service.serverLogger.logger import loggerBox
from service.auth.getEnvVariable import getAuthConfig

"""
finMind 服務
https://finmind.github.io/
"""


# getExchange: 取得匯率資訊
def fm_getExchangeRate(currency, startData):
    data = None
    try:
        url = 'https://api.finmindtrade.com/api/v4/data'
        parameter = {
            'dataset': 'TaiwanExchangeRate',
            'data_id': currency,
            'start_date': startData,
        }
        data = requests.get(url, params=parameter)
        data = data.json()
        data = pd.DataFrame(data['data'])

    except Exception:
        loggerBox(f'getExchange error. {Exception}')
    finally:
        return data


# fm_getUSStockPrice: 取得美股價資料
def fm_getUSStockPrice(ticker, startDate, endDate):
    data = None
    try:
        url = 'https://api.finmindtrade.com/api/v4/data'
        parameter = {
            'dataset': 'USStockPrice',
            'data_id': ticker,
            'start_date': startDate,
            'end_date': endDate,
            'token': getAuthConfig('finMind_TOKEN')
        }
        data = requests.get(url, params=parameter)
        data = data.json()
        data = pd.DataFrame(data['data'])
    except Exception:
        loggerBox(f'fm_getUSStockPrice error. {Exception}')
    finally: 
        return data
