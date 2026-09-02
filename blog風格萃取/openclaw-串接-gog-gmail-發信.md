---
title: openclaw 串接 gog gmail 發信
date: 2026-04-06 02:11:54
tags: openclaw
---
&nbsp;
<!-- more -->

<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/wNxY73hZPqI" 
title="實測 openclaw 串接 gog gmail 發信" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen></iframe>

因為要繳 ai agent 報告, 本來想說用龍蝦送信過去這樣夠 agent 了吧
結果沒想到 gog 不能送 pdf XD
計畫直接毀滅, 不過都弄了就筆記這個功能

官網 https://gogcli.sh/
github https://github.com/steipete/gogcli

```
git clone https://github.com/steipete/gogcli.git
cd gogcli/
make
go version
sudo apt update
sudo apt install golang-go
make
./bin/gog --help

vim ~/.bashrc
export PATH="$PATH:$HOME/gogcli/bin"
```

然後到以下網址一一設定

設定 credentials
https://console.cloud.google.com/apis/credentials

建立專案
https://console.cloud.google.com/projectcreate

gmail api
https://console.cloud.google.com/apis/api/gmail.googleapis.com

oauth 畫面
https://console.cloud.google.com/auth/branding

加入測試使用者
https://console.cloud.google.com/auth/audience

OAuth client 設定, 記得選 Desktop
https://console.cloud.google.com/auth/clients

下載 json
client_secret_....apps.googleusercontent.com.json

```
gog auth credentials ~/Downloads/client_secret.json

gog auth add you@gmail.com

# 設定環境變數
vim ~/.bashrc
export GOG_ACCOUNT=your@gmail.com
source ~/.bashrc
```

看 email
```
gog gmail search 'newer_than:7d'
```

最後到 https://clawhub.ai/ 找出龍蝦爸爸的 gog skill
下載複製到 ~/.openclaw/skills 裡面即可呼叫龍蝦發信
