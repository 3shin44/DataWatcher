

# 專案內部PY引用路徑
import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from service.serverLogger.logger import loggerBox, reportBox
from service.dataFetcher.dataFetcher import *
from service.auth.getEnvVariable import getAuthConfig
from service.messageSender.LINE_Sender import sendLINEMsg

# 低於MA追蹤
reportBox("weeasdfireadscxv")