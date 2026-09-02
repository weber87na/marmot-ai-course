---
title: openclaw 串 line
date: 2026-02-02 07:15:29
tags: openclaw
---
&nbsp;
<!-- more -->

<iframe 
    width="1242" 
    height="699" 
    src="https://www.youtube.com/embed/Bl5wojf0OQU" 
    title="openclaw 串接 line" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
</iframe>

### 安裝 line plugin

因為他本地就已經有了所以只要啟用就好
剛睡醒沒發現一開始直接下 install 然後就噴 `plugin line: duplicate plugin id detected; later plugin may be overridden`
他應該是把 plugin 放到這個目錄底下 `~/.openclaw/extensions`

```
# 可以先執行看看有什麼 plugins
openclaw plugins list


# 啟用 line
openclaw plugins enable line

# 之後想關閉可以執行這個命令
# openclaw plugins disable line

# 重啟下
openclaw gateway restart

# 可以看看裡面幫我們增加了這些設定
#      "line": {
#        "enabled": true
#      }
vim ~/.openclaw/openclaw.json

# 看看是否有啟用
openclaw status
```

### 設定 line 部分
他官網只有寫到 console 這裡
https://developers.line.biz/console/

現在應該都直接在這邊建就好
https://manager.line.biz/

建立完成後開啟 `~/.openclaw/openclaw.json` 設定, 後來發現小龍蝦有 GUI 可以設定 = =
```
  "channels": {
    "line": {
      "channelSecret": "你的secret",
      "channelAccessToken": "你的token",
      "enabled": true,
      "dmPolicy": "pairing"
    }
  },
```

webhook 需要 https 我本地 windows 就有 ngrok 這裡就用本地的

最後在 line 設定 Messaging API Webhook網址 `https://12345xxxxx.ngrok-free.app/line/webhook` 注意後面要有 `/line/webhook`

傳送訊息給龍蝦他會要你貼上 code, 通過後就可以正常傳了

這邊開始非常危險, 測完請馬上關閉!
這邊開始非常危險, 測完請馬上關閉!
這邊開始非常危險, 測完請馬上關閉!
這邊開始非常危險, 測完請馬上關閉!
這邊開始非常危險, 測完請馬上關閉!
```
ngrok http 18789
```

如果手動驗證 code 可以參考這個命令
```
openclaw pairing list line
openclaw pairing approve line <你的CODE>
```
