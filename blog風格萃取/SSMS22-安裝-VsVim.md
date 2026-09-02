---
title: SSMS22 安裝 VsVim
date: 2026-01-25 18:45:25
tags:
---
&nbsp;
<!-- more -->

常久以來 SSMS 好像都不能安裝 VsVim 看到 SSMS22 出了感覺是用 Visual Studio 的核心, 腦洞大開玩看看, 沒想到還可以阿 LOL


<iframe 
    width="1235" 
    height="772" 
    src="https://www.youtube.com/embed/k2b4DEV-Qu4" 
    title="How to Install VsVim in SSMS 22" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" 
    allowfullscreen>
</iframe>



安裝
首先 clone 這個專案
```
git clone https://github.com/VsVim/VsVim.git
```

接著編譯找到 `VsVim.vsix` 這隻檔案然後安裝
`VsVim\Binaries\Debug\VsVim2022\net472\VsVim.vsix`

解除安裝
找到以下路徑刪會看到版本號 `22.0_b4d04xxx` 刪除即可
`C:\Users\YOURNAME\AppData\Local\Microsoft\SSMS\22.0_b4d04xxx\Extensions`

