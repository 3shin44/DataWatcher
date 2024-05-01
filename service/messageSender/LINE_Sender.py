import requests

# 專案內部PY引用路徑
import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from service.auth.getEnvVariable import getAuthConfig
from service.serverLogger.logger import loggerBox

# sendLINEMsg: 傳入字串訊息, 透過LINE發送訊息
def sendLINEMsg(message):
    try:
        # LINE REQUEST CONFIG
        url = 'https://api.line.me/v2/bot/message/push'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {getAuthConfig("LINE_TOKEN")}'
        }
        # REQUEST BODY
        data = {
            'to': getAuthConfig('LINE_user_id'),
            'messages': [
                {
                    'type': 'text',
                    'text': message
                }
            ]
        }
        # LOGGER
        response = requests.post(url, headers=headers, json=data)
        loggerBox(f'sendLINEMsg success. {response}')
    except Exception as error:
        loggerBox(f'sendLINEMsg error. {error}')
