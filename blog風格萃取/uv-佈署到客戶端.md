---
title: uv 佈署到客戶端
date: 2026-05-11 16:42:28
tags:
---
&nbsp;
<!-- more -->

來跟風用看看 uv, 感覺起來就算有 uv python 仍然肥大又難搞

## 在客戶端執行 streamlit

步驟 1：在新機器上安裝 uv
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

步驟 2：將專案取得至新機器
透過 Git Clone 或是直接複製整個資料夾（請記得不要複製 .venv 資料夾，只複製原始碼與 uv.lock）。
如果是複製資料夾過去不要複製到 .venv 這裡面是 python 的環境
```
cd 您的專案資料夾路徑
```

步驟 3：還原環境 (Sync)
在專案目錄下執行：
它會自動讀取 uv.lock，自動下載正確版本的 Python，自動建立 .venv 虛擬環境，並把所有的套件安裝得跟原本一模一樣。
```
uv sync
```

步驟 4：執行您的應用程式
```
uv run streamlit run app.py
```

最終路徑 http://localhost:8501/

由於 dot ent file 不會進入版控, 請採用以下 format 來進行設定, 客戶端的 password 有可能預設不是 postgres
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_SCHEMA=yourschema
```
