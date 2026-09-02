---
title: openclaw tts
date: 2026-03-12 03:38:02
tags: openclaw
---
&nbsp;
<!-- more -->


<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/pzUFP7bWoik" 
title="openclaw tts 文字轉語音" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
</iframe>

繼續跟風玩 openclaw 看到有語音功能覺得很有趣, 可惜雷半天

## edge

可以參考這個[官方說明](https://docs.openclaw.ai/tts)

只要把這段加上去 `openclaw.json` 即可, 最好用 `edge` 成功率比較高, `elevenlabs` 因為要錢雖然可以用免費版, 但問題一堆就放生 ~
設定完後最好還是執行 openclaw gateway restart, 我測 telegram 如果換聲音的話好像都要重啟, 不然會無效
最後音訊檔會在類似這種路徑底下 `/tmp/openclaw/tts-7r6W0a`

```
"tts": {
	"auto": "always",
	"provider": "edge",
	"edge": {
		"enabled": true,
		"voice": "zh-TW-HsiaoChenNeural",
		"lang": "zh-TW",
		"outputFormat": "audio-24khz-48kbitrate-mono-mp3",
		"rate": "+0%",
		"pitch": "+0%"
	},
	"elevenlabs": {
		"apiKey": "yourkey",
		"voiceId": "tItImbfnDIRVXll3jKPx",
		"modelId": "eleven_multilingual_v2"
	}
}
```

## elevenlabs
我是用 [ElevenLabs](https://elevenlabs.io/) 他有送免費額度可以玩看看

先用這個測試, 我一開始用聲音 library 的結果啥都沒有搞了老半天, 後來發現可以先在 create vioce 建立自己的聲音就能用了, 我自己建了兩個, 不過最後用 telegram 傳中文還是失敗

```
curl -X 'POST' \
	'https://api.elevenlabs.io/v1/text-to-speech/tItImbfnDIRVXll3jKPx' \
	-H 'xi-api-key:yourapikey' \
	-H 'Content-Type: application/json' \
	-d '{"text": "test", "model_id": "eleven_multilingual_v2"}'
```

如果有問題的話會噴下面這個 error
```
{
	"detail":{
		"type":"not_found",
		"code":"voice_not_found",
		"message":"A voice with voice_id '21mO4zV6TBFff9u45QHC' was not found.",
		"status":"voice_not_found",
		"request_id":"8fa2f408a94988fe95c089bcd8033244"
	}
}
```

他如果沒噴上面那段跳出警告的話就可以用下面這個指令測看看有文正確產 mp3, 失敗的話應該會是 0 個位元組的檔案
```
curl -X 'POST' \
'https://api.elevenlabs.io/v1/text-to-speech/tItImbfnDIRVXll3jKPx' \
-H 'xi-api-key:yourapikey' \
-H 'Content-Type: application/json' \
-d '{
"text": "你好 中文測試",
"model_id": "eleven_multilingual_v2"
}' \
--output chinese_test.mp3
```

openclaw 設定裡面有段 languageCode 我找半天, 後來發現這個[網站](https://localizely.com/iso-639-1-list/) 中文要用 `zh` 即可

```
    "messages": {                                                                                                                                                              "ackReactionScope": "group-mentions",                                                                                                                                  "tts": {                                                                                                                                                                   "auto": "always",
            "provider": "elevenlabs",
            "elevenlabs": {
                "apiKey": "yourapikey",
                "voiceId": "pNInz6obpgDQGcFmaJgB",
                "modelId": "eleven_multilingual_v2",
                "languageCode": "zh"
            }
        }
    },
```
