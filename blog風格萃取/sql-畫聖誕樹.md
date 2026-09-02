---
title: sql 畫聖誕樹
date: 2026-02-03 13:44:01
tags: sql
---
&nbsp;
<!-- more -->

<iframe 
    width="1235" 
    height="772" 
    src="https://www.youtube.com/embed/qp9ny-zJIbo"
    title="純 sql 畫聖誕樹 (無 AI)" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" 
    allowfullscreen>
</iframe>



快過年了, 剛看到老外在買春聯, 覺得很突兀, 加上旁邊有人在拆聖誕樹, 突然想到聖誕節做的 SQL 還沒上傳 XD

需要用以文字顯示才會有用


```sql
WITH TALLY(N) AS (
    SELECT  1 N
    UNION ALL
    SELECT 1 + N
    FROM Tally
    WHERE N < 9
)
SELECT REPLICATE(' ', (SELECT MAX(N) FROM TALLY) * 3 - N) + REPLICATE('*',N) + REPLICATE('*', N)
FROM TALLY
UNION ALL
SELECT REPLICATE(' ', (SELECT MAX(N) FROM TALLY) * 3 - N * 2)  + REPLICATE('*',N * 2) + REPLICATE('*', N * 2)
FROM TALLY
UNION ALL
SELECT REPLICATE(' ', (SELECT MAX(N) FROM TALLY) * 3 - N * 3)  + REPLICATE('*',N * 3) + REPLICATE('*', N * 3)
FROM TALLY
UNION ALL
SELECT REPLICATE(' ', (SELECT MAX(N) * 3 - 3 FROM TALLY))  + REPLICATE('*', 6 )
FROM TALLY

```

最後會長這樣 = w =
```
                          **
                         ****
                        ******
                       ********
                      **********
                     ************
                    **************
                   ****************
                  ******************
                         ****
                       ********
                     ************
                   ****************
                 ********************
               ************************
             ****************************
           ********************************
         ************************************
                        ******
                     ************
                  ******************
               ************************
            ******************************
         ************************************
      ******************************************
   ************************************************
******************************************************
                        ******
                        ******
                        ******
                        ******
                        ******
                        ******
                        ******
                        ******
                        ******
```
