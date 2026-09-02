---
title: openclaw cron job
date: 2026-03-10 00:50:21
tags: openclaw
---
&nbsp;
<!-- more -->


<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/R2r9IkUyizM" 
title="openclaw cron job" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>


如果有設定 telegram 他預設好像就會自動傳送到 telegram
不過我模型笨笨的, 沒有一次成功
cron 設定可以到這個網站比較好理解
https://crontab.guru/

```
cd ~
mkdir food
cd food

touch 龍蝦三爭霸.txt
vim 龍蝦三爭霸.txt

https://youtu.be/6ms9_MoRNRw?t=912
https://youtu.be/8ows7_hXhck?t=834
https://youtu.be/CMfgTUix7OY?t=904



# 新增工作
openclaw cron add \
  --name "龍蝦三爭霸" \
  --cron "* * * * *" \
  --message "把 "~/food/龍蝦三爭霸.txt" 內的任一條網址隨機傳給我"

# 印出所有工作  
openclaw cron list

# 刪除
openclaw cron rm 2a4d62a2-ae6f-xxxx-xxxx-63f5b448xxxx
```
