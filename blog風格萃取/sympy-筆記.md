---
title: sympy 筆記
date: 2026-01-05 18:57:07
tags: python
---
&nbsp;
<!-- more -->

為了搞論文的數學公式, 希望能把 python 跟數學相關的基本用法搞起來, 特別筆記下

PEMDAS 準則（或 BODMAS、BEMDAS）是數學中用來決定運算順序的規則，確保計算一致性，其代表的順序是：
Parentheses (括號) 優先，然後是 Exponents (指數)，
接著是 Multiplication (乘法) 和 Division (除法)（由左至右），
最後是 Addition (加法) 和 Subtraction (減法)（由左至右）。
中文常說的「先乘除後加減」只涵蓋部分，PEMDAS 則包含指數，而乘除、加減的同級運算要從左到右計算，這點常被忽略導致錯誤。 

PEMDAS 運算順序
P (Parentheses - 括號): 先計算括號內（()、、{}）的運算。
E (Exponents - 指數/次方): 接著計算指數和根號。
M/D (Multiplication/Division - 乘法/除法): 執行乘法和除法，自左至右計算。
A/S (Addition/Subtraction - 加法/減法): 最後執行加法和減法，自左至右計算。 


重要的 import
```
import pandas as pd
import numpy as np
from IPython.display import display, Math
```

分號
```
display(Math("3x(4+y) = %g" % ans))
```

乘法
```
display(Math("3\\times%g(4+%g) = %g" % (x, y, ans)))
```

power
```
display(Math("3^2\\times 3^4 = 3^{2+4}"))
```

Sympy And LaTex

下標可以用底線
```
display(Math("x_{mm} + y^{n+2k-15}"))
```


在 python 用 LaTex 需要兩個斜線
```
display(Math("\\text{The answer to this equation is }\\frac{1+x}{2v-s^{t+4r}}"))
```

也可以在 markdown 使用 LaTex
```
$$\frac{1+x}{2v-s^{t+4r}}$$
```

導數
```
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, cos, pi, lambdify

# 1. 符號計算部分
x_sym = symbols('x')
f_sym = cos(2 * pi * x_sym) + x_sym**2
df_sym = diff(f_sym, x_sym)

# 2. 轉換為 NumPy 可用的函數 (關鍵步驟)
# 'numpy' 參數會自動將 sympy.pi 轉為 np.pi，sympy.cos 轉為 np.cos
f_num = lambdify(x_sym, f_sym, 'numpy')
df_num = lambdify(x_sym, df_sym, 'numpy')

# 3. 準備數值資料
x_vals = np.linspace(-2, 2, 2001)
y_vals = f_num(x_vals)
dy_vals = df_num(x_vals)

# 4. 繪圖
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label='$f(x) = \cos(2\pi x) + x^2$', color='blue')
plt.plot(x_vals, dy_vals, label="$f'(x)$ (Derivative)", color='red', linestyle='--')

plt.xlim(x_vals[0], x_vals[-1])
plt.axhline(0, color='black', linewidth=0.5) # 加入 X 軸基準線
plt.grid(True, linestyle=':', alpha=0.7)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Function and its Derivative')
plt.legend()
plt.show()
```
