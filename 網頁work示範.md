
## work 範例
開啟網頁版 `work` 功能. 在手機上也可以這樣操作. 

接著談談使用 `work`  他是在雲端開啟一台虛擬機, 這裡面可以下載東西執行任務, prompt

```text
上網搜尋土撥鼠和河狸的圖片, 各 50 張, 並分成兩個資料夾, 供我做機器學習真假辨識訓練, 圖片大小需一致.
```

```text
搜尋十篇與土撥鼠演算法或仿生元啟發式演算法有關的論文, 下載後打包成 ZIP 檔給我.
```
## work 其他用法
如果你是開發人員或想要替程式加點功能, 也可以直接用 `work` 來做. 搭配 GitHub 的 GitHub Actions, 可以快速建立線上編譯環境.

需要安裝及設定 `ChatGPT Codex Connector`

https://chatgpt.com/codex/cloud/settings/connectors

`Settings` => `Integrations` => `Applications` 接著允許要編輯的 repository 即可

這個方法尤其點數燒不完的時候, 用手機丟下去做, 人跑去睡覺最適合.

像我自己是 `Vim` 邪教的信徒. 今天最後面介紹的後端程式會使用 `SQLite`, 我們會用到 `SQLiteBrowser` 這個工具, 但它不支援 `Vim` 這類功能, 所以我請它增加.

以下是幾輪主要的 `prompt`:

```markdown
## 建立 Vim 支援
https://github.com/sqlitebrowser/sqlitebrowser, 將這個功能加入 Vim 模式, 讓我可以在 Windows 上使用.


## 增加佈景
你能增加 UI 字體設定, 並加入 Dracula Theme 這個佈景嗎? 參考: https://draculatheme.com/

## 功能調整
我還需要把 Ctrl + W 關閉分頁這個功能移除, 否則我使用 Vim 刪除文字時會很不方便.

## 大功能調整實作
預設佈景直接使用 Dracula.

現在輸出 log 的字體還有問題, 請檢查 UI/Editor 各處與字體相關的設定, 我希望預設直接使用 Consolas 作為字體.

此外, 你目前的 Vim 基本功能實作也不完整. 例如使用 e 鍵進行移動時, 正常情況下, 在這一行按兩次 e 應該會移動到星號的位置, 但你的實作只會移動到 t 的位置.
SELECT *
FROM test;

此外, 我目前也無法使用 vimrc/init.lua 這類功能. 我希望你至少能加入以下我習慣的設定, 參考我的 nvim 設定 init.lua.
-- Insert mode mappings.
keymap("i", "<leader><leader>", "<Esc>", noremap_silent)
keymap("i", "z;", "<Esc>$a;", noremap_silent)
keymap("i", "zh", "<Esc>^i", noremap_silent)
keymap("i", "zl", "<Esc>$a", noremap_silent)
keymap("i", "z,", "<Esc>$a,", noremap_silent)

-- Normal mode mappings.
keymap("n", "<leader><leader>", "<Esc>", noremap_silent)
keymap("n", "<leader><space>", "<leader><leader><leader>bdw", noremap_silent)
keymap("n", "<leader>rv", lsp_rename, silent)
keymap("n", "<leader>qq", grep_prompt, silent)
keymap("n", "<leader>fp", copy_absolute_path, silent)
keymap("n", "<leader>fn", copy_relative_path, silent)
keymap("n", "<leader>tp", "<Cmd>botright split | terminal<CR>", noremap_silent)
keymap("n", "<leader>xm", ":", { noremap = true })
keymap("n", "<leader>ci", "gcc", { remap = true, silent = true })
keymap("n", "<leader>xs", "<Cmd>write<CR>", noremap_silent)
keymap("n", "<leader>ss", "/", { noremap = true })
keymap("n", "<leader>xf", ":edit ", { noremap = true })
keymap("n", "<leader>xk", "<Cmd>bdelete<CR>", noremap_silent)
keymap("n", "<leader>rr", open_recent_file, silent)
keymap("n", "<leader>kk", open_buffer, silent)
keymap("n", "<leader>ii", lsp_symbols, silent)
keymap("n", "<leader>x1", "<Cmd>only<CR>", noremap_silent)
keymap("n", "<leader>x3", "<Cmd>vsplit<CR>", noremap_silent)
keymap("n", "<leader>x2", "<Cmd>split<CR>", noremap_silent)
keymap("n", "<leader>x4", "<Cmd>vsplit | split | wincmd l | split | wincmd h<CR>", noremap_silent)
keymap("n", "<leader>x0", "<Cmd>close<CR>", noremap_silent)
keymap("n", "<leader>xz", "<Cmd>botright split | terminal<CR>", noremap_silent)
keymap("n", "<leader>ff", "<Cmd>only<CR>", noremap_silent)
keymap("n", "<leader>wh", "<C-w>h", noremap_silent)
keymap("n", "<leader>wj", "<C-w>j", noremap_silent)
keymap("n", "<leader>wk", "<C-w>k", noremap_silent)
keymap("n", "<leader>wl", "<C-w>l", noremap_silent)
keymap("n", "<leader>wq", "<Cmd>wq<CR>", noremap_silent)
keymap("n", "zh", "^", noremap_silent)
keymap("n", "zl", "$", noremap_silent)
keymap("n", "z;", "$a;<Esc>", noremap_silent)
keymap("n", "z,", "$a,<Esc>", noremap_silent)

-- Visual mode mappings.
keymap("x", "<leader><leader>", "<Esc>", noremap_silent)
keymap("x", ";h", [[:s?^\(\s*\)+ '\([^']\+\)',*\s*$?\1\2?g<CR>]], noremap_silent)
keymap("x", ";q", [[:s?^\(\s*\)\(.*\)\s*$?\1+ '\2'?<CR>]], noremap_silent)
keymap("x", "<leader>ci", "gc", { remap = true, silent = true })
keymap("x", "<leader>aa", [["+y]], noremap_silent)
keymap("x", "<leader>qq", grep_prompt, silent)
keymap("x", "<leader>ss", "/", { noremap = true })
```

## google spark

談了那麼多 `ChatGPT` 的功能, 這裡介紹下 google 的功能

如果沒有下載需求, 其實也可以試試 Google Spark, 效果類似, 不過 Spark 目前不支援下載功能.

Spark 有個超強功能. 它能以飛快的速度產生 YouTube 影片的字幕.

不過他好像只適用已經上傳一陣子的影片, 即使影片沒有開啟自動字幕也可以抓到, 因為 google 已經在後台偷偷把字幕擷取出來

prompt

```
https://www.youtube.com/watch?v=9HcW0pRnjs4 詳細列出這部影片在講什麼, 並提供影片的逐字稿.
```

結果

```
這則影片來自 YouTube: "海濤法師 一切都是假的!!", 長度約 1 分 28 秒. 內容為海濤法師在弘法開示時, 勸導信眾 "放下執著, 視世間表象為虛妄" 的經典開示片段(亦即網路上廣為流傳的 "假的! 眼睛業障重" 這句名言的出處).

1. 影片內容詳細重點
核心觀點: 把假的當作假的看, 就不會執著.

海濤法師主張, 世間萬物與遭遇都只是 "暫時的" 現象. 若能將其視為虛妄不實(假的), 內心就不會產生痛苦與執著; 反之, 若當成真的, 就會引發極大的情緒波動.

經典情境舉例: 撞見丈夫外遇

法師舉例: 假設一名婦人晚上在寺廟辦法會, 打坐, 並將功德迴向給丈夫, 祝他事業發達; 提早回家開門, 卻赫然撞見丈夫與另一名女子同床.

法師建議當下應立刻把門關上, 對自己說: "假的! 哎呀, 我眼睛業障重啊, 假的!", 然後在門外繼續打坐, 念 "阿彌陀佛", 避免落入執著與痛苦.

"鈔票共用" 與前世因果的比喻

法師以輪迴與因果解釋, 認為那位外遇對象可能是丈夫前世的妻子, 甚至說是自己 "侵占人家的".

法師將人比喻為手上的鈔票: 鈔票在流通時別人也用過, 只要還能使用就好, 不必過度計較是否被 "共用".

結論

勸告信眾不用過度深究伴侶在外是否有外遇, 把它當作不知道, 當作假的來看待, 心裡便能釋懷與解脫.

2. 影片完整逐字內容
(依語音流暢度整理標點, 完整保留原話內容)

[00:00] 當假的看, 你就不會執著.

[00:02] 假的! 今天晚上你在少林寺辦法會, 打坐, 很快樂, 迴向給你老公事業發達.

[00:08] 結果你突然早一點回家, 門打開, 你老公跟別個女人在睡覺.

[00:13] 你要馬上關起來: "假的! 哎呀, 我眼睛業障重啊, 假的!" 在外面繼續打坐: 阿彌陀佛, 阿彌陀佛...

[00:27] 但是如果你當真的, 你會這樣 (痛苦氣憤). 請問那個是真的還是假的? 暫時的! 那個女人是他前世的太太, 你還是侵占人家的嘞!

[00:42] 請問你現在手上那張鈔票, 別人有沒有用過? 它還是可以用就好了.

[00:48] 所以曾經有一個女人啊: "師父, 我老公有外遇, 很多..." 我說: "有差嗎? 共用, 有差嗎? 不然你鈔票怎麼辦呢? 你還不是照用! 那只是一個感覺."

[01:05] 各位女人, 我老實講, 你知道不知道而已, 哪一個男人外面沒外遇? 各位男人講老實話, 你知道不知道而已啊.

[01:16] 所以, 當作不知道就 OK 了, 當假的看 OK 了.
```