# 專案內部PY引用路徑
import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from service.analyzer.faFund import checkFaFundPerformance
from service.serverLogger.logger import loggerBox

# 執行績效檢查
def getCurrentFaFundState():
    loggerBox(f'start getCurrentFaFundState')
    checkFaFundPerformance()
    
getCurrentFaFundState()