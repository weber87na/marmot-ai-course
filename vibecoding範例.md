## 適合 vibe coding 發想 idea 的網站

以下是幾個 vibe coding 酷炫網站的優質素材, 之前抽籤也有用到其中一個

因為 AI 更適合 one shot, few shot, 所以給他範例原始碼請他做成自己心中的樣子往往成功率更高

可以在 codepen 打上創意的關鍵字 ex:parallax, 3d ...

https://codepen.io/

https://codepen.io/shannonmoeller/pen/MWpWJGB

https://www.awwwards.com/

https://threejs.org/examples/

https://www.originkit.dev/


## QR Code

```text
你做一個純前端的網站, 整個網站只用原生 html css js
我要能夠自訂網址, 貼上後可以產生 QR Code
另外還要可以上傳 Logo
產生的 QR Code 希望可以有
500x500 800x800 1000x1000
Logo 大小跟容錯率也分為三種
做完 QR Code 要有按鈕可以讓我下載
另外還需要有按鈕可以清除我上傳的網址 Logo 及 QR Code
整體風格使用歪歪扭扭的線條純黑白, 看起來像是五歲小孩做的網頁
除了電腦版也要可以支援手機, 所以必須把 RWD 考慮進去
```


## todo list

`Sites` 這個技能可以完全無痛幫你佈署自己的網站, 馬上就能看到成品

luna 推理強度最強
```text
使用純 html css js 建立一個純前端的 todolist 網站, 風格為 win xp 風格
```


## 擲筊遊戲

擲筊遊戲, `sol` 推理強度最強

```text
使用 three.js 開發一個擲筊的遊戲 要能紀錄挑戰者最高連續聖杯次數 除了遊戲功能外還需要一個編輯擲筊材質的功能 要能套 uv 以及讓材質具有真實立體感 紋理感 使用者可以選擇不同的筊來進行遊戲, 系統名稱為通靈王, 畫面純黑, 繪製五種常見材質
```

## 佛珠

第一輪對話

```text
用純 html js css 搭配 three.js 建立一個佛珠客製化的系統, 首先要建立一個卡片頁面有很多材質可以選擇, 材質都是類似 vray 那種 demo 材質的畫面, 以單顆佛珠為單位, 先使用 [$imagegen](C:\Users\weberchang\\.codex\skills\\.system\imagegen\SKILL.md) 繪製五種木頭材質紋理, 琉璃, 翡翠, 玻璃, 不鏽鋼, 塑膠, 並且也要繪製 uv 讓佛珠看起來有凹凸效果, 我在這個卡片頁面點進去可以看到此佛珠的 demo, 另外製作一頁串接佛珠的頁面, 每顆佛珠可以使用不同材質, 目前先做比較小串的, 背景先使用純黑即可, 畫面上請勿有冗於文字

佛珠參考以下數量

- 佛珠顆數 36：是將 108 顆佛珠分為 3 分之 1 的便攜選擇，其功德與 108 顆佛珠相同。持誦 36 顆佛珠，方便隨身攜帶，隨時隨地精進修行。
- 佛珠顆數 27：代表二十七賢聖位，包含十八有學與九無學。
- 佛珠顆數 21：象徵十地、十波羅蜜、佛果等 21 位，是菩薩修行成就的階位。
- 佛珠顆數 18：代表十八界，即六根、六塵與六識。
- 佛珠顆數 14：代表觀世音菩薩的 14 種無畏功德。
- 佛珠顆數 12：象徵十二因緣，是佛教中解讀生死、因果、姻緣輪迴的理論。
```

請 AI 規劃
```
再規劃 26 種材質, 並且具有其特殊性, ex: 花崗岩, 隕石, 天珠等, 一樣使用 [$imagegen](C:\Users\weberchang\\.codex\skills\\.system\imagegen\SKILL.md) 來進行繪製, 並且建立 uv 把凹凸也規劃進去
```


## chrome extension 照妖鏡製作
chrome extension `luna` 推理強度最強
```text
[國立高雄科技大學](plugin://browser@openai-bundled?mention=tab-v1\&source=extension\&browserId=192ff825-7d69-4321-b34b-55b78464161b\&tabId=%5B%226c16cd0d-c02c-4d0a-b1c7-7073e551bf4f%22%2C%22202642561%22%5D\&title=%E5%9C%8B%E7%AB%8B%E9%AB%98%E9%9B%84%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%B8\&url=https%3A%2F%2Felearning.nkust.edu.tw%2Fmoocs%2F%23%2Flearning%2F10150867) 我在這個資料夾內已經有放置 [114](114/) [115](115/) 的同學名單 json 及照片
我想要做一個 chrome extension 顯示圖片在上面

這個網頁當切換到 "通訊錄" 這個頁籤時會去呼叫 ajax [https://elearning.nkust.edu.tw/api/v1/courses/10150867/AddressInfo](https://elearning.nkust.edu.tw/api/v1/courses/10150867/AddressInfo) 取得同學資訊, 顯示在畫面上, 可是目前幾乎不會有人去設定圖片, 所以他的頁面會像是 [參考畫面.png](參考畫面.png) 請你依照我給的照片還有已經有的名單進行核對, 把預設的頭像換成我給你的照片, 並且加上綽號在原本的資訊卡上, 讓我可以更清楚分辨誰是誰

注意除了這個課程之外, 其他課程也要可以套用到目前開發的功能

你使用 Manifest  V3 的版本, 可以參考官方文件 [https://developer.chrome.com/docs/extensions/reference/manifest?hl=zh-tw](https://developer.chrome.com/docs/extensions/reference/manifest?hl=zh-tw)
```