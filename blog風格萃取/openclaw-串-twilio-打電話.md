---
title: openclaw 串 twilio 打電話
date: 2026-03-03 13:18:47
tags: openclaw
---
&nbsp;
<!-- more -->

因為朋友覺得龍蝦打電話很神奇, 就玩看看
最近聽說災情慘重, 很多人 google 帳號都被 ban, 我更新龍蝦後 google antigravity 這選項也直接消失 XD

## 更新龍蝦
更新 https://docs.openclaw.ai/install/updating

```
openclaw -v
# 2026.1.30

# 更新
npm i -g openclaw@latest

# 看看更新後的版本
openclaw -v
# 2026.3.1
```

因為 google antigravity 已經失效, 所以需要改成用 openrouter 一樣可以免費蹭
```
# 刪除有 antigravity 登入相關的即可
vim ~/.openclaw/agents/main/agent/auth-profiles.json

# 備份本來的 profiles
cd ~/.openclaw/agents/main/agent/
mv auth-profiles.json backup_auth-profiles.json

# 重新設定改用 openrouter
openclaw configure
```


## 打電話設定

打電話可以參考這兩個龍蝦官方說明

https://docs.openclaw.ai/cli/voicecall

https://docs.openclaw.ai/plugins/voice-call

```
# 查 plugin 狀態
openclaw plugins list
openclaw plugins enable voice-call
```

另外需要一個 twilio 帳號, 免費會送你 15 美元, 到這個 [twilio](https://www.twilio.com/en-us) 然後點選 start for free

進入到 dashboard 需要申請一個測試用的號碼, 點選第二個選項 `Twilio phone number` 即可獲得電話

```
Connect to 3rd-party applications
You'll need 3 things to use Twilio with most 3rd-party applications:

Account SID and Auth token
`Twilio phone number`
Upgraded Twilio account
```

另外要記得設定 Verified Caller IDs 填上自己電話通過驗證就對啦

接著在 twilio 設定 webhook, 先啟動 ngrok
```
ngrok http 3334
```

接著在 twilio 後台 `develop` => `phone numbers` => `active numbers` => `configure` 找到 `A call comes in Webhook` 然後設定他的 url

大概長這樣
```
https://xxx-2401-xxx-8c30-xxx-e129-b9c1-8754-xxx.ngrok-free.app/voice/webhook
```

最後設定龍蝦

```
vim ~/.openclaw/openclaw.json

# 重啟
openclaw gateway restart
```

感覺我不太會設定, 或是有 bug ~
其他問題可以翻看看這兩個 issues 
https://github.com/openclaw/openclaw/issues/11554 

https://github.com/openclaw/openclaw/issues/5732
我的 tts 沒生效這裡就先不放, 不過沒設定也是可以, 他打過來 default 有個外國女人的聲音, 另外我測中文也會失敗, 可是英文 ok, 整個滿崩潰 ~

最後在龍蝦聊天室對他說 打電話到這個號碼 +886987123456 訊息為: "may the force be with you"

他打來後記得要按下 `任意按鍵`

以下是我的設定 fromNumber 是要放 twilio 給你的電話
```
    "plugins": {
        "entries": {
            "line": {
                "enabled": true
            },
            "voice-call": {
                "enabled": true,
                "config": {
                    "provider": "twilio",
                    "publicUrl": "https://bfcb-2401-xxxx-8c30-ce83-xxxx-b9c1-xxxx-xxxx.ngrok-free.app/voice/webhook",
                    "twilio": {
                        "accountSid": "yourid",
                        "authToken": "yourtoken"
                    },
                    "fromNumber": "+19712880123",
                    "serve": {
                        "port": 3334,
                        "path": "/voice/webhook"
                    },
                    "outbound": {
                        "defaultMode": "notify"
                    },
                    "streaming": {
                        "enabled": true,
                        "streamPath": "/voice/stream"
                    }
                }
            }
        },
        "installs": {}
    }
```
