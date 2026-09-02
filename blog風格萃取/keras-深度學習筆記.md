---
title: keras 深度學習筆記
date: 2026-03-09 22:23:58
tags:
---
&nbsp;
<!-- more -->

## 第一堂 環境安裝

搞這麼久今天才知道有這個指令 `conda create -n keras anaconda` 問了 AI 回說會很占用空間, 還是先放棄 XD
```
conda create -n keras python=3.10 -y
conda activate keras
pip install tensorflow keras numpy pandas matplotlib
```

學校安裝有問題會跳個 `streamlit 1.51.0 requires protobuf<7,>3.20`
問 AI 可以這樣解 
```
pip install "protobuf<7" --upgrade
```

最後可以這樣檢查, 正常會跳 `No broken requirements found`
```
pip check
```

測試有無成功 `test_keras.py`
```
import keras
import tensorflow as tf

print(f"Keras 版本: {keras.__version__}")
print(f"TensorFlow 版本: {tf.__version__}")
```
