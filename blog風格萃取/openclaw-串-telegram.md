---
title: openclaw 串 telegram
date: 2026-03-09 22:22:02
tags: openclaw
---
&nbsp;
<!-- more -->

<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/hqYys2P7NAE" 
title="openclaw 串 telegram" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>

開啟 `@BotFather` 輸入 `/newbot`

輸入機器人名稱
接著輸入結尾為 bot 的機器人 username

`vim ~/.openclaw/openclaw.json`

這裡要注意複製官網的片段以後自己要把雙引號補上, 另外要移除逗號
vim format json 可以用 `:%!python3 -m json.tool`

```
"channels": {
 "telegram": {
  "enabled": true,
  "botToken": "yourcode",
  "dmPolicy": "pairing",
  "groups": { "*": { "requireMention": true } }
 }
},
```

開啟你的 bot `/start`
他會給你一串訊息

```
OpenClaw: access not configured.
Your Telegram user id: 1234567

Pairing code: 1234567
Ask the bot owner to approve with:
openclaw pairing approve telegram 1234567
```

最後執行以下把 pairing code 貼上去

```
openclaw gateway restart
openclaw pairing list telegram
openclaw pairing approve telegram yourcode
```
如果想要撤除 pairing code 
可以切換到這個目錄 cd `~/.openclaw/credentials/`
刪除對應通訊軟體的 json 即可
