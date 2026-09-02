---
title: variance 筆記
date: 2026-01-27 13:30:57
mathjax: true
tags:
---
&nbsp;
<!-- more -->

母體方差 (Population Variance)當你擁有所有對象的數據時（例如：全班所有人的身高），使用這個公式。
通常用希臘字母 $\sigma^2$ 表示。

$$\sigma^2 = \frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N}$$

$N$：總資料筆數。
$x_i$：第 $i$ 個資料點。
$\mu$：母體平均值。

假設有一組 5 個學生的成績：$70, 80, 85, 90, 100$。我們來算這組數據的 母體方差 ($\sigma^2$)。

第一步：計算平均值 ($\mu$)
先把所有人加起來，除以總人數。
$$\mu = \frac{70 + 80 + 85 + 90 + 100}{5} = \frac{425}{5} = \mathbf{85}$$

第二步：計算「每個點與平均的距離」並「平方」

| 原始分數 ($x_i$) | 與平均的距離 ($x_i - \mu$) | 距離的平方 ($(x_i - \mu)^2$) |
| :--- | :--- | :--- |
| **70** | $70 - 85 = -15$ | $225$ |
| **80** | $80 - 85 = -5$ | $25$ |
| **85** | $85 - 85 = 0$ | $0$ |
| **90** | $90 - 85 = 5$ | $25$ |
| **100** | $100 - 85 = 15$ | $225$ |
| **總和 ($\sum$)** | **0** | **500** |


第三步：把平方後的結果全部加起來 ($\sum$)
$$\sum = 225 + 25 + 0 + 25 + 225 = \mathbf{500}$$


第四步：除以總人數 ($N$)
$$\sigma^2 = \frac{500}{5} = \mathbf{100}$$

```
score = [70, 80, 85, 90, 100]

mu = sum(score) / len(score)
total = 0
for x in score:
    total += (x - mu) ** 2

ans = total / len(score)
```

標準差

$$\sigma = \sqrt{\frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N}}$$

```
score = [70, 80, 85, 90, 100]

# 你剛才算的方差
mu = sum(score) / len(score)
total = 0
for x in score:
    total += (x - mu) ** 2
ans_variance = total / len(score)

# 計算標準差 (Standard Deviation)
ans_sd = ans_variance ** 0.5  # 開根號

print(f"方差: {ans_variance}")
print(f"標準差: {ans_sd}") # 結果會是 10.0
```
