---
title: confusion matrix
date: 2026-02-05 21:25:00
mathjax: true
tags:
---
&nbsp;
<!-- more -->

| | 實際正類 (Actual Positive) | 實際負類 (Actual Negative) |
| :--- | :---: | :---: |
| **預測正類 (Predicted Positive)** | **TP** (True Positive) <br> 真陽性 | **FP** (False Positive) <br> 偽陽性 |
| **預測負類 (Predicted Negative)** | **FN** (False Negative) <br> 偽陰性 | **TN** (True Negative) <br> 真陰性 |


### 核心指標公式

準確率 (Accuracy)
$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$


精確率 (Precision)
常用在垃圾郵件分類, 不可將重要郵件誤判為垃圾郵件
$$\text{Precision} = \frac{TP}{TP + FP}$$


召回率 (Recall)
常用在醫療診斷, 寧可誤診也不要錯過任何一種可能的疾病
或是用在詐騙偵測, 寧可錯殺也不要放過任何一種詐騙導致重大損失
$$\text{Recall} = \frac{TP}{TP + FN}$$


F1 分數 (F1-Score)
$$F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
