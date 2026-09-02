---
title: openclaw 安裝 chrome extension (win11 + wsl)
date: 2026-02-01 16:55:19
tags: openclaw
---
&nbsp;
<!-- more -->

<iframe width="1235" 
    height="772" 
    src="https://www.youtube.com/embed/5vinJLAnlLI" 
    title="openclaw (clawdbot/moltbot) 安裝 chrome extension (win11 + wsl)" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" 
    allowfullscreen>
</iframe>


```
# 一律先更新不然會找不到套件
sudo apt-get update

# 參考微軟安裝 chrome
# https://learn.microsoft.com/zh-tw/windows/wsl/tutorials/gui-apps
cd /tmp
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -f ./google-chrome-stable_current_amd64.deb

# 輸入土撥鼠 應該是亂碼
google-chrome

# 安裝字體, 到這裡 chrome 中文就會正常了, 如果你有強迫症要在 wsl 裡面的 chrome 也打中文的話請繼續執行下面的指令
sudo apt install fonts-noto-cjk fonts-noto-cjk-extra

# 開啟 chrome 輸入土撥鼠應該就正常了
google-chrome

# 安裝切換輸入法相關的東東
sudo apt install im-config dbus-x11

# 安裝輸入法
sudo apt-get install fcitx5-*

# 設定 ~/.bashrc
vim ~/.bashrc

# 貼上以下內容
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export DefaultIMModule=fcitx

# 重載 ~/.bashrc
source ~/.bashrc

# 建立這個檔案
mkdir -p ~/.config/fcitx5

# 寫入設定
cat <<EOF > ~/.config/fcitx5/profile
[Groups/0]
Name=Default
Default Layout=us
DefaultIM=chewing

[Groups/0/Items/0]
Name=keyboard-us
Layout=

[Groups/0/Items/1]
Name=chewing
Layout=

[GroupList]
0=Default
EOF


# 這裡如果直接用 fcitx5 會遇到個超大的地雷, 雷很久
# E2026-02-01 14:37:54.898677 waylandeventreader.cpp:125] Wayland connection got error: 71
# 設定這個之後就能正常用了
fcitx5 --disable=wayland -d --replace

# ctrl + space 切換輸入法, 他的輸入法跟 windows 的是兩個不一樣的, 要留意下
google-chrome


# 安裝 chrome extension
openclaw browser extension install

# 查路徑
openclaw browser extension path

# 開啟 chrome
google-chrome

# 開啟 chrome://extensions
# 選擇 Developer mode
# 選剛剛的資料夾就可以把龍蝦的 chrome extension 載入進去了
# 接著要打開把他釘選才會生效

# 如果他叫你開 DISPLAY 的話可以這樣做, 感覺 chrome extension 好像比較穩定就是
vim ~/.bashrc
export DISPLAY=:0

```
