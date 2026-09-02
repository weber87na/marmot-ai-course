---
title: vscodevivm 操作 jupyter notebook
date: 2026-02-26 17:30:45
tags:
---
&nbsp;
<!-- more -->

<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/B61uoCxhxQg" 
title="VSCodeVim 操作 jupyter notebook" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>

jupyter notebook 搭配 vscodevim 操作的話, 等於在外層套了一層 jupyter notebook 的殼
這時候使用的熱鍵為 jupyter notebook
進去格子裡面則是使用 vscodevim 的熱鍵
剛開始學這個覺得詭異詭異的, 熱鍵都失效 XD

首先在 normal 模式按下 ese 後, 會看到格子外面框框亮起來, 如果要編輯格子的內容只需要按下 enter 即可

上方新增一個 cell: `a`

下方新增一格並且將目前焦點移動到下一格: `b`

移動到上一格: `k`

移動到下一格: `j`

移動到最後一格: `shift + g`

移動到第一格: `gg`

執行目前這格: `ctrl + Enter`

執行目前格子, 並在下方插入一格: `Alt + Enter`

執行目前 cell 執行完後移動到下一格: `Shift + Enter`

刪除 cell: `dd`

還原: `z`

後悔還原: `ctrl + y`

切換成 markdown: `m`

切換成程式碼：`y`

滾軸置中: `ctrl + l`

往上翻: `ctrl + u`

往下翻: `ctrl + d`

在 Jupyter 模式下存檔: `ctrl + s`

複製目前這格: `c`

往下貼上: `v`

最後可以在 `settings.json` 設定以下顏色方便區分

```
"workbench.colorCustomizations": {
    //jupyter 模式的外框
    "notebook.focusedCellBorder": "#ff0000",
    //編輯的格子外框
    "notebook.focusedEditorBorder": "#007acc",
}
```
