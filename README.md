# Data Watcher

## Introduction

對特定資料獲取、分析、儲存，達到特定條件後發布訊息

## Project Structure
```
├─controller        接口層: 提供排成呼叫
├─dao               資料層: DB連接
├─log               LOG記錄檔
└─service           服務層:
    ├─analyzer        分析模組
    ├─auth            獲取驗證資訊模組
    ├─dataFetcher     外部資料獲取模組
    ├─messageSender	  訊息發送模組
    └─serverLogger    LOG紀錄模組
```
## Installation

1. 驗證資訊建立&存入對應參數
2. 虛擬環境初始化
3. 由requirements安裝lib