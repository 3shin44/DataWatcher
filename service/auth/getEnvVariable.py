from dotenv import load_dotenv
import os

# 專案內部PY引用路徑
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from service.serverLogger.logger import loggerBox

def getAuthConfig(envName):
    load_dotenv()
    envValue = None
    try:
        envValue = os.getenv(envName)
    except:
        # should replace with serverLog
        loggerBox(f'get env variable {envName} error')
    finally:
        return envValue