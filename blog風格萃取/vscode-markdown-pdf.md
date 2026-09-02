---
title: vscode markdown pdf
date: 2026-04-24 06:26:55
tags:
---
&nbsp;
<!-- more -->

老了記性差, 筆記下這個好用[工具](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf)
最近經常要交報告, 偏偏自己當工程師久了變笨都用 markdown, 而且 AI 生出來也都是 markdown
本來想說用 [typora](https://typora.io/) 可是要收費, 這對於一個免費仔當然是最後才走的途徑

之前就用過 `markdown-pdf` 覺得不錯, 可是不曉得怎麼設定 css 及隱藏`檔名` `日期` `頁碼` 原來只要在 `settings.json` 用以下設定即可

```json
    "markdown-pdf.styles": [
        "markdown-pdf.css",
    ],
    "markdown-pdf.displayHeaderFooter": false,
```

接著在自己的 folder 裡面蓋一個 `markdown-pdf.css`

```css
/* --- Markdown PDF 自定義樣式 --- */

/* 基礎頁面設定 */
body {
    font-family: "Segoe UI", "Source Code Pro", "Microsoft JhengHei", "微軟正黑體", sans-serif;
    font-size: 14px;
    line-height: 1.6;
    color: #333;
    margin: 0;
    padding: 20px;
}

/* 標題樣式 - 增加層次感 */
h1, h2, h3, h4, h5, h6 {
    color: #1a5f7a;
    font-weight: 700;
    margin-top: 24px;
    margin-bottom: 16px;
    line-height: 1.25;
}

h1 {
    font-size: 2em;
    padding-bottom: 0.3em;
    border-bottom: 2px solid #1a5f7a;
    text-align: center; /* 主標題置中 */
}

h2 {
    font-size: 1.5em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #eaecef;
}

/* 程式碼區塊 - 針對技術文件優化 */
code {
    font-family: "Cascadia Code", "Consolas", monospace;
    background-color: #f6f8fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 85%;
}

pre {
    background-color: #282c34; /* 深色背景，像 VS Code */
    padding: 16px;
    border-radius: 6px;
    overflow: auto;
    line-height: 1.45;
}

pre code {
    background-color: transparent;
    color: #abb2bf; /* 淺灰色字體 */
    padding: 0;
    font-size: 13px;
    white-space: pre-wrap;
    word-break: break-all;
}

/* 引用區塊樣式 */
blockquote {
    padding: 0 1em;
    color: #6a737d;
    border-left: 0.25em solid #dfe2e5;
    margin: 1em 0;
}

/* 列表與表格 */
ul, ol {
    padding-left: 2em;
}

table {
    border-spacing: 0;
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
}

table th, table td {
    padding: 6px 13px;
    border: 1px solid #dfe2e5;
}

table tr:nth-child(even) {
    background-color: #f6f8fa;
}

/* --- PDF 列印專屬優化 --- */
@media print {
    body {
        padding: 0;
        background-color: white;
    }

    /* 防止標題與內容被切斷 */
    h1, h2, h3 {
        page-break-after: avoid;
    }

    /* 防止程式碼區塊跨頁斷開 */
    pre, blockquote, table {
        page-break-inside: avoid;
    }

    /* 連結在列印時不顯示底線，但保留顏色 */
    a {
        text-decoration: none;
        color: #0366d6;
    }

    /* 自定義強制分頁類別：在 Markdown 加入 <div class="page-break"></div> 即可 */
    .page-break {
        page-break-before: always;
    }
}
```
