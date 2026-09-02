---
title: Vibe coding notepad++ Hippie Completion plugin
date: 2026-01-16 05:57:36
tags:
---
&nbsp;
<!-- more -->

無聊試看看能否用 `AI Vibe Coding` 搞個 `notepad++` 的 `Hippie Completion` 沒想到也行 XD
首先安裝 `PythonScript` 這個外掛, 然後重啟 notepad++
接著找到 `Plugins -> Python Script -> New Script`
新增 `HippieCompletion.py` 把程式碼丟進去
點 `Add` 將他移動到 `Menu items` 然後重啟 notepad++
接著 `Settings -> Shortcut Mapper`
切換到 Plugin commands 分頁, 搜尋 `HippieCompletion` 然後設定 `Alt + /` 就收工了.. 好噁心

```
# -*- coding: utf-8 -*-
from Npp import editor, notepad
import re

# 使用 notepad 物件來儲存狀態，這樣按快捷鍵時資料才不會消失
if not hasattr(notepad, 'hippie_state'):
    notepad.hippie_state = {
        'original_prefix': '',
        'matches': [],
        'index': 0,
        'last_pos': -1
    }

def hippie_completion():
    state = notepad.hippie_state
    current_pos = editor.getCurrentPos()
    
    # 判斷是否為連續觸發 (按住 Alt+/ 不放或連續點擊)
    is_continuation = (current_pos == state['last_pos'] and state['original_prefix'] != '')

    if not is_continuation:
        # 1. 獲取游標前的單字作為前綴
        start_pos = editor.wordStartPosition(current_pos, True)
        prefix = editor.getTextRange(start_pos, current_pos)
        
        if not prefix:
            return

        # 2. 搜尋全文
        text = editor.getText()
        # 尋找所有以 prefix 開頭的單字字元 (\w+)
        pattern = r'\b' + re.escape(prefix) + r'\w+'
        all_matches = re.findall(pattern, text)
        
        # 3. 過濾重複並排除自己
        unique_matches = []
        for m in all_matches:
            if m != prefix and m not in unique_matches:
                unique_matches.append(m)
        
        if not unique_matches:
            return

        # 初始化本次補全狀態
        state['original_prefix'] = prefix
        state['matches'] = unique_matches
        state['index'] = 0
    else:
        # 已經在補全狀態中，切換到下一個匹配項
        state['index'] = (state['index'] + 1) % len(state['matches'])

    # 4. 執行替換邏輯
    match = state['matches'][state['index']]
    
    # 如果是連續觸發，要刪除的是上一次補全上去的長度；否則刪除原始前綴長度
    if is_continuation:
        # 這裡有個技巧：我們直接用當前游標位置減去上一個匹配詞的長度
        # 但最保險的方法是直接紀錄上一次替換的起始點
        pass 

    # 統一處理替換：選取從單字起始點到當前游標，然後替換成新詞
    word_start = current_pos - (len(state['matches'][state['index']-1]) if is_continuation else len(state['original_prefix']))
    
    # 在 PythonScript 中執行替換
    editor.setTargetStart(word_start)
    editor.setTargetEnd(current_pos)
    editor.replaceTarget(match)
    
    # 更新游標位置到單字尾端
    new_pos = word_start + len(match)
    editor.gotoPos(new_pos)
    state['last_pos'] = new_pos

if __name__ == "__main__":
    hippie_completion()
```
