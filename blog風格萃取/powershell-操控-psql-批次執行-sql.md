---
title: powershell 操控 psql 批次執行 sql
date: 2026-05-11 13:11:21
tags:
---
&nbsp;
<!-- more -->

筆記下用 powershell 批次執行 psql 遇到的問題

RROR:  character with byte sequence 0x82 0x99 in encoding
   "BIG5" has no equivalent in encoding "UTF8"

```powershell
$env:PGCLIENTENCODING = "utf8"
$env:PGPASSWORD = "postgres"
$host_ip = "localhost"
$username = "postgres"
$database = "postgres"

# 2. 執行資料夾內的所有 SQL 檔案
Get-ChildItem -Path .\sqls -Filter *.sql | ForEach-Object {
    Write-Host "正在執行 $($_.Name)..."
    psql -h $host_ip -U $username -d $database -f $_.FullName
}

# 3. (可選) 清除變數，增加安全性
$env:PGPASSWORD = ""
$env:PGCLIENTENCODING = ""
Write-Host "所有 SQL 檔案執行完畢！"
```
