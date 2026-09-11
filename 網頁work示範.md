## work 範例
開啟網頁版 `work` 功能. 在手機上也可以這樣操作. 

```text
上網搜尋土撥鼠和河狸的圖片, 各 50 張, 並分成兩個資料夾, 供我做機器學習真假辨識訓練, 圖片大小需一致.
```

```text
搜尋十篇與土撥鼠演算法或仿生元啟發式演算法有關的論文, 下載後打包成 ZIP 檔給我.
```

接著談談使用 `work` 把論文 meeting 內容給產生字幕及重點摘要的案例, 因為 `work` 他是在雲端開啟一台虛擬機, 這裡面可以下載東西, 執行指令

以下為 prompt

```text
使用 whisper 產生這個影片 https://www.youtube.com/watch?v=1Lgs8PwB5aM  的字幕 SRT 格式 , 品質設定最高, 完成後執行校對錯字及用詞工作
如果有出現人名或是相近的音使用以下進行校對 
俊宇 / 俊玉 / 駿裕 / 均勻 ➡️ 駿寓 
宜甄 / 宜真 / 怡蓁 / 一針 ➡️ 宜禎 
宇宙 / 偽咒 / 偉洲 / 尾奏 ➡️ 瑋宙 
嘉豪 / 加好 ➡️ 家豪 
莊程 / 莊成 ➡️ 莊丞 
錦成 / 競撐 ➡️ 錦丞 
 
做好後產生類似這樣的摘要報告 md 給我 
 
## 會議重點摘要 
 
這次會議主要在說明**碩士論文的基本架構、每位同學的研究方向，以及下次要完成的文獻蒐集作業**。老師強調，AI 可以協助寫論文，但前提是學生必須先找到可靠文獻，並了解文獻內容，不能完全依賴 AI 自動生成。 
 
### 一、論文基本架構 
 
碩士論文大多分成五章： 
 
1. **緒論**：研究背景、研究動機、研究目的與問題。 
2. **文獻探討**：介紹研究主題、相關理論及研究構面。 
3. **研究方法**：研究架構、研究假說、操作型定義、研究對象及資料分析方法。 
4. **研究結果**：樣本描述、平均數與標準差、信效度分析、模型分析及假說檢定。 
5. **結論與建議**：研究結論、學術貢獻、實務貢獻及後續研究建議。 
 
論文通常約 **70～80頁**，但老師認為頁數不是重點，內容清楚、邏輯完整比較重要。 
 
--- 
 
## 二、不同研究方法的安排 
 
依照每位同學的題目，大致分成三種研究方式： 
 
* **問卷研究＋PLS分析**：宜禎、莊臣。 
* **實驗法＋ANOVA或T檢定**：家豪、駿寓。 
* **系統開發＋使用者成效評估**：瑋宙。 
 
所有人的研究原則上都會有研究問題或假說，例如探討「某個因素是否會影響另一個因素」。 
 
--- 
 
## 三、每位同學的論文方向 
 
### 1. 莊臣：台糖ESG與品牌信任 
 
研究方向為： 
 
> 探討台糖的產品品質與ESG表現，如何影響品牌信任，並進一步影響食品安全認知及購買意願。 
 
可能使用： 
 
* 訊號理論 
* 信任理論 
* 產品品質 
* ESG 
* 品牌信任 
* 食品安全認知 
* 購買意願 
 
老師認為只研究ESG可能過於簡單，也可能出現結果不顯著，因此加入「產品品質」構面。 
 
### 2. 宜禎：自動倉儲對員工的影響 
 
研究場域是物流中心或自動倉儲，探討導入AI、自動化設備後，對員工心理與工作的影響。 
 
可能包含兩條路徑： 
 
* **正向路徑**：提升工作效率、能力增強，進而提升工作滿意度。 
* **負向路徑**：產生工作不安全感，進而降低工作滿意度。 
 
老師建議暫時不要使用過度負面的「離職意圖」，可改以「工作滿意度」作為結果變項。自主性是否適合，也要根據實際工作場域與文獻判斷。 
 
### 3. 家豪：AI影片與人工影片的廣告效果 
 
研究主題以木質地板等高涉入產品為例，比較： 
 
* AI生成影片 
* 人工製作影片 
 
可能評估： 
 
* 廣告真實性 
* 感知風險 
* 信任 
* 購買意願 
 
實驗影片可以分成： 
 
* 功能性影片：介紹材質、功能及規格。 
* 情感性影片：透過情境與故事引發情感。 
 
老師推測功能性影片的AI與人工差異可能較小，情感性影片的差異可能較明顯。理論可使用「來源可信度理論」。 
 
### 4. 駿寓：不同電腦組裝推薦來源 
 
比較不同推薦來源對消費者決策的影響，例如： 
 
* ChatGPT推薦 
* 電腦平台AI組裝助手 
* 門市專業人員推薦 
 
可能評估： 
 
* 推薦品質 
* 信任度 
* 決策信心 
* 購買意願 
 
不一定要真正開發三套推薦系統，可以使用「情境劇本」呈現不同推薦結果，再請受測者進行評估。也可以簡化成AI組裝助手與門市人員兩組比較。 
 
### 5. 瑋宙：商業用Multi-Agent AI系統 
 
研究重點是先開發一套**商業用途的Multi-Agent AI Agent**，再讓業者實際使用並評估成效。 
 
老師提出的主要方向是「社群行銷AI Agent」，系統可依序完成： 
 
1. 詢問企業、產品或服務內容。 
2. 分析目標受眾是B2B或B2C。 
3. 分析產業及行銷情境。 
4. 規劃社群貼文主題。 
5. 生成貼文文字。 
6. 產生Hashtag。 
7. 生成圖片或影音。 
8. 安排貼文時間與排程。 
9. 提供完整的行銷內容方案。 
 
可能的論文題目為： 
 
> 多代理人AI輔助數位行銷任務之系統設計與成效評估 
 
或： 
 
> AI Agents對數位行銷任務成效之影響 
 
老師強調不能只做單一功能，例如只生成一篇貼文，而要做成能夠完成多個步驟的 **Multi-Agent系統**。系統完成後，再找業者試用，評估系統品質、實用性、效率或使用意願。 
 
--- 
 
## 四、下次作業：蒐集30篇相關文獻 
 
每位同學需依照自己的論文題目，蒐集 **30篇相關文獻**。 
 
要求如下： 
 
* 期刊論文、碩博士論文、中文或英文文獻皆可。 
* 盡量取得全文PDF。 
* 沒有全文時，可以保留網頁或論文連結。 
* 不可全部使用舊文獻。 
* 至少一半應為近年文獻，建議以 **2020年以後**為主。 
* 經典理論可以使用較舊的原始文獻，例如訊號理論的早期文獻。 
* 檔名至少應包含「年份＋論文題目」，有能力時可再加入作者。 
* 將30篇文獻放入自己的作業目錄。 
* 同時匯入NotebookLM，協助閱讀、分類及摘要。 
* 每位同學必須能簡單說明這30篇文獻分別在研究什麼。 
 
老師特別強調： 
 
> 找到30篇並不是完成作業，必須真正了解每篇文獻的研究主題、變項、理論與結果。 
 
--- 
 
## 五、文獻搜尋方式 
 
老師示範兩種主要方法。 
 
### NotebookLM 
 
可以使用Fast Research輸入論文題目，讓系統搜尋相關資料，再挑選有用的來源匯入筆記本。 
 
優點： 
 
* 可以快速找出論文與網頁資料。 
* 上傳PDF後可協助摘要。 
* 可以針對多篇文獻提問。 
* 可以依據上傳內容撰寫初稿。 
 
缺點： 
 
* 搜尋結果不一定都是正式論文。 
* 有些網站或最新文章無法直接匯入。 
* 輸出的APA引用格式可能需要再次修正。 
 
### ChatGPT＋Google Scholar 
 
可請ChatGPT尋找近五年的SCI或SSCI文章，再將論文名稱放到Google Scholar查證。 
 
原因是ChatGPT可能產生不存在的論文，因此每一篇都必須確認： 
 
* 論文是否真的存在。 
* 作者與年份是否正確。 
* 是否能取得全文。 
* 內容是否與研究題目相關。 
 
--- 
 
## 六、使用AI撰寫論文的原則 
 
可使用的工具包括： 
 
* ChatGPT 
* NotebookLM 
* Codex 
 
老師認為AI可以協助撰寫緒論、文獻探討、研究方法、資料分析及結論，但必須先提供足夠且正確的文獻。 
 
核心概念是： 
 
> 文獻就是「原料」，AI只是負責將原料整理成論文。 
 
如果沒有提供文獻，AI仍然可以寫出內容，但可能會： 
 
* 虛構引用來源。 
* 使用錯誤的研究結果。 
* 內容看似合理但沒有證據。 
* 過度加入不需要的章節，例如名詞解釋。 
* 只集中在少數構面，忽略完整研究架構。 
 
因此AI產出的內容必須人工檢查、刪減及修正。 
 
--- 
 
## 七、重要時間與繳交方式 
 
* **下次Meeting：2026年8月12日晚上8點** 
* 每次作業都要放進自己的個人目錄。 
* 下次主要檢查每人蒐集的30篇文獻。 
* 開學後Meeting時間可能由星期三調整至星期二。 
* 老師希望有一位同學在會議前一天提醒大家及老師。 
 
## 一句話總結 
 
這次會議的核心任務是：**先確定研究方向，再找到30篇真正相關且以近年為主的文獻，了解每篇文獻後，才利用ChatGPT、NotebookLM或Codex協助撰寫論文。**
```


## work 其他用法
如果你是開發人員或想要替程式加點功能, 也可以直接用 `work` 來做. 搭配 GitHub 的 GitHub Actions, 可以快速建立線上編譯環境.

像我自己是 `Vim` 邪教的信徒. 今天最後面介紹的後端程式會使用 `SQLite`, 我們會用到 `SQLiteBrowser` 這個工具, 但它不支援 `Vim` 這類功能, 所以我請它增加.

尤其點數燒不完的時候, 用手機丟下去做, 人跑去睡覺最適合.

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