---
title: python 進位轉換
date: 2026-01-24 10:00:21
tags: python
---
&nbsp;
<!-- more -->

十進位轉二進位

26 / 2 = 13 remainder:0
13 / 2 = 6 remainder:1
6 / 2 = 3 remainder:0
3 / 2 = 1 remainder:1
1 / 2 = 0 remainder:1
result: 11010

```
from collections import deque
def decimal2bin(num : int) -> str:
    base = 2
    ans = deque([])

    while True:
        print(f"{num} / {base} = {(num // base)}")
        remainder = num % base
        ans.appendleft(remainder)
        num = num // base
        if num == 0:
            break

    result = "".join(map(str, ans))
    print(f"result: {result}")
    
    return result


decimal2bin(26)
```

二進位轉十進位

s:0 current:0 ans:0
s:1 current:2 ans:2
s:0 current:0 ans:2
s:1 current:8 ans:10
s:1 current:16 ans:26

```
def bin2decimal(bin: str) -> int:
    power = 0
    ans = 0
    for s in bin[::-1]:
        current = int(s) * (2**power)
        print(f"s:{s} current:{current}")
        ans += current
        power += 1
    return ans

bin2decimal("11010")
```
