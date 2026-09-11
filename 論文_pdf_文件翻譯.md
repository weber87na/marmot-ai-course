[影片請參考](https://www.youtube.com/watch?v=FuhQMD2Tq_Y)

[專案網址](https://github.com/funstory-ai/BabelDOC)

這個範例需要使用 openai 的 token, 需要自己刷卡購買, 或是可以 fork 這個 babeldoc 專案看看能否改成用 oauth 來進行驗證吃訂閱

這個專案使用 `gpt-4o-mini` 翻譯的成本非常便宜, 要看帳單或使用量可以到 [這裡](https://platform.openai.com/usage)

實測翻譯了 30 篇學術論文以及一份長達 500 頁的 PDF, API 呼叫成本約僅 2 美元

翻譯 500 頁 pdf 範例 (powershell)

```powershell
babeldoc `
  --files 論文.pdf `
  --openai `
  --openai-model gpt-4o-mini `
  --openai-api-key "sk-xxxxxxxx" `
  --lang-in en `
  --lang-out zh-TW `
  --max-pages-per-part 50
```