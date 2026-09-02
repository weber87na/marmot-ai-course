---
title: Entropy 筆記
date: 2026-01-27 12:20:42
mathjax: true
tags:
---
&nbsp;
<!-- more -->

簡單來說，Entropy（熵） 是在衡量「驚訝程度」或「不確定性」，而 Cross Entropy（交叉熵） 則是在衡量「你的預測」跟「現實」之間差了多少。
我們可以把這兩個概念想像成在玩猜謎遊戲：

### Entropy

Entropy (資訊熵)：這件事有多難猜？Entropy 衡量的是一個系統內部的「混亂程度」或「資訊量」。
白話解釋： 如果一件事發生的機率是 100%（例如：太陽明天從東邊升起），那你完全不會感到驚訝，這件事的 Entropy 就是 0。
但如果一件事機率很隨機（例如：擲硬幣），你很不確定結果，Entropy 就會很高。
直覺理解： 當情況越「亂」、越「難預測」，Entropy 就越大。
數學公式假設有一個機率分佈 $P$，其 Entropy $H(P)$ 的公式為：

$$H(P) = -\sum_{i=1}^{n} P(x_i) \log P(x_i)$$

註： 在機器學習中通常以 $e$ 為底（單位是 nats），在資訊理論中則常以 2 為底（單位是 bits）。
```
# .25 發生
# .75 不發生
x = [0.25, 0.75]

H = 0
for p in x:
    H -= p * np.log(p)

print("entropy:", H)


# Binary entropy
H = -(p * np.log(p) + (1 - p) * np.log(1 - p))
print("entropy:", H)
```

## Cross Entropy
Cross Entropy (交叉熵)：你猜得有多準？Cross Entropy 是用來衡量兩個機率分佈之間的距離。
在機器學習中，$P$ 通常是「真實答案」（Ground Truth），而 $Q$ 是「模型預測的結果」。
白話解釋： 想像你在猜一疊牌的顏色。如果實際機率（$P$）是紅色的，但你以為（$Q$）很大機率是藍色，那你的「驚訝程度」就會爆表。
Cross Entropy 就是在計算：當你用錯誤的認知 ($Q$) 去解釋真實的世界 ($P$) 時，你會浪費多少資訊量。
直覺理解： 當預測越準，Cross Entropy 就越接近原本的 Entropy；預測越爛，數值就越大。
這也是為什麼分類問題（如手寫辨識）都用它當 Loss Function，因為我們想讓預測儘可能貼近現實。
數學公式給定真實分佈 $P$ 與預測分佈 $Q$，Cross Entropy $H(P, Q)$ 的公式為：

$$H(P, Q) = -\sum_{i=1}^{n} P(x_i) \log Q(x_i)$$


```
p = [1,0]
q = [.25, .75]

H = 0
for i in range(len(p)):
    H -= p[i] * np.log(q[i])

print('Cross Entropy:' + str(H))



# also correct, written out for N=2 event
H = -(p[0] * np.log(q[0]) + p[1] * np.log(q[1]))
print('Correct entropy: ' + str(H))

# simplification
H = -np.log(q[0])
print('Manually simplified: ' + str(H))
```

torch
```
import torch
import torch.nn.functional as F

q_tensor = torch.Tensor(q)
p_tensor = torch.Tensor(p)

F.binary_cross_entropy(
    q_tensor,
    p_tensor,
)
```

1. $P$：真實分佈 (The Ground Truth)$P$ 代表的是**「現實世界真正的樣子」**。它的角色：標準答案。特性：它是我們想要模仿或達到的目標。例子：如果你在訓練一個辨識貓狗的模型，當一張圖片真的是「貓」時，它的 $P$ 分佈就是 $[1, 0]$（100% 是貓，0% 是狗）。這是不會改變的既定事實。

2. $Q$：預測分佈 (The Predicted Distribution)$Q$ 代表的是**「你對現實的猜測」**。它的角色：模型給出的答案。特性：它是會變動的。在機器學習訓練過程中，我們會不斷調整模型，讓 $Q$ 越來越接近 $P$。例子：模型看到圖片後，說：「我覺得 80% 是貓，20% 是狗」，這時 $Q$ 就是 $[0.8, 0.2]$。

3. $H$：熵 / 交叉熵 (The Measure)$H$ 是最後算出來的一個**「數值」**，用來衡量資訊量或差距。它的角色：評分者。特性：如果是 $H(P)$：衡量現實本身有多亂（Entropy）。如果是 $H(P, Q)$：衡量「用猜測的 $Q$ 去解釋現實的 $P$」時，表現有多糟（Cross Entropy）。直覺理解：$H$ 就像是**「驚訝程度」**。如果 $P$ 說會發生，但你的 $Q$ 說機率很低，最後算出的 $H$ 就會很大，代表你被現實狠狠地「驚嚇」到了。


| 符號 | 英文名稱 | 中文意義 | 機器學習角色 | 白話直覺理解 |
| :--- | :--- | :--- | :--- | :--- |
| **$P$** | **True Distribution** | **真實分佈** | **Label (標籤)** | 現實世界的真相、標準答案。 |
| **$Q$** | **Predicted Distribution** | **預測分佈** | **Prediction (預測值)** | 模型根據目前經驗猜出的機率。 |
| **$H(P)$** | **Entropy** | **資訊熵** | **數據本身複雜度** | 這件事本身有多「亂」或多難猜？ |
| **$H(P, Q)$** | **Cross Entropy** | **交叉熵** | **Loss Function (損失)** | 你的預測與現實「差了多少」？ |
