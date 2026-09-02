---
title: dbeaver vim config
date: 2020-11-30 19:22:56
top: true
tags:
- vim
- dbeaver
---

<div style="display: flex; justify-content: center; margin: 20px 0;">
  <iframe 
    width="100" 
    height="100" 
    src="https://www.youtube.com/embed/ubMulKfAb-Y" 
    title="ビーバー流 働き方改革！" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" 
    allowfullscreen>
  </iframe>
</div>

&nbsp;
<!-- more -->

<iframe 
    width="1235" 
    height="772" 
    src="https://www.youtube.com/embed/N7vWnqHWCQo" 
    title="dbeaver vim 安裝及設定" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" 
    allowfullscreen>
</iframe>

最近整理文章加上朋友的案子用 mariadb 還有他們都用 [dbeaver](https://dbeaver.io/download/) 雖然還是土撥鼠更古椎一點, 但還是用吧 XD
記錄下安裝 [vrapper plugin](http://vrapper.sourceforge.net/home/) 過程免得之後又忘了
沒想到沒怎麼用到的 eclipse 竟然是 dbeaver 讓他還有機會活下去 LOL

在 `help` => `install new software` => `work with` 貼上 [vrapper](http://vrapper.sourceforge.net/update-site/stable) 
最好也要勾選 `surround` 這樣操作會更順些, 不過他的 surround 做得有點 bug bug 的 ~

想要相對行號的話可以找 [relative number](http://matf.github.io/relativenumberruler/updatesite/) (可以不裝)

順便提一下怎麼找到正確的 plugin 連結
首先到 [eclipse market](https://marketplace.eclipse.org) 搜尋想要的關鍵字
接著點選想要的套件圖示，在 install 下方有個下載圖示，點下去複製那個 url 才是真的連結


接著在使用者資料夾底下建立 `_vrapperrc` 檔案即可編輯自己想要的 config 
路徑
```
C:\Users\YourName
```

設定字體
`window` => `Preferences` => `User Interface` => `Appearance` => `Basic` => `Colors And Fonts` => `Basic` => `Text Font` => `Edit`
[fira code](https://github.com/tonsky/FiraCode)

設定背景色彩
`window` => `Preferences` => `Editors` => `Text Editors` => `Appearance color options` => `Color` => `定義自訂色彩`
rgb 239 255 239

另外有個很討厭的就是預設的 eclipse keybinding 會讓 ctrl + w 及 ctrl + h 砍字與 vim 衝突到
`window` => `Preferences` => `User Interface` => `Appearance` => `Keys` => 

搜尋以下內容並且 Unbind Command
Close
Open Search Dialog


萬一安裝 vrapper 他把 menu 變成黑色可以這樣還原

`Window` => `Preferences` => `General` => `Appearance` => `Theme` => `Light`


fullconfig
```
" _vrapperrc
" === 基礎設定 ===
set clipboard=unnamed
set ignorecase
set smartcase
set scrolloff=5

" 設定 Leader 鍵
let mapleader = ","

" === 定義 Eclipse 功能別名 (Eclipse Action Aliases) ===
" 語法: eclipseaction [別名] [Eclipse_Command_ID]
eclipseaction rename org.eclipse.jdt.ui.edit.text.java.rename.element
eclipseaction findInFiles org.eclipse.ui.edit.findReplace
eclipseaction find org.eclipse.ui.edit.findReplace
eclipseaction toggleComment org.eclipse.jdt.ui.edit.text.java.toggle.comment
eclipseaction quickFix org.eclipse.ui.edit.text.java.correction.assist
eclipseaction showCommands org.eclipse.ui.commands.showHelp
eclipseaction expandSelection org.eclipse.jdt.ui.edit.text.java.select.enclosing
eclipseaction contractSelection org.eclipse.jdt.ui.edit.text.java.select.last
eclipseaction openRecent org.eclipse.ui.file.openWorkspaceFile
eclipseaction solutionExplorer org.eclipse.ui.views.ResourceNavigator
eclipseaction format org.eclipse.jdt.ui.edit.text.java.format
eclipseaction organizeImports org.eclipse.jdt.ui.edit.text.java.organize.imports

" === 快捷鍵映射 ===

" Refactor / Rename
nmap <Leader>rv :rename<CR>

" 搜尋功能
nmap <Leader>qq :findInFiles<CR>
nmap <Leader>ss :find<CR>
vmap <Leader>ss :find<CR>

" 開啟指令面板 (像 VS 的 Command Window)
nmap <Leader>xm :showCommands<CR>

" 註解切換
nmap <Leader>ci :toggleComment<CR>
vmap <Leader>ci :toggleComment<CR>

" 擴展/反擴展選取
nmap <Leader>xx :expandSelection<CR>
vmap <Leader>xx :expandSelection<CR>
nmap <Leader>zz :contractSelection<CR>
vmap <Leader>zz :contractSelection<CR>

" 最近開啟檔案
nmap <Leader>zr :openRecent<CR>

" 視窗操作
nmap <Leader>x1 :split<CR>
nmap <Leader>x0 :quit<CR>

" 映射 ;; 為 Esc
imap <Leader><Leader> <Esc>

" 切換到專案總管
nmap ,e :solutionExplorer<CR>

" 導航與編輯優化
nmap zh ^
nmap zl $
imap zh <Esc>^i
imap zl <Esc>$a

" 快速補分號
nmap z; $a;<Esc>
imap z; <Esc>$a;

" 錯誤跳轉
nmap zn :eclipse org.eclipse.ui.edit.marker.next<CR>
nmap zp :eclipse org.eclipse.ui.edit.marker.previous<CR>

" 保存並重載設定 (Vrapper 的載入指令)
nmap <Leader>so :source ~/_vrapperrc<CR>
```
