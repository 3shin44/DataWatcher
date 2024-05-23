# SERVER LOGGER
from datetime import datetime
import logging
import os

"""
獲取一個配置好的 logger 實例，日誌輸出到指定目錄下的文件。

參數:
log_name (str): logger 的名稱，用於區分不同的 logger。
log_dir (str): 日誌文件存放的目錄。
log_file_prefix (str): 日誌文件名的前綴，用於區分不同的日誌文件。

返回:
logging.Logger: 配置好的 logger 實例。
"""
def get_logger(log_name, log_dir, log_file_prefix):
    # 產生對應檔案名稱
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file_path = os.path.join(log_dir, f"{log_file_prefix}_{current_date}.log")
    
    # 建立logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    
    # 確保不重複添加處理器
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# loggerBox: 傳入字串訊息, 將加入時間戳記並寫入專案夾中log/資料夾下並以日期做區分
def loggerBox(msg):
    # 獲取專案根目錄
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # LOG檔案存放目錄, 檢查並建立有無存在
    log_dir = os.path.join(project_dir, 'log')
    os.makedirs(log_dir, exist_ok=True)
    
    logger = get_logger('serverLog', log_dir, 'serverLog')
    logger.info(msg)

# Report Logger
def reportBox(msg):
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # report檔案存放目錄, 檢查並建立有無存在
    log_dir = os.path.join(project_dir, 'report')
    os.makedirs(log_dir, exist_ok=True)
    
    logger = get_logger('report', log_dir, 'report')
    logger.info(msg)