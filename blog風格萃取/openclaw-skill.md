---
title: openclaw skill
date: 2026-03-20 02:04:20
tags: openclaw
---
&nbsp;
<!-- more -->

## 自訂土撥鼠偵測 skill

<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/UEW_lWR3mK8" 
title="openclaw 自訂 skill 偵測土撥鼠" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>

一直希望有個可以偵測土撥鼠的 skill 今天所幸就搞看看 XD
定義方法可以上 clawhub 找看看別人的 skill.md 檔丟給 antigravity 請他改成你的即可

skill 在此 https://github.com/weber87na/marmot-skilll

下載 skill 後放到 `~/.openclaw/skills` 底下
或放在 `~/.openclaw/workspace/skills` 底下

prompt
你執行 marmot-detector 的 skill 影片路徑在 ~/video/marmot.mp4 輸出路徑到 ~/marmot_clip 底下, 你記得切換環境 source ~/ultralytics-env/bin/activate

## openclaw skill 產生影片字幕

<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/6e3vrplZtsQ" 
title="openclaw skill 產生影片字幕" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>

openclaw 呼叫 Openai Whisper skill 產生影片字幕
需要先安裝 whisper
whisper 因為安裝在 python 環境之上
所以需要先切換環境 source venv/bin/activate
因為龍蝦不曉得這段所以呼叫時需要先下 prompt 叫他切換

skill
https://clawhub.ai/steipete/openai-whisper

prompt
我已經在 ~/venv 建立 python 環境, 你切換到 source venv/bin/activate
用 openai-whisper 技能產生 ~/video/Marmota_chonk_chonk_marmota_viralshorts.mp4 的 txt 字幕


## openclaw skill 下載 youtube 影片

<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/g3iVP6073Ag" 
title="openclaw skill 下載 youtube 影片" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>

確認機器有 python 下載 uv
```
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv --version
```

下載這個 skill 解壓縮
https://clawhub.ai/guoqiao/dl

放在 `~./openclaw/skills` 底下
重啟 gateway, 有時候龍蝦會笨笨的, 不曉得自己有什麼技能可以把 skill.md 貼給他
```
openclaw gateway restart
```

prompt
你用 dl 這個 skill 下載影片 https://www.youtube.com/shorts/sTezq-GOTY4 到 ~/video 資料夾底下


## openclaw skill 剪影片

<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/pq0n06zAJF4" 
title="openclaw skill 剪影片" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>

openclaw 使用 video-frames 這個 skill 剪老鼠廢片
需要安裝 ffmpeg
sudo apt update && sudo apt install ffmpeg

skill (已內建)
https://clawhub.ai/steipete/video-frames

prompt
你幫我用 video-frames 擷取 ~/video/marmot.mp4 從第 0 秒擷取到第 5 秒, 副檔名 mp4 檔名 
