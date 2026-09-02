---
title: hermes 安裝
date: 2026-04-11 07:30:51
tags:
---
&nbsp;
<!-- more -->

<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/8C7pOln2e9E" 
title="實測 hermes 安裝" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>


官方文件
https://hermes-agent.ai/how-to/install-hermes-agent
https://github.com/nousresearch/hermes-agent

```
#先看自己有無之前安裝的 linux
wsl --list

#看看線上有什麼 linux 可以使用
wsl --list --online

#安裝 ubuntu24.04 並且命名 hermes
wsl --install Ubuntu-24.04 --name hermes

#啟動 ubuntu24
wsl -d hermes

#更新
sudo apt update

#安裝 git
sudo apt install git

#看你要不要安裝 vim 反正我是邪教徒肯定裝
sudo apt install vim

#切換到 home 接著安裝 hermes 他上面寫說會幫你搞定 python 跟 nodejs
cd ~
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

#他中間會跳出官方要你買 plan 的畫面, 發生這段可以 ctrl + c 關閉
#讓設定生效並且啟動 hermes
source ~/.bashrc

#設定 model
hermes model

#最後執行 hermes 就可以叫他做牛做馬了 XD
hermes
```
