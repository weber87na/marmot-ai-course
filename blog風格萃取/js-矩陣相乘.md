---
title: js 矩陣相乘
date: 2026-01-24 18:43:07
tags: js
---
&nbsp;
<!-- more -->

矩陣運算, 每次遇到這個問題就頭痛想半天, 要搞這個就要先理解術語

台灣跟大陸定義剛好是反過來, 看得很煩躁

m = row = y = height = 高 = 列 = 行(簡)
n = column = x = width = 寬 = (欄/行) = 列(簡)

```
height = len(matrix)     # y 的最大範圍 (Rows)
width = len(matrix[0])   # x 的最大範圍 (Cols)

for y in range(height):      # 外層跑垂直高度 (y 方向)
    for x in range(width):   # 內層跑水平寬度 (x 方向)
        # 注意：矩陣存取通常是 [y][x]
        print(f"座標 ({x}, {y}) 的值為: {matrix[y][x]}")


rows = len(matrix)
cols = len(matrix[0])

for i in range(rows):
    for j in range(cols):
        print(matrix[i][j])
```

搞定術語後就可以進入正題

可以參考這裡 [mathsisfun](https://www.mathsisfun.com/algebra/matrix-multiplying.html)
或是用這個線上工具來算 [matrixmultiplication](http://matrixmultiplication.xyz/)

(1, 2, 3) • (7, 9, 11)= 1×7 + 2×9 + 3×11 = 58
(1, 2, 3) • (8, 10, 12) = 1×8 + 2×10 + 3×12 = 64

(4, 5, 6) • (7, 9, 11) = 4×7 + 5×9 + 6×11 = 139
(4, 5, 6) • (8, 10, 12) = 4×8 + 5×10 + 6×12 = 154

關鍵在於先把解答矩陣大小算出來

A (2 * 3) = 2 h * 3 w
B (3 * 2) = 3 h * 2 w

只取 A 的 h 跟 B 的 w
C (2 * 2) = C(Ay * Bx)

所以這裡會得到一個 m = 2, n 也 = 2 的 matrix

計算時跟平時操作 2d array 一樣, aWidth 等於就是次數

第三個迴圈是這題另外一個關鍵, 他第一次會長這樣以此類推

C[0][0] += A[0][0] * B[0][0] //1*7
C[0][0] += A[0][1] * B[1][0] //2*9
C[0][0] += A[0][2] * B[2][0] //3*11
結果為 58

C[0][1] += A[0][0] * B[0][1] //1*8
C[0][1] += A[0][1] * B[1][1] //2*10
C[0][1] += A[0][2] * B[1][1] //3*12
結果為 64

最後要注意到矩陣維度問題

(3,2) * (3,2) not work
(2,3) * (3,2) work
(3,2) * (2,3) work


```
let A = [
	[1,2,3],
	[4,5,6]
]

let B = [
	[7,8],
	[9,10],
	[11,12],
]

ay = aHeight = A.length
ax = aWidth = A[0].length
by = bHeight = B.length
bx = bWidth = B[0].length

console.log(`ay ${ay}`)
console.log(`ax ${ax}`)
console.log(`by ${by}`)
console.log(`bx ${bx}`)



let C = []
for (let y = 0; y < ay; y++) {
    C[y] = []
    for (let x = 0; x < bx; x++) {
        C[y][x] = 0
    }
}



//立即列印, 防止 chrome 之後印參考
console.log(JSON.stringify(C))

/*
let C = [
	[0,0],
	[0,0],
]
*/


//計算結果
for(let y = 0; y < aHeight; y++){
	for(let x = 0; x < bWidth; x++){
		for(let z = 0; z < aWidth; z++){
			C[y][x] += A[y][z] * B[z][x]
		}
	}
}

/*
C[0][0] += A[0][0] * B[0][0] //1*7
C[0][0] += A[0][1] * B[1][0] //2*9
C[0][0] += A[0][2] * B[2][0] //3*11
結果為 58

C[0][1] += A[0][0] * B[0][1] //1*8
C[0][1] += A[0][1] * B[1][1] //2*10
C[0][1] += A[0][2] * B21][1] //3*12
結果為 64
*/

console.log(C)

```

偷懶用 chatgpt 搞成 python XD

```
# 定義矩陣
A = [
    [1, 2, 3],
    [4, 5, 6]
]

B = [
    [7, 8],
    [9, 10],
    [11, 12]
]

# 矩陣尺寸
aHeight = len(A)
aWidth = len(A[0])
bHeight = len(B)
bWidth = len(B[0])

print(f"ay {aHeight}")
print(f"ax {aWidth}")
print(f"by {bHeight}")
print(f"bx {bWidth}")

# 初始化結果矩陣 C
C = [[0 for _ in range(bWidth)] for _ in range(aHeight)]

# 立即列印，防止引用問題
import json
print(json.dumps(C))

# 計算結果
for y in range(aHeight):
    for x in range(bWidth):
        for z in range(aWidth):
            C[y][x] += A[y][z] * B[z][x]

print(C)

```

順帶一提要算 dot product 可以這樣寫
```
A = [[0, 3, 2], [-3, -3, 1], [1, 0, 2]]

B = [[1, 0, 6], [2, -1, 0], [5, 1, 4]]

total = 0
for y in range(len(A)):
    for x in range(len(A[0])):
        total += A[y][x] * B[y][x]
        print(f"{A[y][x] * B[y][x]:>2} ", end="")
    print()

print()
print(f"total:{total}")
```
