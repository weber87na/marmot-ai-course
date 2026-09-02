---
title: opencode 筆記
date: 2026-01-30 11:30:32
tags: 
---
&nbsp;
<!-- more -->

跟風看看 opencode 短短兩天就把之前儲值的 OpenAI 額度全花光光

網路上看到這個 [opencode-antigravity-auth](https://github.com/NoeFabris/opencode-antigravity-auth) plugin 可以免費繼續玩 opencode

安裝很簡單只要無腦執行就搞定了, 然後執行 `/connect` 連線他會跳出一個 oauth google 認證, 做完就收工
```
Install the opencode-antigravity-auth plugin and add the Antigravity model definitions to ~/.config/opencode/opencode.json by following: https://raw.githubusercontent.com/NoeFabris/opencode-antigravity-auth/dev/README.md
```

今天早上想搞繼續搞 [肥鼠 TD](https://codepen.io/weber87na/full/JoKMxPE) 結果 opencode 馬上噴這個 bug

This version of Antigravity is no longer supported. Please update to receive the latest features

看到社區哀鴻遍野, 後來發現只要到 `C:\Users\yourname\AppData\Roaming\opencode` 修改 `antigravity-accounts.json`
找到 `userAgent` 把本來的版本號 `1.15.x` 改成 `1.15.8` 就可以用了
大概長這樣
```
{
  "version": 3,
  "accounts": [
    {
      "email": "xxx@gmail.com",
      "refreshToken": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "addedAt": 12345,
      "lastUsed": 12345,
      "enabled": true,
      "rateLimitResetTimes": {
        "gemini-cli:gemini-3-flash-preview": 123444445,
        "gemini-antigravity:antigravity-gemini-3-pro": 123456.4026
      },
      "fingerprint": {
        "deviceId": "xxxxxxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxxx",
        "sessionToken": "xxxxxxxxxxxxxxxxxxxx",
        "userAgent": "antigravity/1.15.8 win32/x64",
        "apiClient": "google-cloud-sdk vscode_cloudshelleditor/0.1",
        "clientMetadata": {
          "ideType": "IDE_UNSPECIFIED",
          "platform": "WINDOWS",
          "pluginType": "GEMINI",
          "osVersion": "10.0.xxxx",
          "arch": "x64",
          "sqmId": "{xxxx-xxxx-xxxx-xxxx-xxxxx}"
        },
        "quotaUser": "device-xxxxxxxxxxxxxxxx",
        "createdAt": 12345678
      },
      "managedProjectId": "modified-tempest-xxx",
      "projectId": "modified-tempest-xxxx"
    }
  ],
  "activeIndex": 0,
  "activeIndexByFamily": {
    "claude": 0,
    "gemini": 0
  }
}
```
