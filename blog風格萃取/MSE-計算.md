---
title: MSE 計算
date: 2026-02-25 13:04:14
mathjax: true
tags:
---
&nbsp;
<!-- more -->

MSE (Mean Squared Error，均方誤差) 是機器學習與統計學中，衡量「預測值」與「真實值」之間差異最常用的指標。

簡單來說，它告訴你：「你的模型預測得有多準？」，數值越小，代表預測越接近真實情況。

1. MSE 的核心用途
A. 作為損失函數 (Loss Function)
在訓練模型（如線性迴歸）時，MSE 被用來指導模型學習。透過「梯度下降法 (Gradient Descent)」，模型會不斷調整參數，目標就是讓 MSE 的值降到最低。

B. 衡量預測準確度
在測試階段，我們用 MSE 來評估模型的表現。它能將所有誤差加總並平均，給出一個量化的分數，方便我們比較不同模型（例如：模型 A 的 MSE 是 10，模型 B 是 5，則模型 B 較優）。

MES 計算

$$MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$


```
def mean_squared_error(y_true, y_hat):
    return np.mean(np.square(y_true - y_hat))


np.random.seed(42)
y = np.linspace(0, 10, 100)
y_hat = y + np.random.normal(0, 1, 100)

mean_squared_error(y, y_hat)
```
