# SERVER LOGGER
from datetime import datetime
import logging
import os
# loggerBox: 傳入字串訊息, 將加入時間戳記並寫入專案夾中log/資料夾下並以日期做區分
def loggerBox(msg):
    # 獲取專案根目錄  os.getcwd() 在Win/Linux解釋不同, 乖乖用OS抓路徑
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # LOG檔案存放目錄, 檢查並建立有無存在
    log_dir = os.path.join(project_dir, 'log')
    os.makedirs(log_dir, exist_ok=True)

    # 產生對應檔案名稱
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file_path = os.path.join(log_dir, f"serverLog_{current_date}.log")

    # 產生LOG訊息並寫入
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(msg)
    
# Report Logger
def reportBox(msg):
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # report檔案存放目錄, 檢查並建立有無存在
    log_dir = os.path.join(project_dir, 'report')
    os.makedirs(log_dir, exist_ok=True)

    # 產生對應檔案名稱
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file_path = os.path.join(log_dir, f"report_{current_date}.log")

    # 產生LOG訊息並寫入
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(msg)