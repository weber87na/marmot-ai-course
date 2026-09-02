---
title: softmax 筆記
date: 2026-01-27 01:16:14
mathjax: true
tags:
---
&nbsp;
<!-- more -->

softmax 簡單說就是把一組亂七八糟的數字轉化為加總為 1
z 通常被稱為 Logits (原始分數)

$$\sigma(\mathbf{z})_i = \frac{e^{z_i}}{\sum e^{z_j}}$$


softmax 計算實例: $\mathbf{z} = [1, 2, 3]$

---

1: 計算指數值 ($e^{z_i}$)
首先, 對輸入向量中的每個元素取自然指數. 這裡取 $e \approx 2.71828$.

* $e^1 \approx 2.7183$
* $e^2 \approx 7.3891$
* $e^3 \approx 20.0855$

2: 計算分母 (所有指數的總和)
將上述結果加總:
$$\sum e^{z_j} = 2.7183 + 7.3891 + 20.0855 = 30.1929$$

3: 計算各別機率
將每個指數值除以總和:

1. $P_1 = \frac{2.7183}{30.1929} \approx 0.0900$
2. $P_2 = \frac{7.3891}{30.1929} \approx 0.2447$
3. $P_3 = \frac{20.0855}{30.1929} \approx 0.6653$

---

終結果統計表

| 輸入 ($z_i$) | 指數 ($e^{z_i}$) | 機率 ($P_i$) | 百分比 |
| :--- | :--- | :--- | :--- |
| 1 | 2.7183 | 0.0900 | 9.00% |
| 2 | 7.3891 | 0.2447 | 24.47% |
| 3 | 20.0855 | 0.6653 | 66.53% |
| **總和** | **30.1929** | **1.0000** | **100%** |


程式碼

```
/**
 * 計算 Softmax 的穩定版本
 * @param {number[]} logits - 原始分數陣列
 * @returns {number[]} - 機率分佈
 */
function softmax(logits) {
  // 1. 找到陣列中的最大值 (數值穩定性關鍵)
  const maxLogit = Math.max(...logits);
  
  // 2. 計算每個元素的 e^(x - max)
  const exponents = logits.map(z => Math.exp(z - maxLogit));
  
  // 3. 計算所有指數的總和
  const totalSum = exponents.reduce((acc, val) => acc + val, 0);
  
  // 4. 歸一化: 每個元素除以總和
  return exponents.map(exp => exp / totalSum);
}

// 測試代碼
const testScores = [2.0, 1.0, 0.1];
const result = softmax(testScores);

console.log("Input:", testScores);
console.log("Output (Probabilities):", result);
console.log("Total Sum:", result.reduce((a, b) => a + b, 0)); // 結果應為 1

//如果出現 0.9999999999 這種精度落差可以用這樣解
const sum = result.reduce((a, b) => a + b, 0);
const isCloseToOne = Math.abs(sum - 1) < Number.EPSILON; 

console.log(isCloseToOne); // true
```





python
```
# numpy
z = [1, 2, 3]

num = np.exp(z)
den = np.sum(np.exp(z))
sigma = num / den
print(sigma)

# torch
softfun = nn.Softmax(dim=0)
sigmaT = softfun(torch.Tensor(z))
print(sigmaT)
```
