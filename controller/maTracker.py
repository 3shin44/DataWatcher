# 專案內部PY引用路徑
import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from service.analyzer.maTracker import maTracker
from service.serverLogger.logger import loggerBox

# 執行追蹤檢查
def runMaTracker():
    loggerBox(f'start runMaTracker')
    maTracker()
    
maTracker()