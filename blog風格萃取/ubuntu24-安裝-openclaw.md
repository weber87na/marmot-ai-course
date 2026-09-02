---
title: ubuntu24 安裝 openclaw
date: 2026-03-17 19:30:59
tags:
---
&nbsp;
<!-- more -->

<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/lvRKSWi8ulI" 
title="ubuntu 24 安裝 openclaw" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>

本來在 wsl 上面已經搞過一把, 朋友想在 linux 上弄看看, 所幸也玩玩

```
# 更新 ubuntu 套件
sudo apt update

# 安裝 vbox 相關套件
sudo apt install build-essential dkms linux-headers-$(uname -r)

# 更新 bashrc
source ~/.bashrc

# 安裝 VBoxLinuxAdditions
sudo sh VBoxLinuxAdditions.run

# 安裝好之後關機
poweroff
```


設定全螢幕
開啟 virtualbox 選到顯示
畫面 視訊記憶體 256 MB
圖形控制器 VMSVGA

```
# 安裝 nvm
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash

# 安裝 nodejs
nvm install 22

# 安裝 vim
sudo apt install vim

# 安裝 git
sudo apt install git

# 安裝龍蝦
npm i -g openclaw

# 設定龍蝦
openclaw onboard
```

到老黃的網站選模型
https://build.nvidia.com/models?filters=nimType%3Anim_type_preview

點 view code

https://integrate.api.nvidia.com/v1
deepseek-ai/deepseek-v3.2
