---
title: vscode 加入右鍵選單
date: 2026-03-18 03:15:40
tags:
---
&nbsp;
<!-- more -->

因為 vscode 更新右鍵選單被弄壞了, 可以用下面這段存為 reg , 編碼務必要使用 `UTF-16 LE BOM` 不然會亂碼
注意他有兩種可能安裝的路徑, 需要執行的 reg 不太一樣

for 系統的 vscode 路徑 `C:\\Program Files\\Microsoft VS Code\\Code.exe`
```
Windows Registry Editor Version 5.00

; 針對檔案的右鍵選單
[HKEY_CLASSES_ROOT\*\shell\VSCode]
@="透過 Code 開啟"
"Icon"="%LocalAppData%\\Programs\\Microsoft VS Code\\Code.exe,0"

[HKEY_CLASSES_ROOT\*\shell\VSCode\command]
@="\"%LocalAppData%\\Programs\\Microsoft VS Code\\Code.exe\" \"%1\""

; 針對資料夾的右鍵選單
[HKEY_CLASSES_ROOT\Directory\shell\VSCode]
@="透過 Code 開啟"
"Icon"="%LocalAppData%\\Programs\\Microsoft VS Code\\Code.exe,0"

[HKEY_CLASSES_ROOT\Directory\shell\VSCode\command]
@="\"%LocalAppData%\\Programs\\Microsoft VS Code\\Code.exe\" \"%V\""

; 針對資料夾背景的右鍵選單
[HKEY_CLASSES_ROOT\Directory\Background\shell\VSCode]
@="透過 Code 開啟"
"Icon"="%LocalAppData%\\Programs\\Microsoft VS Code\\Code.exe,0"

[HKEY_CLASSES_ROOT\Directory\Background\shell\VSCode\command]
@="\"%LocalAppData%\\Programs\\Microsoft VS Code\\Code.exe\" \"%V\""
```

如果你的 vscode 是只有 for 使用者的話則要這樣

for 使用者的 vscode 路徑 `%LocalAppData%\Programs\Microsoft VS Code`

```
Windows Registry Editor Version 5.00

; --- 針對檔案的右鍵選單 ---
[HKEY_CLASSES_ROOT\*\shell\VSCode]
@="透過 Code 開啟"
"Icon"="C:\\Users\\<你的使用者名稱>\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe,0"

[HKEY_CLASSES_ROOT\*\shell\VSCode\command]
@="\"C:\\Users\\<你的使用者名稱>\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe\" \"%1\""

; --- 針對資料夾的右鍵選單 ---
[HKEY_CLASSES_ROOT\Directory\shell\VSCode]
@="透過 Code 開啟"
"Icon"="C:\\Users\\<你的使用者名稱>\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe,0"

[HKEY_CLASSES_ROOT\Directory\shell\VSCode\command]
@="\"C:\\Users\\<你的使用者名稱>\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe\" \"%V\""

; --- 針對資料夾背景的右鍵選單 ---
[HKEY_CLASSES_ROOT\Directory\Background\shell\VSCode]
@="透過 Code 開啟"
"Icon"="C:\\Users\\<你的使用者名稱>\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe,0"

[HKEY_CLASSES_ROOT\Directory\Background\shell\VSCode\command]
@="\"C:\\Users\\<你的使用者名稱>\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe\" \"%V\""
```

想要移除的話用以下
```
Windows Registry Editor Version 5.00

; 移除檔案右鍵選單
[-HKEY_CLASSES_ROOT\*\shell\VSCode]

; 移除資料夾右鍵選單
[-HKEY_CLASSES_ROOT\Directory\shell\VSCode]

; 移除資料夾背景右鍵選單
[-HKEY_CLASSES_ROOT\Directory\Background\shell\VSCode]
```
