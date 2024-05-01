import mysql.connector
from mysql.connector import Error

# 專案內部PY引用路徑
import sys
import os
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)
from service.serverLogger.logger import loggerBox
from service.auth.getEnvVariable import getAuthConfig

# 建立DB連線實體
def dbConnector():
    try:
        # Connect to DB
        conn = mysql.connector.connect(
            host = getAuthConfig('dbAddress'),
            user = getAuthConfig('dbUser'),
            password = getAuthConfig('dbPwd'),
            database = getAuthConfig('dnName')
        )
        return conn
    except Error:
        loggerBox(f'dbConnector error. {Error}')
        
# SQL執行: return flag for check result
def sqlExecutor(sqltemplate):
    successFlag = False
    try:
        # Connect to DB
        dbConn = dbConnector()
        dbConn.cursor().execute(sqltemplate)
        # Commit changes and close connection
        dbConn.commit()
        dbConn.close()
        successFlag = True
    except Error:
        loggerBox(f'sqlExecutor error. {Error}')
    finally:
        return successFlag

# SQL查詢, fetchAll: 取1筆 (預設全取)
def sqlQuery(sqltemplate, fetchAll=True):
    try:
        # Connect to DB
        dbConn = dbConnector()
        # get cursor and execute query
        cursor = dbConn.cursor()
        cursor.execute(sqltemplate)
        
        # package data
        if(fetchAll):
            queryResult = cursor.fetchall()
        else:
            queryResult = cursor.fetchone()

        return queryResult
    except Error:
        loggerBox(f'sqlQuery error. {Error}')
