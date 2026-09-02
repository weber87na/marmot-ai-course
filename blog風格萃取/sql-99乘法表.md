---
title: sql 99乘法表
date: 2020-10-05 00:13:58
tags:
- sql
---
&nbsp;
![terminal](https://raw.githubusercontent.com/weber87na/flowers/master/terminal.png)
<!-- more -->





### c#
今天看書時又看到這題，這也是老生常談了，多數看到 c# or java 等程式語言會採用 loop 方式進行兩重迴圈輸出如下
``` csharp
            //橫式
            for(int i = 1; i <= 9; i++) {
                for(int j = 1; j <= 9; j++) {
                    string str = $"{i} * {j} = {(i * j).ToString().PadLeft(2,' ')} | ";
                    Console.Write(str);
                }
                Console.WriteLine();
                Console.WriteLine();
            }

            //直式
            for (int i = 1; i <= 9; i++)
            {
                //繪製 1 to 9
                for(int j = 0; j < 9; j++)
                {
                    Console.Write($"   {i}  ");
                }
                Console.WriteLine();


                //繪製乘號及 1 to 9
                for (int j = 1; j <= 9; j++)
                {
                    Console.Write($"x  {j}  ");
                }
                Console.WriteLine();


                //繪製填寫答案前的分隔號
                for (int j = 1; j <= 9; j++)
                {
                    Console.Write($"----  ");
                }
                Console.WriteLine();

                //繪製解答
                for (int j = 1; j <= 9; j++)
                {
                    Console.Write($"{(i * j).ToString().PadLeft(4, ' ')}  ");
                }
                Console.WriteLine();

                //保持多空一行
                Console.WriteLine();
            }

```
其實可以用 linq 寫 , 跟 sql 解法雷同產生笛卡爾積
``` csharp
	var nums = Enumerable.Range( 1, 9 );
	var result = from x in nums
				 from y in nums
				 select $"{x} * {y} = {x * y}";
	result.ToList().ForEach( x => Console.WriteLine(x));
```
後來想到這樣寫成直式好像也滿直覺的
``` csharp
	var nums = Enumerable.Range( 1, 9 );
	var result = from x in nums
				 from y in nums
				 select
				 $@"  {y.ToString( ).PadLeft( 4 )}" + Environment.NewLine +
				 $@"x {x.ToString( ).PadLeft( 4 )}" + Environment.NewLine +
				 $@"------" + Environment.NewLine +
				 $@"  {(x * y).ToString( ).PadLeft( 4 )}" + Environment.NewLine;
	result.ToList().ForEach( x => Console.WriteLine(x));
```

這裡還有很噁爛的 `SelectMany` 寫法 , 想要詳細知道 linq 可以看這個微軟 mvp 大神的 [blog](https://weblogs.asp.net/dixin/entity-framework-core-and-linq-to-entities-4-query-methods-7) , 應該是講解 linq 最細的 blog
``` csharp
var num = Enumerable.Range(1, 9);
var result = num.SelectMany(
		x => num,
		(x, y) => $"{x} * {y} = {x * y}" 
	);
result.ToList().ForEach(x => Console.WriteLine(x));
```

### sql server


<iframe 
    width="1235" 
    height="772" 
    src="https://www.youtube.com/embed/KVLRRX3YUF8" 
    title="純 sql 寫 99 乘法表" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" 
    allowfullscreen>
</iframe>


而 SQL 採用集合做為思考，一般都會使用 UNION ALL 搭配遞迴與 CROSS JOIN 進行計算，大概會長得像下面這樣
``` sql
WITH TALLY(N) AS (
    SELECT  1 
    UNION ALL
    SELECT  2
    UNION ALL
    SELECT  3
    UNION ALL
    SELECT  4
    UNION ALL
    SELECT  5
    UNION ALL
    SELECT  6
    UNION ALL
    SELECT  7
    UNION ALL
    SELECT  8
    UNION ALL
    SELECT  9
)
SELECT CAST(A.N AS varchar) + '*'  
    + CAST(B.N AS varchar) + '=' 
    + CAST(A.N * B.N AS varchar)
FROM Tally A 
CROSS JOIN Tally B

--使用遞迴(RECURSIVE)
WITH TALLY(N) AS (
    SELECT  1 N
    UNION ALL
    SELECT 1 + N
    FROM Tally
    WHERE N < 9
)
SELECT CAST(A.N AS varchar) + '*'  
    + CAST(B.N AS varchar) + '=' 
    + CAST(A.N * B.N AS varchar)
FROM Tally A 
CROSS JOIN Tally B
```

無聊想到好像也搭配 `REPLICATE` 可以拿來畫個三角形 , `REPLICATE` 到底還能做啥呢 , 大概統計東西時可以畫個文字版的 chart 之類的吧
```
WITH TALLY(N) AS (
    SELECT  1 N
    UNION ALL
    SELECT 1 + N
    FROM Tally
    WHERE N < 9
)
SELECT REPLICATE('*',N)
FROM TALLY
```

偶然看到[老外文章](https://blog.jooq.org/2016/04/25/10-sql-tricks-that-you-didnt-think-were-possible/)
 VALUES 也可以當作衍生資料表使用所以又生出一種無腦的寫法
``` sql
WITH TALLY AS(
    SELECT *
    FROM (
        VALUES(1),(2),(3),(4),(5),(6),(7),(8),(9)
    ) T(N) 
)
SELECT CAST(A.N AS varchar) + '*'  
    + CAST(B.N AS varchar) + '=' 
    +  CAST(A.N * B.N AS varchar)
FROM TALLY A
CROSS JOIN TALLY B
```

如果是 sql server 2016 可以用 `string_split`
```
with cte(n) as (
	select cast(value as int) as n
	from string_split('1,2,3,4,5,6,7,8,9' , ',')
)
select x.n , '*' as '*' , y.n , '=' as '=' , (x.n * y.n) result
from cte x
cross join cte y
```

其實也能寫出直式 XD
```
with t(n) as (
select 1 n
union all
select 1 + n
from t
where n < 9
)
select right('     ' + cast(a.n as varchar(5)),5) + char(13) + char(10) +
'x' + right('    ' + cast(b.n as varchar(5)),4) + char(13) + char(10) +
'-----' + char(13) + char(10) +
right('     ' + cast(a.n * b.n as varchar(5)),5) + char(13) + char(10) +
' '
from t a , t b
```


### postgresql
後來想到 postgresql 其實可以直接用 generate_series 函數產生或是 array達成相同效果，
順便多個機車變化，將計算出的答案以 9 , 8 , 7 , 1 , 2 , 4 , 5 , 6 進行排序，一題完美刁難面試者的題目就誕生了
``` sql
--使用generate_series
select a , b , a || '*' || b || '=' || a * b as result
from generate_series(1,9) a , generate_series(1,9) b
order by 
case when a >= 7 then a else -a end desc 
, b asc;

--使用array
elect a , b , a || '*' || b || '=' || a * b as result
from unnest(array[1,2,3,4,5,6,7,8,9]) a , unnest(array[1,2,3,4,5,6,7,8,9]) b
order by 
case when a >= 7 then a else -a end desc 
, b asc;
```

### oracle
偶然機會下用到 Oracle 想說順便玩玩 , 然後就可以生出有顏色的九九乘法了
```
WITH TALLY AS (
SELECT 1 N FROM DUAL
UNION ALL
SELECT 2 N FROM DUAL
UNION ALL
SELECT 3 N FROM DUAL
UNION ALL
SELECT 4 N FROM DUAL
UNION ALL
SELECT 5 N FROM DUAL
UNION ALL
SELECT 6 N FROM DUAL
UNION ALL
SELECT 7 N FROM DUAL
UNION ALL
SELECT 8 N FROM DUAL
UNION ALL
SELECT 9 N FROM DUAL
)
SELECT CASE WHEN MOD(X.N , 2) = 0 THEN '<html><font color="red">' || X.N || '*' || Y.N || '=' || X.N * Y.N
ELSE X.N || '*' || Y.N || '=' || X.N * Y.N END NINENINE
FROM TALLY X
CROSS JOIN TALLY Y
```

### python
最近搞 python , 來個單迴圈
```
i = 1
j = 1

while j <= 9:
    print(f"{i} * {j} = {i * j}")
    if i == 9:
        j += 1
        i = 1
    else:
        i += 1
```

反人類遞迴 python
```
def test(i, j):
    if j <= 9:
        print(f"{i} * {j} = {i * j}")
        if i == 9:
            j += 1
            i = 1
        else:
            i += 1

        test(i, j)

test(1,1)
```


### js
```
for (var i = 1, j = 1; j <= 9;){
    console.log(`${i} * ${j} = ${i * j}`)
    if (i == 9) {
        i = 1
        j += 1
    } else {
        i += 1
    }
}
```

雙重遞迴 , 關鍵是在 N 裡面再多包一個 M 的遞迴
首先當數字小於 10 時會不斷印出來 , 當數字執行到 10 的時候會 return
接著再回到 N 開始往下個數字疊加下去 , 此時 m 已經歸零又重新進入 M 的遞迴
有趣的是拿這串 code 去問 chatgpt 問他這串作用是啥 , 他竟然可以回出 99 乘法表 , 真是太噁心了
```
function N(n , m){
	if(n === 10){
		return
	} else {
		M(m + 1, n)
		return N(n + 1 , m)
	}
}

function M(m , n){
	if(m === 10){
		return
	} else {
		console.log(`${n} * ${m} = ${n * m}`)
		return M(m + 1 , n)
	}
}

N(0,0)
```

### rxjs
最近搞 rxjs 開開腦洞
```
let A$ = range(1, 9)
let B$ = range(1, 9)

A$.subscribe(x => {
    console.log(`----${x}-----`)
    B$.subscribe(y =>
        console.log(`${x} * ${y} = ${x * y}`)
    )
    console.log('----------')
})
```
