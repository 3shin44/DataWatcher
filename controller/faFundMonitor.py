from service.analyzer.faFund import checkFaFundPerformance
from service.serverLogger.logger import loggerBox

# 執行績效檢查
def getCurrentFaFundState():
    loggerBox(f'getCurrentFaFundState')
    checkFaFundPerformance()
    
getCurrentFaFundState()