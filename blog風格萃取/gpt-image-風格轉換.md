---
title: gpt-image-風格轉換
date: 2026-05-11 03:48:40
tags:
---
&nbsp;
<!-- more -->

半夜收到教授的信, 要我嘗試以下文章的東東, 順手筆記下

最後用 vibe coding 做出 AR 帶看房風格轉換的[有趣咚咚](https://vickys-ai-room-restyle.vercel.app/?openExternalBrowser=1)

用 agent 之後越來越懶了, 幾乎已經變成指揮 agent 來 coding, 以前數週能做到的事現在幾天甚至幾小時就能完成

有前途堪慮的 fu XD

[原文網址](https://blog.jbs.co.jp/entry/2025/05/20/134318)

Azure OpenAI Service 中的 GPT-Image-1 詳細解析

針對在 Azure OpenAI Service 中提供試用版的圖像生成模型「GPT-Image-1」，本文將從概要到使用方式，進行詳細說明。

## 摘要
GPT-Image-1 是 Azure OpenAI Service 所提供的最新型的圖像生成 AI 模型。

正如其名，這是屬於 GPT 系列的第一款專門用於處理圖像的模型。它可視為 OpenAI 之前推出的 DALL·E 系列的後繼者。

### 特徵與功能
輸入文字提示後，系統會根據該提示生成相應的原始圖像。

在具備圖像生成能力的同時，還進一步提升了對於複雜、詳細指令的響應能力。無論是複雜冗長的提示語，都能被精準理解並轉化為圖像；即便沒有示例，也能展現出高度的表現力。

透過"圖像到圖像"功能，可對現有圖像進行編輯或轉換（如改變風格、生成各種變體）。

經過優化，能夠精確地將文字呈現在圖像中。

### 2025 年 5 月時點下所支援的輸出尺寸
GPT-Image-1 至少會以 1024×1024 像素以上的分辨率來生成圖像。

1024×1024（正方形）
1024×1536（縱長）
1536×1024（橫長）

### 安全性・內容過濾器
Azure OpenAI 的 GPT-Image-1 內建了 OpenAI 的安全防護機制。

與現有模型一樣，對於所生成或編輯的圖像內容，也會進行嚴格的過濾與監控。

## Azure OpenAI 的提供方式 – 使用方法與地區範圍
這是作為 Azure OpenAI 服務的限時公開預覽版而提供的。

因此，使用該服務必須事先申請。截至 2025 年 5 月，若想在 Azure 上使用 GPT-Image-1，必須先向 Microsoft 提出申請並獲得批准。

申請連結：https://aka.ms/oai/gptimage1access

### 支持的地區/區域
截至 2025 年 5 月，能夠部署 GPT-Image-1 的地區十分有限。

僅在西美 3 和阿聯酋北部這兩個地區，才支援全球標準格式的部署方式。

因此，如果想使用 GPT-Image-1，就需要在相應的區域中創建 Azure OpenAI 資源。請注意，日本地區目前尚不支持該功能。

### API Version  API 版本
在撰寫本文時，所使用的 API 版本為預覽版 2025-04-01-preview 。

此 API 版本包含用於圖像生成的各個端點，因此必須必須指定這些端點。

### 使用費用
可能是因為正在預覽中，目前官方頁面上沒有明確的說明。

供參考之用，以下是 OpenAI 的 API 費用相關連結。

https://openai.com/ja-JP/api/pricing/

## 部署方法
一旦訂閱申請獲得批准，即可開始使用。

轉移到 Azure OpenAI Service 後，即可像部署普通模型一樣進行操作。

在預覽模式下，可將轉速設定為 2K（6RPM）。若需要短時間內生成大量圖像，此預設值就不夠用了。因此，目前必須根據需求聯絡 Azure 客服，申請解除此限制。


## 主要功能與 API 的使用方式
這些就是 GPT-Image-1 所提供的主要功能。

從文本生成圖像（Text-to-Image）

畫像編輯（上色/繪製）

圖像轉換（Image-to-Image）

將其分為這三類，並說明對應的 API 端點的使用方式。

將使用以下的套件。

``` python
from openai import AzureOpenAI
import os
import json
import base64
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image, ImageDraw

API_KEY = ""
RESOURCE_ENDPOINT = "https://<AOAIリソース名>.openai.azure.com/"

model_name = "gpt-image-1" #デプロイしたモデル名
file_name1 = "./panda1.png"
file_name2 = "./panda2.png"
file_name3 = "./panda3.png"
file_name4 = "./panda4.png"

client = AzureOpenAI(
    api_key=API_KEY,
    azure_endpoint=RESOURCE_ENDPOINT,
    api_version="2025-04-01-preview"
)
```

在目前階段，若使用 Azure OpenAI 的 API，則在 2 和 3 那個圖像轉文字的處理過程中會出現錯誤。因此，我們會在 import requests 中說明相關的操作步驟。

### 從文本生成圖像（Text-to-Image）
從文本生成圖像是最基本的應用方式。當使用者提供文本形式的指令後，GPT-Image-1 模型會解讀這些指令並生成新的圖像。

``` python
prompt_base = """
パンダの画像を書いてみて
"""
response = client.images.generate(
    model = model_name,
    prompt=prompt_base,
    size="1024x1024",
    quality="low"
)
image_base64 = response.data[0].b64_json
image_bytes = base64.b64decode(image_base64)
with open(file_name1, "wb") as f:
    f.write(image_bytes)
```

### 圖像轉換（透過 Image-to-Image 技術生成各種變體）
圖像轉換（Image-to-Image）是一種以輸入的原始圖像為基礎，再根據提示詞來生成新圖像的功能。這些新圖像可以是原始圖像的各種變體或具有不同風格的圖像。

這與上一項的圖像編輯類似，但不同之處在於，不需要特別指定遮罩區域，就能改變整張圖像的氣氛，或是將原圖中的物體替換成不同的樣式。

在 GPT-Image-1 中，官方並沒有明確指定用於“圖像轉換”的 API 端點。不過，一般而言，只要直接使用圖像編輯 API，即可實現圖像轉換的功能。

也就是說，將原始圖像放入「image」欄位中，不必指定「mask」（或者，即使指定全透明區域的「mask」也沒有關係）。然後在「prompt」欄位中輸入想要轉換成的內容，即可提交請求。

模型在參考整張原始圖像的基礎上，根據提示詞生成新的圖像。

``` python
import requests
url = "https://<AOAIリソース名>.openai.azure.com/openai/deployments/<gpt-image-1デプロイ名>/images/edits?api-version=2025-04-01-preview"
headers = {"api-key": "<API_KEY>"}
data = {
    "prompt": "アニメ調にしたうえで、このパンダを警察風にして",
    "model": 'gpt-image-1',
    "size": "1024x1024",
    "n": "1"
}
files = {"image": open(file_name1, "rb")}

response = requests.post(url, headers=headers, data=data, files=files)

json_data = response.json()
if not "data" in json_data.keys():
    print(json_data)
b64_image = json_data["data"][0]["b64_json"]
image_data = base64.b64decode(b64_image)
with open(file_name2, "wb") as f:
    f.write(image_data)
```

在圖像轉換的情況下，基本的輸入規格（圖像以 Base64 格式表示，大小與原始圖像相同或為指定值等）也與編輯 API 相同。


根據提示詞的不同，原始圖像的變化程度也會有所差異。如果希望保留原始圖像的樣貌，只做些微小的修改，可以使用「稍微修改一下～」這樣的表述；如果想要大幅改變圖像，則可以說「以完全不同的～風格重新繪製」。

另外，如果在圖像中加入文字，則會是如下所示的樣子。

```
data = {
    "prompt": "「特殊詐欺には気を付けよう」という文字を入れて、啓発ポスター風にして",
    "model": 'gpt-image-1',
    "size": "1024x1024",
    "n": "1"
}
files = {"image": open(file_name2, "rb")}

response = requests.post(url, headers=headers, data=data, files=files)
json_data = response.json()
if not "data" in json_data.keys():
    print(json_data)
b64_image = json_data["data"][0]["b64_json"]
image_data = base64.b64decode(b64_image)
with open(file_name3, "wb") as f:
    f.write(image_data)
```

有部分的文字顯示不完整。第二次之後，文字就能正常顯示了，因此似乎有時需要重新生成頁面。

### 圖像編輯（透過繪圖和遮罩進行編輯）
圖像編輯是一種對現有圖像施加特定指令、並對其中部分內容進行合成性修改的功能。

GPT-Image-1 可以接收圖像輸入和遮罩圖像，並根據給定的提示，修改原始圖像中指定的區域。

首先，要製作用於口罩的圖像。

```
ef create_inverse_circular_mask_image(
    out_path: str | Path,
    size: tuple[int, int],
    ratio: float = 0.25  # 半径 = 短辺 × ratio
) -> None:
    """
    外側だけ白、中心の円は透明なマスク画像（PNG）を生成。

    Parameters
    ----------
    out_path : str | Path
        出力PNG画像のパス
    size : tuple[int, int]
        出力画像のサイズ (width, height)
    ratio : float, default 0.25
        円の半径を「短辺 × ratio」で決定（0.0〜1.0）
    """
    w, h = size
    r = int(min(w, h) * ratio)
    mask = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(mask)
    cx, cy = w // 2, h // 2
    bbox = (cx - r, cy - r, cx + r, cy + r)
    # 中心の円だけ透明にする
    draw.ellipse(bbox, fill=(0, 0, 0, 0))
    mask.save(out_path)

create_inverse_circular_mask_image("mask.png", size=(1024, 1024), ratio=0.3)
```

使用口罩圖像和剛才的熊貓圖像，將角色替換成狗吧。


```
data = {
    "prompt": "マスクした部分をアニメの犬に置き換えて",
    "model": 'gpt-image-1',
    "size": "1024x1024",
    "n": "1"
}
files = {
    "image": (file_name3, open(file_name3, "rb"), "image/png"),
    "mask": ("mask.png", open("./mask.png", "rb"), "image/png")
}

response = requests.post(url, headers=headers, data=data, files=files)
```

熊貓的臉部被換成了狗的臉部。形象如下所示。

將轉換前後的圖像進行比較後，可以發現那些被切斷的文字又重新顯現出來了，而耳朵的形狀也變成了狗的耳朵。為了讓整體看起來更協調，inpaint 範圍之外的部分也會受到一些影響。

## 總結
本文詳細說明瞭 Azure OpenAI Service 在限時預覽階段的圖像生成模型「GPT-Image-1」的概要及實際使用方法。

GPT-Image-1 擁有出色的圖像生成能力，能夠運用各種提示詞或現有的圖像進行編輯。這是一個具有巨大發展潛力的圖像生成 AI 模型。隨著其應用的不斷拓展，地區限制和 TPM 相關的規定也有可能發生變化。

歡迎大家也試著運用這個新的圖像生成模型吧。


