---
title: vibe coding 自動擷取 chrome 圖片
date: 2026-01-25 15:40:17
tags:
---
&nbsp;
<!-- more -->

最近遇到一個有一堆圖檔在網頁上, 需要手動下載, 想說能否讓他自動翻頁然後拍下來所以搞了這個 = . =

`chrome://extensions/` => `開發人員模式` => `載入未封裝項目`

下載完後執行 python convert.py

manifest.json
```
{
  "manifest_version": 3,
  "name": "自動按鍵與截圖工具 V2",
  "version": "2.0",
  "permissions": [
    "debugger",
    "tabs",
    "activeTab",
    "downloads"
  ],
  "action": {
    "default_popup": "popup.html"
  }
}
```


popup.js
```
let timer = null;
let count = 1;

document.getElementById('start').onclick = async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab) return;
    const tabId = tab.id;

    // --- 第一步：防錯處理，先強制斷開可能存在的舊連接 ---
    try {
        await chrome.debugger.detach({ tabId });
    } catch (e) {
        // 如果原本沒連接，這會報錯，我們直接忽略它
    }

    // --- 第二步：重新附加 Debugger ---
    chrome.debugger.attach({ tabId }, "1.3", () => {
        if (chrome.runtime.lastError) {
            alert("啟動失敗！請檢查是否正開啟著 F12 開發者工具。如果是，請先關閉它。");
            return;
        }

        startAutomation(tabId);
    });
};

function startAutomation(tabId) {
    count = 1;
    updateStatus(`執行中... (第 ${count} 張)`);

    // 設定 2 秒一次的循環 (2000 毫秒)
    timer = setInterval(() => {
        // 1. 模擬物理按鍵 ArrowRight (按下與放開)
        chrome.debugger.sendCommand({ tabId }, "Input.dispatchKeyEvent", {
            type: "keyDown", windowsVirtualKeyCode: 39, nativeVirtualKeyCode: 39, key: "ArrowRight"
        });
        chrome.debugger.sendCommand({ tabId }, "Input.dispatchKeyEvent", {
            type: "keyUp", windowsVirtualKeyCode: 39, nativeVirtualKeyCode: 39, key: "ArrowRight"
        });

        // 2. 延遲 500ms 截圖（給網頁一點點渲染時間）
        setTimeout(() => {
            chrome.tabs.captureVisibleTab(null, { format: "png" }, (dataUrl) => {
                if (dataUrl) {
                    const fileName = `auto_shot_${String(count).padStart(3, '0')}.png`;
                    chrome.downloads.download({
                        url: dataUrl,
                        filename: fileName
                    });
                    count++;
                    updateStatus(`執行中... (第 ${count} 張)`);
                }
            });
        }, 500);

    }, 2000); // 這裡設定為 2000 毫秒 = 2 秒
}

document.getElementById('stop').onclick = () => {
    if (timer) {
        clearInterval(timer);
        chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
            if (tab) chrome.debugger.detach({ tabId: tab.id });
        });
        updateStatus("已停止執行");
    }
};

function updateStatus(msg) {
    document.getElementById('status').innerText = msg;
}
```

popup.html
```
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { width: 200px; padding: 15px; font-family: 'Segoe UI', sans-serif; }
    button { width: 100%; padding: 10px; margin: 5px 0; cursor: pointer; border: none; border-radius: 4px; font-weight: bold; }
    #start { background-color: #28a745; color: white; }
    #stop { background-color: #dc3545; color: white; }
    #status { margin-top: 10px; font-size: 13px; text-align: center; color: #555; }
    .note { font-size: 11px; color: #888; margin-top: 10px; border-top: 1px solid #eee; padding-top: 5px; }
  </style>
</head>
<body>
  <h3>截圖工具 (2秒/次)</h3>
  <button id="start">開始自動化</button>
  <button id="stop">停止</button>
  <div id="status">狀態：待機中</div>
  <div class="note">注意：請先關閉 F12 視窗</div>
  <script src="popup.js"></script>
</body>
</html>
```



convert.py
```
import os
import re
from PIL import Image

# 1. 設定路徑
folder_name = 'imgs'
output_pdf = 'sharp_screenshots.pdf'

def natural_key(string_):
    """ 確保 1.png, 2.png, 10.png 順序正確 """
    return [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', string_)]

def combine_to_sharp_pdf():
    if not os.path.exists(folder_name):
        print(f"錯誤：找不到 '{folder_name}' 資料夾")
        return

    # 2. 抓取並排序檔案
    files = [f for f in os.listdir(folder_name) if f.lower().endswith('.png')]
    files.sort(key=natural_key)

    if not files:
        print("資料夾內沒圖！")
        return

    print(f"準備合成 {len(files)} 張高畫質圖片...")

    image_objects = []
    
    # 3. 讀取第一張圖並獲取其原始尺寸
    first_img_path = os.path.join(folder_name, files[0])
    first_img = Image.open(first_img_path).convert('RGB')
    
    # 獲取原始尺寸，這對於保持清晰度很重要
    width, height = first_img.size

    # 4. 讀取後續圖片
    for filename in files[1:]:
        img_path = os.path.join(folder_name, filename)
        img = Image.open(img_path).convert('RGB')
        image_objects.append(img)
        print(f"已排隊: {filename}")

    # 5. 儲存 PDF (關鍵優化區)
    # 我們設定 resolution 為 144 (或更高)，這會告訴閱讀器這張圖很精細
    # 並且不進行任何縮放優化
    first_img.save(
        output_pdf,
        save_all=True,
        append_images=image_objects,
        resolution=144.0,  # 強制設定解析度，避免閱讀器自動模糊
        quality=100,       # 雖然 PNG 是無損，但這能確保封裝品質
        optimize=False     # 關閉優化以保持原始數據
    )

    print(f"\n--- 合成完成！ ---")
    print(f"清晰版 PDF 已生成：{os.path.abspath(output_pdf)}")
    print(f"原始尺寸：{width}x{height} 像素")

if __name__ == "__main__":
    combine_to_sharp_pdf()
```
