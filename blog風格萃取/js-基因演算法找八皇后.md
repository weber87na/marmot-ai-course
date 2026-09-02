---
title: js 基因演算法找八皇后
date: 2025-12-20 10:02:33
tags: js
---
&nbsp;
<!-- more -->

```js
const userInputNum = process.argv[2]

//100 皇后跑不太出來
//50 皇后有機會
const population = 100
const numOfQueen = userInputNum
let geneList = []
let counterArr = []

geneList = initGeneList(population, numOfQueen)
let counter = 1
while (true) {

    const currentBest = geneList.reduce((minItem, current) => {
        return current.total < minItem.total ? current : minItem;
    }, geneList[0])


    if (counter % 100 === 0) {
        console.log(`目前最佳衝突數 ${currentBest.total} 狀態 ${currentBest.simple.join(' ')}`)
        console.log(counter)
        counterArr.push(counter)
    }

    let ans = geneList.filter(item => item.total === 0)
    if (ans.length > 0) {
        console.log(`第 ${counter} 代找到最佳解`)
        console.log(ans)
        // console.log('node index.js ' + `${ans[0].simple.length}` + ' ' + `'${ans[0].simple.join(' ')}'`)
        console.log('ans: ' + `'${ans[0].simple.join(' ')}'`)

        let queens = getQueens(ans[0].simple)

        //初始化棋盤
        let board = initEmptyBoard(ans[0].simple.length)


        //放入皇后
        board = fillQueen(board, ans[0].simple)
        printBoard(board)

        return
    }

    //陷入 local optima
    //只保留前 N 名的基因, 然後重新殺了所有個體
    if (counterArr.length >= 2) {
        let top10Percent = population * 0.1
        geneList = createNext(population, geneList).slice(0, top10Percent)
        let newGeneList = initGeneList(population, numOfQueen).slice(population * 0.1, population)
        geneList = geneList.concat(newGeneList)
        counterArr = []
    } else {
        geneList = createNext(population, geneList)
    }


    geneList = createNext(population, geneList)

    counter++
}


function initGeneList(population, numOfQueen) {
    let geneList = []
    for (let i = 0; i < population; i++) {
        let current = initialState(numOfQueen)
        let emptyBoard = initEmptyBoard(current.length)
        let queens = getQueens(current)
        let board = fillQueen(emptyBoard, current)
        let currentScore = calcResult(board, queens)
        geneList.push(currentScore)
    }

    //排序
    geneList.sort((a, b) => a.total - b.total)

    return geneList
}

function crossover(parentA, parentB) {
    const numOfQueen = parentA.simple.length
    let childGene = []

    //隨機選父母基因
    for (let i = 0; i < numOfQueen; i++) {
        if (Math.random() < 0.5) childGene.push(parentA.simple[i])
        else childGene.push(parentB.simple[i])
    }

    return childGene
}



function createNext(population, geneList) {
    //前 K% 進入下一代
    let topK = Math.ceil(population * 0.1)

    //存活者
    let survivor = geneList.slice(0, topK)

    let lastNPercent = geneList.slice(population * 0.5)


    let nextGeneList = []

    //產生下一代
    for (let i = 0; i < population - topK; i++) {
        //隨機選兩個人 包含保證進入的存活者
        //菁英父母

        let a = Math.floor(Math.random() * survivor.length)

        //後段父母
        let b = Math.floor(Math.random() * lastNPercent.length)

        let parentA = survivor[a]
        let parentB = lastNPercent[b]

        let mutationRate = 0.2

        //crossover
        let childGene = crossover(parentA, parentB)


        //mutation 突變率越大越隨機
        //自然界千分之三突變率太低
        if (Math.random() < mutationRate) {
            //更隨機一點突變
            for (let m = 0; m < 10; m++)
                childGene = mutation(childGene)
        }

        let emptyBoard = initEmptyBoard(childGene.length)
        let queens = getQueens(childGene)
        let board = fillQueen(emptyBoard, childGene)
        let child = calcResult(board, queens)
        nextGeneList.push(child)
    }
    nextGeneList = nextGeneList.concat(survivor)
    nextGeneList.sort((a, b) => a.total - b.total)

    return nextGeneList
}



function mutation(current) {
    // console.log('randomSuccessor', current)
    let pos = Math.floor(Math.random() * current.length)
    while (true) {
        let newPosY = Math.floor(Math.random() * current.length)
        if (current[pos] !== newPosY) {
            let result = [...current]
            result[pos] = newPosY
            return result
        }
    }
}


//亂數建立皇后在棋盤位置的 array
function initialState(num) {
    let result = []
    for (let i = 0; i < num; i++) {
        let pos = Math.floor(Math.random() * num)
        result.push(pos)
    }
    return result
}


/** 計算結果*/
function calcResult(board, queens) {
    let result = []
    let total = 0
    for (let i = 0; i < queens.length; i++) {
        let queen = queens[i]
        let count = scan(queen, board)
        result.push({ x: queen.x, y: queen.y, count: count })
        // console.log(`queen:(${queen.x},${queen.y})-${count}次`)
        total += count
    }

    // console.log(`共:${total}次`)

    return { 'board': result, 'total': total, 'simple': result.map(item => item.y) }

    // return total
}

/**印出棋盤 */
function printBoard(board) {
    for (let y = 0; y < board.length; y++) {
        let str = ''
        for (let x = 0; x < board.length; x++) {
            str += board[y][x] + ' '
        }
        console.log(str)
    }
}


/**組合所有掃描的函數 */
function scan(queen, board) {
    let count = 0
    count += scanRow(queen, board)

    //左上至右下
    count += scanToTopLeft(queen, board)
    count += scanToBottomRight(queen, board)

    //右上至左下
    count += scanToTopRight(queen, board)
    count += scanToBottomLeft(queen, board)

    return count
}

/**掃描目前棋子到左下 */
function scanToBottomLeft(queen, board) {
    let y = queen.y
    let x = queen.x
    let count = 0
    x -= 1
    y += 1

    while (true) {
        if (x < 0 || y >= board.length) break
        if (board[y][x] === 'Q') count++
        x -= 1
        y += 1
    }
    return count
}

/**掃描目前棋子到右上 */
function scanToTopRight(queen, board) {
    let y = queen.y
    let x = queen.x
    let count = 0
    x += 1
    y -= 1

    while (true) {
        if (x >= board.length || y < 0) break
        if (board[y][x] === 'Q') count++
        x += 1
        y -= 1
    }
    return count
}

/**掃描目前棋子到左上 */
function scanToTopLeft(queen, board) {
    let y = queen.y
    let x = queen.x
    let count = 0
    x -= 1
    y -= 1

    while (true) {
        if (x < 0 || y < 0) break
        if (board[y][x] === 'Q') count++
        x -= 1
        y -= 1
    }
    return count
}


/**掃描目前棋子到右下 */
function scanToBottomRight(queen, board) {
    let y = queen.y
    let x = queen.x
    let count = 0
    x += 1
    y += 1

    while (true) {
        if (x >= board.length || y >= board.length) break
        if (board[y][x] === 'Q') count++
        x += 1
        y += 1
    }
    return count
}

/**掃描整個橫向 */
function scanRow(queen, board) {
    let num = board.length
    let y = queen.y
    let count = 0
    for (let x = 0; x < num; x++) {
        if (x === queen.x) continue
        if (board[y][x] === 'Q') count++
    }
    return count
}

/**簡化取得皇后 xy 位置 */
function getQueens(initQueenPos) {
    let queens = []
    for (let i = 0; i < initQueenPos.length; i++) {
        let queen = { x: i, y: initQueenPos[i] }
        queens.push(queen)
    }
    return queens
}

/**建立棋盤 */
function initEmptyBoard(num) {
    let board = []
    for (let y = 0; y < num; y++) {
        board.push([])
        for (let x = 0; x < num; x++) {
            board[y].push('X')
        }
    }
    return board
}

/**填滿皇后 */
function fillQueen(board, initQueenPos) {
    for (let i = 0; i < initQueenPos.length; i++) {
        //取得皇后位置
        let queen = initQueenPos[i]
        //填入皇后
        board[queen][i] = 'Q'
    }
    return board
}
```

後來弄個更快的版本, 主要還是算衝突的方法要想辦法讓他快才會過

可以用數學方法讓計算對角線加速

資料型別可以用 `Uint16Array` 來加速, 避免直接用 `[1,2,3,4]` 來存

突變率數建議不要設定太低, 用自然界千分之三會跑不出來

基因配對時也需要多試試, 完全亂數應該也跑不出來

人口數不能太高也不能太低

```
const userInputNum = process.argv[2]

//100 皇后免強
//50 皇后還行
//40 皇后可以
//20 皇后很快
const population = 500
const numOfQueen = userInputNum

//突變率
const mutationRate = 0.2

let geneList = initGeneList(population, numOfQueen)

//計算目前第幾代
let counter = 1

while (true) {
    //每 100 代列印一次
    if (counter % 100 === 0) {
        const currentBest = geneList[0]
        console.log(`目前最佳衝突數 ${currentBest.total} 狀態 ${currentBest.gene.join(' ')}`)
        console.log(counter)
    }

    //得到解答
    if (geneList[0].total === 0) {
        let ans = geneList[0]
        console.log(`第 ${counter} 代找到最佳解`)
        console.log(`population:${population}`)
        console.log(ans)
        console.log('node index.js ' + `${ans.gene.length}` + ' ' + `'${ans.gene.join(' ')}'`)
        console.log()
        console.log('ans: ' + `'${ans.gene.join(' ')}'`)
        console.log()
        printBoard(ans.gene)
        return
    }

    geneList = createNext(population, geneList, mutationRate)
    counter++
}

//建立下一代
function createNext(population, geneList, mutationRate) {
    //前 K% 進入下一代
    let topK = Math.ceil(population * 0.1)

    //存活者
    let survivor = geneList.slice(0, topK)

    //選擇前 N%
    let topNPercent = geneList.slice(0, population * 0.3)

    let nextGeneList = []

    //產生下一代
    //確保菁英有繼續保留
    for (let i = 0; i < population - topK; i++) {
        //隨機選兩個人
        //前段父母
        let a = Math.floor(Math.random() * survivor.length)

        //後段父母
        let b = Math.floor(Math.random() * topNPercent.length)

        let parentA = survivor[a]
        let parentB = topNPercent[b]

        //crossover
        let childGene = crossover(parentA, parentB)

        //mutation 突變率越大越隨機
        //自然界千分之三突變率太低
        if (Math.random() < mutationRate) {
            childGene = mutation(childGene)
        }

        childGeneObj = toGeneObj(childGene)
        nextGeneList.push(childGeneObj)
    }
    nextGeneList = nextGeneList.concat(survivor)
    nextGeneList.sort((a, b) => a.total - b.total)

    return nextGeneList
}


//把基因跟衝突結果合成物件
function toGeneObj(gene) {
    let total = conflict(gene)
    let geneObj = { gene: gene, total: total }
    return geneObj
}

//突變
//隨機取得一個位置然後在 Y 方向進行移動
function mutation(current) {
    let pos = Math.floor(Math.random() * current.length)
    while (true) {
        let newPosY = Math.floor(Math.random() * current.length)
        if (current[pos] !== newPosY) {
            let result = new Uint16Array(current)
            result[pos] = newPosY
            return result
        }
    }
}


//亂數選基因配對下一代
//loop 走訪每個基因節點 正面選父反面選母
function crossover(parentA, parentB) {
    const n = parentA.gene.length
    let childGene = new Uint16Array(n)

    for (let i = 0; i < n; i++) {
        childGene[i] = (Math.random() < 0.5) ? parentA.gene[i] : parentB.gene[i]
    }
    return childGene
}


//初始化所有基因並且依照衝突數來排序
function initGeneList(population, numOfQueen) {
    let result = []
    for (let i = 0; i < population; i++) {
        let gene = initialState(numOfQueen)
        let geneObj = toGeneObj(gene)
        result.push(geneObj)
    }

    //排序
    result.sort((a, b) => a.total - b.total)

    return result
}

//建立棋盤
function initialState(num) {
    let result = new Uint16Array(num)
    for (let i = 0; i < num; i++) {
        let pos = Math.floor(Math.random() * num)
        result[i] = pos
    }
    return result
}

//衝突數計算
function conflict(gene) {
    let counter = 0
    for (let i = 0; i < gene.length; i++) {
        //取得目前數值
        let x1 = i
        let y1 = gene[i]

        for (let j = i + 1; j < gene.length; j++) {

            //取得後面元素的數值
            let x2 = j
            let y2 = gene[j]

            //計算橫向的衝突
            if (y1 === y2) counter++

            //計算斜線
            if (Math.abs(y1 - y2) === Math.abs(x1 - x2)) counter++
        }
    }
    return counter * 2
}

//印出棋盤
function printBoard(gene) {
    let board = []
    for (let y = 0; y < gene.length; y++) {
        board.push([])
        for (let x = 0; x < gene.length; x++) {
            board[y].push('X')
        }
    }

    for (let i = 0; i < gene.length; i++) {
        //取得皇后位置
        let queen = gene[i]
        //填入皇后
        board[queen][i] = 'Q'
    }

    for (let y = 0; y < gene.length; y++) {
        let str = ''
        for (let x = 0; x < gene.length; x++) {
            str += board[y][x] + ' '
        }
        console.log(str)
    }
}
```

後來問 AI 還有更噁心的方法來解 `conflict` 用這樣速度應該爆快
```
// 優化後的衝突計算 O(N)

function conflict(gene) {

    let collisions = 0;

    const n = gene.length;

    // 使用 TypedArray 加速運算

    const rowCount = new Int32Array(n);

    const diag1Count = new Int32Array(2 * n); // y - x

    const diag2Count = new Int32Array(2 * n); // y + x



    for (let i = 0; i < n; i++) {

        const y = gene[i];

        const d1 = y - i + n; // 加 n 確保索引為正數

        const d2 = y + i;



        // 如果該行、或對角線已經有皇后，則增加衝突數

        collisions += rowCount[y]++;

        collisions += diag1Count[d1]++;

        collisions += diag2Count[d2]++;

    }

    return collisions;

}
```
