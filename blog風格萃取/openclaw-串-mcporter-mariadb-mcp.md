---
title: openclaw 串 mcporter mariadb mcp
date: 2026-04-12 01:39:40
tags:
---
&nbsp;
<!-- more -->

<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/qwscQNvA8b0" 
title="" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen></iframe>

範例資料庫下載位置, 這裡用 world 來測
https://dev.mysql.com/doc/index-other.html

mariadb mcp
https://github.com/mariadb/mcp

mcporter
https://github.com/steipete/mcporter

`注意要把 mcporter skill 打開`


確保已經安裝 uv, clone 專案並且安裝相依套件
```
# pip install uv
git clone https://github.com/mariadb/mcp.git
cd mcp
uv lock
uv sync
```

建立 .env 在 mcp 這個目錄底下, 實際最好建一個 read only 的 user, 我這裡偷懶
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=world

MCP_READ_ONLY=true
MCP_MAX_POOL_SIZE=10
```

測試
```
cd src
uv run server.py
```

測試 mcporter
```
mcporter call --output json \
  --stdio "uv --directory /home/openclaw/mcp/src run server.py" \
  list_databases
```

手動或是叫龍蝦幫你把路徑寫進去類似這樣的位置 `/home/openclaw/.openclaw/workspace/config/mcporter.json`
```
{
  "mcpServers": {
    "mariadb-server": {
      "command": "uv --directory /home/openclaw/mcp/src run server.py"
    }
  },
  "imports": []
}
```

如果是 gemini cli 只需要在 `gemini\settings.json` 裡面這樣設定就可以用了, 類似這樣

```
{
  "security": {
    "auth": {
      "selectedType": "oauth-personal"
    }
  },
  "mcpServers": {
    "mariadb-official": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\weberchang\\Desktop\\hermes\\mcp",
        "run",
        "src/server.py"
      ]
    }
  }
}
```
