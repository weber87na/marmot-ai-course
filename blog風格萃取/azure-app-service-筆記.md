---
title: azure app service 筆記
date: 2026-08-15 01:08:55
tags: azure
---
&nbsp;
<!-- more -->

好久沒寫 blog 了, 自從有 AI 後, 很多工作莫名其妙就做完了, 今天遇到比較陌生的 azure 環境還是筆記下

今天佈署 nodejs 網站在 azure 碰到的問題, 一直沒辦法正常佈署, 最大重點加上就過了 `allow-no-subscriptions: true`
問了問 AI 發現要改這個 CI/CD 設定

https://github.com/yourname/your_repo_name/blob/main/.github/workflows/main_xxx.yml

```
      - name: Login to Azure
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZUREAPPSERVICE_CLIENTID_XXX }}
          tenant-id: ${{ secrets.AZUREAPPSERVICE_TENANTID_OOO }}
          subscription-id: ${{ secrets.AZUREAPPSERVICE_SUBSCRIPTIONID_QQQ }}
          allow-no-subscriptions: true
```

另外 azure app service 的 ssh 跟普通 ssh 也不太一樣, 需要使用 azure cli

安裝
```
winget install --exact --id Microsoft.AzureCLI
```

登入非常噁心, 會開個 web ssh...
如果是學校的帳號要選學校的組織, 不然是進不去低
```
az login
az webapp ssh -g xxx -n xxx
```


還好有這種可以開 ssh 的方法, 不然用 web ssh
```
az webapp create-remote-connection `
  --resource-group xxx `
  --name xxx
```

成功後會顯示這樣, 此時這個 terminal 不要關閉
```
Verifying if app is running....
App is running. Trying to establish tunnel connection...
Opening tunnel on addr: 127.0.0.1
Opening tunnel on port: 56471
SSH is available { username: root, password: Docker! }
Enter a full SSH session with: ssh root@127.0.0.1 -m hmac-sha1 -p 56471
```

最後在另外一個 terminal 開啟就可以連線進去啦, 灑花 ~
```
🌹 ssh root@127.0.0.1 -m hmac-sha1 -p 56471
The authenticity of host '[127.0.0.1]:56471 ([127.0.0.1]:56471)' can't be established.
ED25519 key fingerprint is SHA256:1234abcd.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[127.0.0.1]:56471' (ED25519) to the list of known hosts.
root@127.0.0.1's password:
Permission denied, please try again.
root@127.0.0.1's password:
Last login: Fri Aug 14 16:56:17 2026 from 123.456.129.3
   _____
  /  _  \ __________ _________   ____
 /  /_\  \\___   /  |  \_  __ \_/ __ \
/    |    \/    /|  |  /|  | \/\  ___/
\____|__  /_____ \____/ |__|    \___  >
        \/      \/                  \/
A P P   S E R V I C E   O N   L I N U X

Documentation    : http://aka.ms/webapp-linux
NodeJS quickstart: https://aka.ms/node-qs
NodeJS Version   : v24.15.0
Instance Name    : 10-30-0-11
Instance Id      : 1234567c5c33ddxxxxxxxxxxxx30958a08e7979805123d99794b1ec9xxx
```

接著可以看看網站放在哪, 探索下是放在 `/home/site/wwwroot` 底下
```
root@123abcdefg:/home/site/wwwroot# ls
README.md          example-images     node_modules         oryx-manifest.toml  package.json  server.js
_del_node_modules  hostingstart.html  node_modules.tar.gz  package-lock.json   public        styles.js
```
