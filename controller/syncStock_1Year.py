# 專案內部PY引用路徑
import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from service.dataFetcher.syncStock import syncStockPrice
from service.serverLogger.logger import loggerBox

# 更新資料至本地端 預設參數為 1y
def getSyncStockPrice(param):
    loggerBox(f'start getSyncStockPrice: {param}')
    syncStockPrice(param)
    
getSyncStockPrice({'period': '1y'})