因為每個人作業系統環境不同, 我上面可以用的安裝方法不見得適用於每個人, 有問題請想辦法自行排除

## 必裝清單

* codex
* python
* nodejs


## Oracle VirtualBox (僅講解不用裝)
這是 [Oracle VirtualBox](https://www.virtualbox.org/wiki/Downloads) 佛心出品的虛擬機器, 常見的虛擬機還有 VMware Workstation Pro, hyper-v (要$$$ windows pro/enterprise)

因為有同學非 IT 背景, 所以稍微講解下, 虛擬機器 VM 可以想像為在電腦裡面模擬一個電腦出來, 這個模擬電腦的功能幾乎等同於真實電腦

常見用途為拿來測試軟體或特殊需求隔離環境測試, 模擬網路等 ...

因為 AI 帶來的便利, 現在也可以直接用 AI 來幫你安裝虛擬機器, 會透過 `VBoxManage.exe` 這個 cli 命令列程式

預設在這個路徑裡面 `C:\Program Files\Oracle\VirtualBox`
以下為 prompt

```
幫我用 VirtualBox 安裝 win11[Win11\_25H2\_Chinese\_Traditional\_x64\_v2.iso](Win11_25H2_Chinese_Traditional_x64_v2.iso) 
我已經有管理工具 VBoxManage 放在 C:\Program Files\Oracle\VirtualBox 路徑底下
資源分配的話要跑得順就好
VM 相關檔案位置都放在 D:\win11 這個資料夾底下
```

## notepad++ (可選)
[notepad++](https://notepad-plus-plus.org/downloads/) 因為操作 AI 或是 vibe coding 會有很多文字設定檔, 所以建議要裝這個, 遇到工程師也比較愛你

## notepad replacer (不用裝, IT 人員可考慮, 可選)
[notepad replacer](https://www.binaryfortress.com/NotepadReplacer/) 是可以把 notepad 命令改為呼叫 notepad++ 的小工具, 很實用

安裝並設定好後按下 `win + r` 開啟執行視窗, 接著輸入 notepad 即可開啟 notepad++

## winget (可選, 應該是內建)

winget 是 windows 套件管理器, win11 通常已經內建, 可以很方便的拿來安裝一些 windows 上面的工具

如果沒有 [winget](https://github.com/microsoft/winget-cli) 在 windows 平台會使用 [Chocolatey](https://chocolatey.org/)

他們在其他平台上的關係如下
```
Ubuntu  → apt
macOS   → brew
Windows → winget
```

也可以到這個[winstall](https://winstall.app/)搜尋想要安裝的程式, 就可以無腦安裝節省心力

## windows terminal (可選, win11 新版應該是有內建)

windows terminal 就像是一個管理 shell 的殼, 常見的 shell 有 cmd, powershell 5.1, powershell core, git bash, bash, zsh, fish...

以前沒有 windows terminal 通常會使用 [cmder](https://cmder.app/) 但是設定很噁心人, 為了不要浪費生命請盡早遠離

## powershell core (可選)

微軟的 `powershell` 分為兩種, 目前 win11 內建的還是舊版的 `5.1` 使用的命令為 `powershell`

新版則稱為 `powershell core`, 目前版本應該是 `7.6` 使用的命令為 `pwsh`

建議大家使用 `powershell core` 這樣後續使用 `coreutils` 還有 AI 呼叫一些工具才會更順

可以在電腦執行這個命令版本檢查
```
$PSVersionTable
```

powershell
```
Name                           Value
----                           -----
PSVersion                      5.1.26100.9168
PSEdition                      Desktop
PSCompatibleVersions           {1.0, 2.0, 3.0, 4.0...}
BuildVersion                   10.0.26100.9168
CLRVersion                     4.0.30319.42000
WSManStackVersion              3.0
PSRemotingProtocolVersion      2.3
SerializationVersion           1.1.0.1
```

powershell core
```
Name                           Value
----                           -----
PSVersion                      7.6.3
PSEdition                      Core
GitCommitId                    7.6.3
OS                             Microsoft Windows 10.0.26200
Platform                       Win32NT
PSCompatibleVersions           {1.0, 2.0, 3.0, 4.0…}
PSRemotingProtocolVersion      2.4
SerializationVersion           1.1.0.1
WSManStackVersion              3.0

```

powershell core 下載及安裝

[powershell core 官網](https://github.com/powershell/powershell)

[微軟說明頁面](https://learn.microsoft.com/zh-tw/powershell/scripting/install/install-powershell-on-windows?view=powershell-7.6)

最簡單的安裝方法
```
winget install --id Microsoft.PowerShell --source winget
```

## coreutils (可選)

[coreutils](https://github.com/microsoft/coreutils) 是微軟用 rust 重寫底層基本命令的工具, 為了在 AI 時代統一底層命令的行為跟 linux, macOS 輸出預期一樣

安裝方法如下
```
winget install Microsoft.Coreutils
```

## rg 及 fd (可選)

這兩個東西是 codex cli 預設用來查檔案的工具, 如果有安裝的話茶檔案速度應該是會提升, windows 預設沒這兩個工具

[rg](https://github.com/burntsushi/ripgrep)

[fd](https://github.com/sharkdp/fd)

```
winget install BurntSushi.ripgrep.MSVC
winget install sharkdp.fd
```

## yt-dlp (可選)
[yt-dlp](https://github.com/yt-dlp/yt-dlp) 是一個可以下載 youtube 影片的工具
```
winget install --id yt-dlp.yt-dlp -e --source winget
```

用法很腦殘, 只要像下面這樣加上網址即可
```
yt-dlp https://www.youtube.com/watch?v=olaOoD8O1l4
```

如果遇到無法下載的問題可能是版本過舊, 像以下這個問題他需要指定 nodejs 環境, 新版才會出現
```
🌹 yt-dlp https://www.youtube.com/watch?v=mSr7YHpZhJI
[youtube] Extracting URL: https://www.youtube.com/watch?v=mSr7YHpZhJI
[youtube] mSr7YHpZhJI: Downloading webpage
WARNING: [youtube] No supported JavaScript runtime could be found. Only deno is enabled by default; to use another runtime add  --js-runtimes RUNTIME[:PATH]  to your command/config. YouTube extraction without a JS runtime has been deprecated, and some formats may be missing. See  https://github.com/yt-dlp/yt-dlp/wiki/EJS  for details on installing one
[youtube] mSr7YHpZhJI: Downloading android vr player API JSON
[info] mSr7YHpZhJI: Downloading 1 format(s): 18
ERROR: unable to download video data: HTTP Error 403: Forbidden

```

可以用下面這個命令更新看看
```
yt-dlp --update-to nightly
```

這個指令可以看版本
```
🌹 yt-dlp --version
2026.08.20.234504
```

最後執行就正常了
```
yt-dlp --js-runtimes node "https://www.youtube.com/watch?v=mSr7YHpZhJI"
```

## ffmpeg (要玩影片才裝 可選)
[ffmpeg](https://www.ffmpeg.org/) 是影音處理工具, 常用剪片軟體 CapCut 威力導演內的核心應該都有用到它, 它可以剪片, 轉檔, 聲音淡化 等等各種效果
```
winget install Gyan.FFmpeg
```

## nodejs (必裝)

[nodejs](https://nodejs.org/zh-tw) 是讓 javascript 跑在電腦上的一種後端環境, 原本的 javascript 只能跑在瀏覽器 chrome firefox edge...

javascript 是一種程式語言, 常用在前端網頁

typescript 則是一種 javascript 的延伸語言, 他可以編譯出 javascript 程式碼

建立環境建議使用 [nvm](https://github.com/nvm-sh/nvm) 或 [fnm](https://github.com/schniz/fnm) 安裝, 它們可以快速切換不同版本的 nodejs

用 nvm 安裝時則要注意平台,如果是 windows 要使用 [nvm-windows](https://github.com/coreybutler/nvm-windows)
如果用 linux or macOS 則是原生的 [nvm](https://github.com/nvm-sh/nvm)

課程將示範 [fnm](https://github.com/schniz/fnm) 因為是用 rust 做的比較潮
```
winget install Schniz.fnm
```

fnm 安裝穩定版本的 nodejs
```
fnm install --lts

```

打開記事本或 notepad++ 將它塞入到設定檔內才可以一勞永逸
```
# C:\Users\你的帳號\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
# C:\Users\你的帳號\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
notepad $PROFILE

# 接著在檔案內設定這條即可
fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression
```

列出目前有什麼 nodejs 環境
```
fnm list
# 輸出
# * v24.19.0 default, lts-latest
# * system
```

切換至 nodejs 24
```
fnm use 24
# 輸出
# Using Node v24.19.0
```

最後執行看看 node 是否成功
```
node -v
# 輸出
# v24.19.0
```

## python (必裝)

python 是一個很噁心的程式語言, 它比 java 還更古老, 因為 AI 的關係所以爆紅, 寫起來就是噁心

python 的環境安裝往往讓人感到頭痛, 比較好的方式是使用 [uv](https://github.com/astral-sh/uv) 來進行安裝

```
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安裝好之後可以執行以下命令
```
uv -V
# 輸出
# uv 0.11.6 (65950801c 2026-04-09 x86_64-pc-windows-msvc)
```

## git (想學 vibe coding 才裝, 可選)

[git](https://git-scm.com/) 是一種版本管控工具, 學習曲線較高, 他可以用來管理檔案的版本, 告別用日期來命名檔案, final, final final, final final final 版本的問題


## github (建議要申請, 才有福利, 可選)

[github](https://github.com/) 是一個程式碼管理平台, 建議可以申請下, 後續有機會可以 vibe coding 的成果放到平台上


## vscode (想學 vibecoding 才裝, 可選)

visual studio code 簡稱 [vscode](https://code.visualstudio.com/) 是一個程式碼編輯器, 可以看做是輕量的 IDE(Integrated Development Environment)

常用在寫 python, javascript

因為名稱相近, 它常常會跟微軟另外一個產品 visual studio 搞混, 這個主要用途是拿來開發 asp.net core, csharp, c++ ...


今天還會有兩個 extension 需要下載

[liveserver](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)

[Codex – OpenAI’s coding agent](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt)


## postman (可選)

[postman](https://www.postman.com/) 是一種拿來測試後端 api 的工具, 因為它操作比較直覺, 不用背一堆指令所以用來測試後端 api 幾乎是標配

不想安裝的話也可以用 curl 代替, curl 也是一種拿來測試或呼叫後端 api 的工具, 在 win11 應該是已經內建在系統裡

但是舊版的 windows 內建的 curl 是 powershell 裡面非標準的 curl, 所以要設定 alias 才會正常

```
notepad $PROFILE

# 加入到設定檔內
if (Test-Path Alias:curl) { Remove-Item Alias:curl }
```

## codex (必裝)

[codex](https://openai.com/zh-Hant/codex/) 是一個 OpenAI 的 AI Agent 工具, 其他還有 google antigravity, anthropic claude code

今天主要是講解 codex, 因為目前看來它 CP 值最高, ChatGPT Plus Subscription 一個月 690

##  ChatGPT for Excel (常用 excel 工作者建議裝, 可選)

[ChatGPT for Excel](https://chatgpt.com/zh-Hant/apps/spreadsheets/) 他可以直接掛在 excel 裡面操作

## Blender (要玩 3d model 才安裝, 可選)

open source 的好用建模軟體 [blender](https://www.blender.org) 有想要 vibe coding 3d 網頁的可以安裝看看

## Antigravity (google 的 ai agent 比較可愛, 可選)

[antigravity](https://antigravity.google/)

如果還在觀望不想花錢, 或是有些低階任務可以安裝使用看看, 反正學校有額度目前免費


## 福利
可以先到這裡看[操作說明](https://go.nkust.edu.tw/info.php)

首先要拿學校信箱, 一個學生會有兩個信箱, 常用的會是 google 信箱, 另一個為 office365 的信箱, 所以應該是可以有兩倍的用量 XD

如果是學生的話 google 去年有送 google ai pro 版本, 今年則是送 plus 版本

可以到這個 google [官方連結](https://blog.google/innovation-and-ai/products/gemini-app/student-offer-google-ai/) 進行申請

其他學生福利則可以看[GitHub Copilot Student Pack](https://education.github.com/pack)

這裡面有涵蓋送網域, azure, jetbrains 一堆有的沒的

不過這認證有點噁心, 所以可以看[我之前的文章](https://blog.lasai.com.tw/posts/%E7%94%B3%E8%AB%8B-GitHub-Copilot-Student-Pack/)申請看看

如果在家申請不過的話, 請使用學校網路, 反正各種不同方法測試看看

如果你是程式相關工作者, dba, vim 狂熱者, 不想這麼麻煩, 應該也可以直接用學校信箱申請[jetbrains 大禮包](https://www.jetbrains.com/academy/student-pack/)

這裡面有 rider, pycharm, datagrip, intellij... 重點是有 ideavim XD

學校也有提供 matlab 教育版, 有需要也可以玩看看

## 程式課程推薦
如果你真的對程式語言有興趣, 想要多了解下, python 可以參考 [wilson-ren](https://wilson-ren.netlify.app/) 他在 udemy 上面販售的相關課程大概只要 `270 ~ 370`

想學習前端 css, 可以參考我的老師 [Amos 大神](https://www.youtube.com/watch?v=ZavL9y4Adrk&list=PLqivELodHt3iL9PgGHg0_EF86FwdiqCre)的前端課程, 雖然有點舊了, 不過底層概念就是這樣

如果對 AI 或其他程式內容有興趣也可以參考我無緣的老闆 [WILL 保哥的課程](https://learn.duotify.com/) 也可以上網搜尋他的粉專或是社團加入, 裡面有很多 AI 相關資訊
建議要有 IT 背景, 不然可能都火星文