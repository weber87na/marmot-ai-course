---
title: vibe coding vs2022 postfix
date: 2026-01-05 18:42:14
tags:
---
&nbsp;
<!-- more -->

剛學 vim 的時候很喜歡 resharper 上面 postfix 的功能, 現在這個功能在 vscode 上面可以說是爛大街, 可是在 visual studio 上面始終沒有看到
幾年前曾經自己開發過 `.var` `.return` 這兩個功能, 後來因為操作失誤導致 code 不見了, 就再也沒去搞這些, 最近想說跟風 vibe coding 來做看看
沒想到還真行!


<iframe width="1242" height="735" src="https://www.youtube.com/embed/-LQhDgXsZhI" title="Vibe Coding Visual Studio Marmot Postfix Completion" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


我已經上架到 [marketplace](https://marketplace.visualstudio.com/items?itemName=weber87na.MarmotPostfixCompletion) 雖然用起來還很陽春, 但還可以過得去啦 LOL


```csharp
using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.ComponentModel.Composition;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.Text;
using Microsoft.CodeAnalysis.Formatting;
using Microsoft.VisualStudio.Language.Intellisense.AsyncCompletion;
using Microsoft.VisualStudio.Language.Intellisense.AsyncCompletion.Data;
using Microsoft.VisualStudio.Text;
using Microsoft.VisualStudio.Text.Editor;
using Microsoft.VisualStudio.Utilities;
using Microsoft.VisualStudio.ComponentModelHost;
using Microsoft.VisualStudio.LanguageServices;
using Microsoft.VisualStudio.Shell;
using Microsoft.VisualStudio.Imaging;
using Microsoft.VisualStudio.Core.Imaging;
using Microsoft.VisualStudio.Text.Adornments;

namespace MarmotPostfixCompletion
{
    [Export(typeof(IAsyncCompletionSourceProvider))]
    [Export(typeof(IAsyncCompletionCommitManagerProvider))]
    [Name("Marmot Postfix Completion")]
    [ContentType("CSharp")]
    public class MarmotPostfixProvider : IAsyncCompletionSourceProvider, IAsyncCompletionCommitManagerProvider
    {
        IAsyncCompletionSource IAsyncCompletionSourceProvider.GetOrCreate(ITextView textView) => new PostfixCompletionSource();
        IAsyncCompletionCommitManager IAsyncCompletionCommitManagerProvider.GetOrCreate(ITextView textView) => new PostfixCommitManager();
    }

    public class PostfixCompletionSource : IAsyncCompletionSource
    {
        public CompletionStartData InitializeCompletion(CompletionTrigger trigger, SnapshotPoint triggerLocation, CancellationToken token)
        {
            return trigger.Character == '.'
                ? new CompletionStartData(CompletionParticipation.ProvidesItems, new SnapshotSpan(triggerLocation, 0))
                : new CompletionStartData(CompletionParticipation.DoesNotProvideItems, default(SnapshotSpan));
        }

        public async Task<CompletionContext> GetCompletionContextAsync(IAsyncCompletionSession session, CompletionTrigger trigger, SnapshotPoint triggerLocation, SnapshotSpan applicableToSpan, CancellationToken token)
        {
            var componentModel = (IComponentModel)Package.GetGlobalService(typeof(SComponentModel));
            var workspace = componentModel.GetService<VisualStudioWorkspace>();
            var buffer = triggerLocation.Snapshot.TextBuffer;
            var container = buffer.AsTextContainer();
            var documentId = workspace.GetDocumentIdInCurrentContext(container);
            if (documentId == null) return CompletionContext.Empty;

            var document = workspace.CurrentSolution.GetDocument(documentId);
            var root = await document.GetSyntaxRootAsync(token);
            var semanticModel = await document.GetSemanticModelAsync(token);

            var position = triggerLocation.Position;
            var tokenAtPos = root.FindToken(position - 1);

            ExpressionSyntax expression = (tokenAtPos.IsKind(SyntaxKind.DotToken) && tokenAtPos.Parent is MemberAccessExpressionSyntax mae)
                ? mae.Expression
                : tokenAtPos.Parent?.AncestorsAndSelf().OfType<ExpressionSyntax>().FirstOrDefault(e => e.Span.End == position - 1);

            if (expression == null || expression.SpanStart >= position - 1) return CompletionContext.Empty;

            var typeInfo = semanticModel.GetTypeInfo(expression, token);
            var symbolInfo = semanticModel.GetSymbolInfo(expression, token);
            var items = ImmutableArray.CreateBuilder<CompletionItem>();

            // --- 加入重複項守衛 ---
            var addedKeys = new HashSet<string>();

            void Add(string name)
            {
                // 如果已經加過這個關鍵字，直接跳過，防止重複出現
                if (addedKeys.Contains(name)) return;

                var icon = new ImageElement(KnownMonikers.Snippet.ToImageId());
                var item = new CompletionItem(
                    displayText: name,
                    source: this,
                    icon: icon,
                    filters: ImmutableArray<CompletionFilter>.Empty,
                    suffix: "(postfix)",
                    insertText: name,
                    sortText: name,
                    filterText: name,
                    automationText: name,
                    attributeIcons: ImmutableArray<ImageElement>.Empty);

                item.Properties.AddProperty("Type", name);
                item.Properties.AddProperty("Expr", expression.ToString());
                item.Properties.AddProperty("Start", expression.SpanStart);

                items.Add(item);
                addedKeys.Add(name); // 標記為已加入
            }

            var type = typeInfo.Type;
            bool isVoid = type?.SpecialType == SpecialType.System_Void;
            bool isBool = type?.SpecialType == SpecialType.System_Boolean;
            bool isString = type?.SpecialType == SpecialType.System_String;
            bool isEnumerable = IsEnumerable(type);
            bool isTask = type?.Name.Contains("Task") == true;

            // 1. 通用模板 (只要不是 void)
            if (!isVoid && type != null)
            {
                Add("var"); Add("return"); Add("yield"); Add("par"); Add("arg");
                Add("cast"); Add("field"); Add("prop"); Add("to"); Add("throw");
                Add("using"); Add("lock"); Add("switch"); Add("sel");
            }

            // 2. 布林專屬
            if (isBool)
            {
                Add("if"); Add("else"); Add("not"); Add("while");
            }

            // 3. 集合專屬
            if (isEnumerable)
            {
                Add("foreach"); Add("for"); Add("forr");
            }

            // 4. 非同步專屬
            if (isTask) Add("await");

            // 5. 引用型別/可空
            if (type?.IsReferenceType == true || (type?.OriginalDefinition.SpecialType == SpecialType.System_Nullable_T))
            {
                Add("null"); Add("notnull");
            }

            // 6. 字串專屬
            if (isString)
            {
                Add("parse"); Add("tryparse");
            }

            // 7. 型別/類別符號專屬
            if (symbolInfo.Symbol is ITypeSymbol)
            {
                Add("new"); Add("typeof"); Add("inject");
            }

            return new CompletionContext(items.ToImmutable());
        }

        private bool IsEnumerable(ITypeSymbol t) => t != null && (t.SpecialType == SpecialType.System_Collections_IEnumerable || t.AllInterfaces.Any(i => i.SpecialType == SpecialType.System_Collections_IEnumerable));
        public Task<object> GetDescriptionAsync(IAsyncCompletionSession s, CompletionItem i, CancellationToken t) => Task.FromResult<object>(i.DisplayText);
    }

    public class PostfixCommitManager : IAsyncCompletionCommitManager
    {
        public IEnumerable<char> PotentialCommitCharacters => new[] { '\t', '\n', '\r' };
        public bool ShouldCommitCompletion(IAsyncCompletionSession s, SnapshotPoint l, char c, CancellationToken t) => true;
        public CommitResult GetNextContext(IAsyncCompletionSession s, CompletionItem i, char c, CancellationToken t) => CommitResult.Unhandled;

        public CommitResult TryCommit(IAsyncCompletionSession session, ITextBuffer buffer, CompletionItem item, char typedChar, CancellationToken token)
        {
            if (!item.Properties.TryGetProperty("Type", out string type) || !item.Properties.TryGetProperty("Expr", out string expr) || !item.Properties.TryGetProperty("Start", out int start))
                return CommitResult.Unhandled;

            var snapshot = buffer.CurrentSnapshot;
            var endPos = session.ApplicableToSpan.GetEndPoint(snapshot).Position;
            var replaceSpan = new Span(start, endPos - start);

            string r = GetReplacement(type, expr);
            if (r == null) return CommitResult.Unhandled;

            using (var edit = buffer.CreateEdit())
            {
                edit.Replace(replaceSpan, r);
                edit.Apply();
            }

            FormatRange(buffer, start, r.Length);

            if (type == "sel")
            {
                session.TextView.Selection.Select(new SnapshotSpan(buffer.CurrentSnapshot, start, expr.Length), false);
            }

            return CommitResult.Handled;
        }

        private string GetReplacement(string type, string expr)
        {
            switch (type)
            {
                case "arg": return $"Method({expr})";
                case "await": return $"await {expr}";
                case "cast": return $"((SomeType){expr})";
                case "else": return $"if (!({expr}))\r\n{{\r\n}}";
                case "field": return $"_field = {expr};";
                case "for": return $"for (var i = 0; i < {expr}.Length; i++)\r\n{{\r\n}}";
                case "foreach": return $"foreach (var x in {expr})\r\n{{\r\n}}";
                case "forr": return $"for (var i = {expr}.Length - 1; i >= 0; i--)\r\n{{\r\n}}";
                case "if": return $"if ({expr})\r\n{{\r\n}}";
                case "inject": return $"public class Component(IType {expr})";
                case "lock": return $"lock ({expr})\r\n{{\r\n}}";
                case "new": return $"new {expr}()";
                case "not": return $"!({expr})";
                case "notnull": return $"if ({expr} != null)\r\n{{\r\n}}";
                case "null": return $"if ({expr} == null)\r\n{{\r\n}}";
                case "par": return $"({expr})";
                case "parse": return $"int.Parse({expr})";
                case "prop": return $"public IType Property {{ get; set; }} = {expr};";
                case "return": return $"return {expr};";
                case "sel": return expr;
                case "switch": return $"switch ({expr})\r\n{{\r\n}}";
                case "throw": return $"throw {expr};";
                case "to": return $"lvalue = {expr};";
                case "tryparse": return $"int.TryParse({expr}, out var value)";
                case "typeof": return $"typeof({expr})";
                case "using": return $"using (var x = {expr})\r\n{{\r\n}}";
                case "var": return $"var x = {expr};";
                case "while": return $"while ({expr})\r\n{{\r\n}}";
                case "yield": return $"yield return {expr};";
                default: return null;
            }
        }

        private void FormatRange(ITextBuffer buffer, int start, int length)
        {
            ThreadHelper.JoinableTaskFactory.Run(async () =>
            {
                var componentModel = (IComponentModel)Package.GetGlobalService(typeof(SComponentModel));
                var workspace = componentModel.GetService<VisualStudioWorkspace>();
                var document = buffer.CurrentSnapshot.GetOpenDocumentInCurrentContextWithChanges();
                if (document == null) return;
                var newDocument = await Formatter.FormatAsync(document, new TextSpan(start, length));
                workspace.TryApplyChanges(newDocument.Project.Solution);
            });
        }
    }
}
```


後來又弄了一個 [Hippie Completion](https://marketplace.visualstudio.com/items?itemName=weber87na.MarmotHippieCompletion) 感覺這個實作還算是不錯

順帶一提這次錄影順便改成 [keyviz](https://mularahul.github.io/keyviz/) 感覺效果滿漂亮的

<iframe width="1242" height="735" src="https://www.youtube.com/embed/qkDf-FfNEwc" title="Vibe Coding Visual Studio Marmot Hippie Completion" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>




