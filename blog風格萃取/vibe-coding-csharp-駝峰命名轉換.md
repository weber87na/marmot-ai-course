---
title: vibe coding csharp 駝峰命名轉換
date: 2026-01-19 12:12:15
tags: csharp
---
&nbsp;
<!-- more -->

朋友遇到的一個問題, 他有個大概兩千行的類別, 裡面有一坨欄位, 因為之前的工程師偷懶所以都用小寫當類別屬性 LOL ~
他希望把他轉為大寫駝峰, 就 vibe coding 搞看看
記得以前自己也弄過類似的功能, 不過是用 visual studio 燈泡的那種功能手動一個一個屬性去加
需要安裝 `SymSpell` `Microsoft.CodeAnalysis.CSharp`

```csharp
using System;
using System.IO;
using System.Linq;
using System.Text;
using System.Globalization;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace CodeRefactorTool
{
    class Program
    {
        static void Main(string[] args)
        {
            // 1. 初始化 SymSpell
            string dictPath = "frequency_dictionary_en_82_765.txt";
            var symSpell = new SymSpell(82765, 0);
            if (!symSpell.LoadDictionary(dictPath, 0, 1))
            {
                Console.WriteLine("錯誤：找不到詞典檔！");
                return;
            }

            // 2. 目標檔案路徑
            string filePath = @"shit_code.cs"; 

            if (!File.Exists(filePath))
            {
                Console.WriteLine($"檔案不存在：{filePath}");
                return;
            }

            ProcessFile(filePath, symSpell);
            Console.WriteLine("\n重構完成！註解已保留在最上方。");
            Console.ReadKey();
        }

        static void ProcessFile(string filePath, SymSpell symSpell)
        {
            string sourceCode = File.ReadAllText(filePath);
            SyntaxTree tree = CSharpSyntaxTree.ParseText(sourceCode);
            var root = (CompilationUnitSyntax)tree.GetCompilationUnitRoot();

            // 3. 自動補上 Using
            if (!root.Usings.Any(u => u.Name.ToString() == "System.Text.Json.Serialization"))
            {
                root = root.AddUsings(SyntaxFactory.UsingDirective(SyntaxFactory.ParseName("System.Text.Json.Serialization")));
            }

            // 4. 執行重寫
            var rewriter = new JsonAttributeTopRewriter(symSpell);
            var result = rewriter.Visit(root);

            File.WriteAllText(filePath, result.ToFullString(), Encoding.UTF8);
        }
    }

    class JsonAttributeTopRewriter : CSharpSyntaxRewriter
    {
        private readonly SymSpell _symSpell;
        private readonly TextInfo _textInfo = CultureInfo.InvariantCulture.TextInfo;

        public JsonAttributeTopRewriter(SymSpell symSpell) => _symSpell = symSpell;

        public override SyntaxNode VisitPropertyDeclaration(PropertyDeclarationSyntax node)
        {
            string propertyName = node.Identifier.Text;
            var symResult = _symSpell.WordSegmentation(propertyName);
            string pascalName = string.Concat(symResult.segmentedString.Split(' ').Select(w => _textInfo.ToTitleCase(w)));

            // 防止重複
            if (node.AttributeLists.Any(al => al.Attributes.Any(a => a.Name.ToString().Contains("JsonPropertyName"))))
                return node;

            // --- 核心邏輯：搬移註解 ---

            // 1. 取得原本整個節點最前方的 Trivia (包含 Summary 註解和縮排)
            var allLeadingTrivia = node.GetLeadingTrivia();
            
            // 2. 找到最後一段縮排 (用來給欄位本體對齊用)
            var lastWhitespace = allLeadingTrivia.LastOrDefault(t => t.IsKind(SyntaxKind.WhitespaceTrivia));

            // 3. 建立 [JsonPropertyName("...")]
            var attribute = SyntaxFactory.Attribute(SyntaxFactory.ParseName("JsonPropertyName"))
                .AddArgumentListArguments(SyntaxFactory.AttributeArgument(SyntaxFactory.ParseExpression($"\"{pascalName}\"")));
            
            // 將「所有註解」貼到這個新標籤的上方
            var newAttrList = SyntaxFactory.AttributeList(SyntaxFactory.SingletonSeparatedList(attribute))
                .WithLeadingTrivia(allLeadingTrivia)
                .WithTrailingTrivia(SyntaxFactory.EndOfLine("\r\n"));

            // 4. 處理原本的屬性列表
            // 如果原本就有 [Column] 等標籤，那些標籤上可能也帶著註解，我們要把它們清空，只留縮排
            var updatedAttributeLists = node.AttributeLists;
            if (updatedAttributeLists.Count > 0)
            {
                var firstList = updatedAttributeLists[0];
                updatedAttributeLists = updatedAttributeLists.Replace(firstList, firstList.WithLeadingTrivia(SyntaxFactory.TriviaList(lastWhitespace)));
            }

            // 5. 組裝新節點
            // 把原本 node 最前方的註解清掉（因為已經移到 JsonPropertyName 上了）
            var newNode = node.WithLeadingTrivia(SyntaxFactory.TriviaList(lastWhitespace))
                              .WithAttributeLists(updatedAttributeLists.Insert(0, newAttrList));

            return newNode;
        }
    }
}

```
