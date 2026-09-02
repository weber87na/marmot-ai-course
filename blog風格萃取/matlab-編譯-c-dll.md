---
title: matlab 編譯 c# dll
date: 2026-01-21 03:45:22
tags:
---
&nbsp;
<!-- more -->

十多年前曾經有參加過一個案子會用 c# 呼叫 matlab 函數, 最近又被問到以前的考古問題早就都忘光光了, 還好現在是學生可以免費蹭 matlab XD

開啟 matlab 在選單找到 `APPS` => `Get More Apps`

接著安裝 `MATLAB Compiler` `MATLAB Compiler SDK`

他新版跟舊版作法又不太一樣, 舊版叫做 `MWArray API` 新版則是 `MATLAB Data API for .NET`

先建立一個 matlab 函數, 檔名為 `add_two_numbers`
```
function result = add_two_numbers(a, b)
    result = a + b;
end
```

點選 `APPS` => `.NET Assembly Compiler`

點選 `Exported Functions` => `Add Exported Function` 把 `add_two_numbers` 函數加入

### MATLAB Data API for .NET

<iframe 
	width="1235" 
	height="772" 
	src="https://www.youtube.com/embed/GEsAWn2tCOI" 
	title="How to compile a MATLAB function for .NET 8 (MATLAB Data API for .NET)" 
	frameborder="0" 
	allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
	referrerpolicy="strict-origin-when-cross-origin" 
	allowfullscreen>
</iframe>

點選 `.NET API Selection` => `Create interface that uses the MATLAB Data API for .NET`

點選 `Assembly Options` =>  `.NET 5.0 or higher`

點選 `Installer Details` => `Do not include MATLAB Runtime in application Installer`

然後選擇編譯, 他會建立一個 c# csproj, 可以直接在 solution 底下直接建個新的 console 專案

引入剛剛 matlab 編譯好的專案

接著看看自己電腦是否有 matlab 沒的話請使用 runtime

runtime 可以在這裡下載 https://www.mathworks.com/products/compiler/matlab-runtime.html

If MATLAB is installed on your system	

`matlabroot\extern\dotnet\netstandard2.0\MathWorks.MATLAB.Runtime.dll`

`matlabroot\extern\dotnet\netstandard2.0\MathWorks.MATLAB.Types.dll`


If MATLAB Runtime is installed on your system
<MATLAB_RUNTIME_INSTALL_DIR>\extern\dotnet\netstandard2.0\MathWorks.MATLAB.Runtime.dll`

`<MATLAB_RUNTIME_INSTALL_DIR>\extern\dotnet\netstandard2.0\MathWorks.MATLAB.Types.dll`


我環境的位置在 `C:\Program Files\MATLAB\R2025b\extern\dotnet\netstandard2.0` 
加入參考 `MathWorks.MATLAB.Types.dll` `MathWorks.MATLAB.Runtime.dll`

或參考這個 [官方範例](https://www.mathworks.com/help/compiler_sdk/dotnet/dotnet-development-environment.html) 去調整 csproj

```
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net5.0</TargetFramework>
  </PropertyGroup>
  
  <ItemGroup>
    <Reference Include="MathWorks.MATLAB.Runtime">
      <HintPath>C:\Program Files\MATLAB\MATLAB Runtime\R2025b\extern\dotnet\netstandard2.0\MathWorks.MATLAB.Runtime.dll</HintPath>
    </Reference>
    <Reference Include="MathWorks.MATLAB.Types">
      <HintPath>C:\Program Files\MATLAB\MATLAB Runtime\R2025b\extern\dotnet\netstandard2.0\MathWorks.MATLAB.Types.dll</HintPath>
    </Reference>
  </ItemGroup>
</Project>
```

貼上以下程式碼即可
```csharp
// See https://aka.ms/new-console-template for more information
using MathWorks.MATLAB.Types;
using MathWorks.MATLAB.Runtime;
using MyDotNetAssembly;

// 1. 建立 MATLAB Runtime 實例 (這會消耗較多時間，建議重用)
// 注意：這裡啟動的是封裝後的 Runtime 環境
using (var matlab = MATLABRuntime.StartMATLAB("MyDotNetAssembly.ctf"))
{
    double inputA = 1.0;
    double inputB = 2.0;
    dynamic result;

    // 2. 呼叫生成的靜態方法
    // 第一個參數是剛建立的 matlab 實例
    // 最後一個參數使用 out 接收回傳值
    MATLABFunctions.add_two_numbers(matlab, inputA, inputB, out result);

    // 3. 處理回傳值
    // 在強型別介面中，回傳通常是 MATLABArray，可以直接進行運算或轉型
    Console.WriteLine($"計算結果: {result}");

    // 如果需要轉回 C# 原生型別 (例如 double)
    double finalValue = (double)result;
    Console.WriteLine($"轉型後的結果: {finalValue}");
}

```

### MWArray API

<iframe 
	width="1235" 
	height="772" 
	src="https://www.youtube.com/embed/GV0AvIT4MRs" 
	title="How to compile a MATLAB function for .net framework 4.8 (MWArray API)" 
	frameborder="0" 
	allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
	referrerpolicy="strict-origin-when-cross-origin" 
	allowfullscreen>
</iframe>

點選 `.NET API Selection` => `Create interface that uses the mwArray API for .NET`

點選 `Assembly Options` =>  `.NET 4.x(.NET framework)`

點選 `Installer Details` => `Do not include MATLAB Runtime in application Installer`

要調整類別名稱的話則選 `Build Settings` => `Class info`

編譯之後請自己開一個 .net framework 的 console 並且引入剛剛編譯好的 dll

另外還需要引入 `MWArray.dll` 它的位置在 `C:\Program Files\MATLAB\R2025b\toolbox\dotnetbuilder\bin\win64\netstandard2.0`

特別注意到他這裡是 `win64` c# 專案也要用 `x64` 如果你的環境是 `x86` 則記得選則 `x86` 不然會噴 error 噴到死 ~~~

最後記得要改成 `x64` 不然會噴 error!
最後記得要改成 `x64` 不然會噴 error!
最後記得要改成 `x64` 不然會噴 error!
最後記得要改成 `x64` 不然會噴 error!
最後記得要改成 `x64` 不然會噴 error!

最後貼上以下程式碼即可
```csharp
using System;
using MathWorks.MATLAB.NET.Arrays;
using MyDotNetAssembly;

namespace MatlabTest
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                // 1. 實例化 MATLAB 類別
                // 在 MWArray 版本中，通常是直接 new 出產生的類別實例
                // 這會自動初始化 MATLAB Runtime
                Class1 matlabObj = new Class1();

                // 2. 準備輸入參數
                // 需要將 C# 原生型別包裝成 MWArray (這裡使用 MWNumericArray)
                MWNumericArray inputA = 1.0;
                MWNumericArray inputB = 2.0;

                // 3. 呼叫方法
                // 第一個參數是「輸出參數的個數」(numArgsOut)
                // 之後才是 MATLAB 函數所需的輸入參數
                // 回傳值會是一個 MWArray 陣列 (因為 MATLAB 函數可能回傳多個值)
                MWArray[] results = matlabObj.add_two_numbers(1, inputA, inputB);

                // 4. 處理回傳值
                // 即使只有一個回傳值，也會放在陣列的第一個元素 [0]
                MWArray result = results[0];
                Console.WriteLine($"計算結果 (MWArray): {result}");

                // 5. 轉回 C# 原生型別 (例如 double)
                // 這裡通常使用 ToScalarDouble() 或強轉為 MWNumericArray 後取值
                double finalValue = ((MWNumericArray)result).ToScalarDouble();
                Console.WriteLine($"轉型後的結果: {finalValue}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"發生錯誤: {ex.Message}");
            }
        }
    }
}

```
