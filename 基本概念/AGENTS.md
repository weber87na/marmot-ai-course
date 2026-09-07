# Rust/codex-rs

在存放 Rust 程式碼的 `codex-rs` 資料夾中：

* Crate 名稱都以 `codex-` 為前綴。例如，`core` 資料夾中的 crate 名稱是 `codex-core`。
* 使用 `format!` 時，只要可以把變數直接內嵌到 `{}` 中，就一律這麼做。
* 在執行此處的指示之前，如果儲存庫依賴的任何命令（例如 `just`、`rg` 或 `cargo-insta`）尚未安裝，請先安裝。
* 絕對不要新增或修改任何與 `CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR` 或 `CODEX_SANDBOX_ENV_VAR` 相關的程式碼。

  * 你是在沙箱環境中運作，每當使用 `shell` 工具時，都會設定 `CODEX_SANDBOX_NETWORK_DISABLED=1`。任何既有使用 `CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR` 的程式碼，都是作者在知道這項事實的前提下撰寫的。它通常用來讓作者明知因沙箱限制而無法執行的測試提早退出。
  * 同樣地，當你使用 Seatbelt（`/usr/bin/sandbox-exec`）啟動程序時，子程序會被設定 `CODEX_SANDBOX=seatbelt`。想要自行執行 Seatbelt 的整合測試無法在 Seatbelt 內執行，因此針對 `CODEX_SANDBOX=seatbelt` 的檢查，也常用來在適當情況下提早退出測試。
* 一律依照 https://rust-lang.github.io/rust-clippy/master/index.html#collapsible_if 合併可合併的 `if` 陳述式。
* 只要可能，一律依照 https://rust-lang.github.io/rust-clippy/master/index.html#uninlined_format_args 將 `format!` 的參數直接內嵌。
* 只要可能，優先使用方法參照而不是閉包，依照 https://rust-lang.github.io/rust-clippy/master/index.html#redundant_closure_for_method_calls。
* 避免使用 `bool` 或語意模糊的 `Option` 參數，因為這會迫使呼叫端寫出像 `foo(false)` 或 `bar(None)` 這種難以閱讀的程式碼。當 enum、具名方法、newtype 或其他慣用的 Rust API 形式能讓呼叫處本身更具自我說明性時，應優先使用這些方式。
* 當你無法進行上述 API 調整，但仍需要在 Rust 中使用少量位置式常值呼叫時，請遵循 `argument_comment_lint` 慣例：

  * 對於以位置傳入的 `None`、布林值與數字常值等不透明參數，請在參數前加入完全一致的 `/*param_name*/` 註解。
  * 如果某個方法唯一的非 `self` 參數，其方法名稱與參數名稱相同，則可豁免，例如 `.enabled(false)` 對應 `fn enabled(&self, enabled: bool)`。
  * 不要為字串或字元常值加上這類註解，除非註解確實能增加清晰度；這些常值刻意被排除在此 lint 之外。
  * 註解中的參數名稱必須與被呼叫函式的簽章完全一致。
  * 你可以執行 `just argument-comment-lint` 在本機執行 lint 檢查。這是由 Bazel 驅動，因此若 Bazel 尚未預熱，第一次執行可能較慢；之後的增量執行通常應少於 15 秒。大多數情況下，最好直接更新 PR，讓 CI 負責檢查（或在提交 PR 後於背景非同步執行）。請注意，CI 會檢查三個平台，而本機執行不會。
* 只要可能，讓 `match` 陳述式涵蓋所有情況，並避免使用萬用分支（wildcard arms）。
* 新增的 trait 應包含文件註解，說明其角色，以及實作者應如何使用它。
* 在 Rust trait 中，不建議使用 `#[async_trait]` 與 `#[allow(async_fn_in_trait)]`。

  * 優先使用原生 RPITIT trait 方法，並對回傳的 future 明確加上 `Send` 約束，如 `3c7f013f9735` / `#16630`。
  * 建議的 trait 形式：
    `fn foo(&self, ...) -> impl std::future::Future<Output = T> + Send;`
  * 實作端只要符合這份契約，仍然可以使用 `async fn foo(&self, ...) -> T`。
  * 不要把 `#[allow(async_fn_in_trait)]` 當成逃避明確寫出 future 契約的捷徑。
* 撰寫測試時，優先比較整個物件是否相等，而不是逐一比較欄位。
* 不要為靜態定義的值新增測試。
* 不要為已移除的邏輯新增負向測試。
* 不要把一般產品文件或面向使用者的文件加入 `docs/` 資料夾。Codex 的官方文件位於其他地方。例外是 app-server API 文件，相關規範見下方 app-server 指引。
* 優先使用私有模組，並明確匯出 crate 的公開 API。
* 如果你修改 `ConfigToml` 或其巢狀設定型別，請執行 `just write-config-schema`，以更新 `codex-rs/core/config.schema.json`。
* 處理 MCP 工具呼叫時，優先使用 `codex-rs/codex-mcp/src/mcp_connection_manager.rs` 來處理工具與工具呼叫的變更。目標是盡量縮小修改範圍，並善用既有抽象，而不是把程式碼一路穿透多層函式呼叫。
* 不要不必要地呼叫 `reset_client_session`；讓增量檢查邏輯自行決定是否重用上一個 request。
* 如果你修改 Rust 相依套件（`Cargo.toml` 或 `Cargo.lock`），請從儲存庫根目錄執行 `just bazel-lock-update`，
  以更新 `MODULE.bazel.lock`，並在同一次變更中一併提交這個 lockfile 更新。CI
  會檢查 lockfile 是否發生漂移。
* Bazel 不會自動讓來源樹中的檔案可供 Rust 在編譯期間存取。若你新增
  `include_str!`、`include_bytes!`、`sqlx::migrate!` 或類似的建置期間檔案／
  目錄讀取，請更新該 crate 的 `BUILD.bazel`（`compile_data`、`build_script_data` 或測試
  data），否則即使 Cargo 能通過，Bazel 仍可能失敗。
* 不要建立只會被引用一次的小型輔助方法。
* 若要追蹤非同步工作，應在函式或方法定義上使用
  `#[tracing::instrument(...)]`，而不是在呼叫處透過
  `.instrument(...)` 將 span 附加到 future 上。新增 instrumentation 前，請先確認被呼叫者——或
  它立即委派到的實作方法——是否已經有 instrumentation。
* 避免大型模組：

  * 優先新增模組，而不是持續擴充既有模組。
  * Rust 模組的目標應控制在 500 行程式碼（LoC）以下，不含測試。
  * 如果某個檔案超過約 800 LoC，請把新功能放到新模組，而不是繼續擴充
    既有檔案，除非有充分且已記錄的理由不這麼做。
  * 這項規則尤其適用於那些經常被修改、且容易吸引無關變更的檔案，例如
    `codex-rs/tui/src/app.rs`、`codex-rs/tui/src/bottom_pane/chat_composer.rs`、
    `codex-rs/tui/src/bottom_pane/footer.rs`、`codex-rs/tui/src/chatwidget.rs`、
    `codex-rs/tui/src/bottom_pane/mod.rs`，以及其他類似的核心協調模組。
  * 從大型模組抽離程式碼時，也應把相關測試與模組／型別文件一起移到
    新實作附近，讓不變條件（invariants）與擁有它們的程式碼保持接近。
  * 除非變更非常簡單，否則避免在 `codex-rs/tui/src/chatwidget.rs` 新增獨立方法；
    優先建立新模組／檔案，並讓 `chatwidget.rs` 專注於協調工作。
* 執行 Rust 命令（例如 `just fix` 或 `just test`）時請耐心等待，絕對不要嘗試用 PID 終止它們。Rust lock 可能讓執行速度變慢，這是正常現象。

在這個儲存庫中的任何位置完成程式碼修改後，都要自動在 `codex-rs` 目錄中執行 `just fmt`；不要詢問是否可以執行。此外，還要執行測試：

1. 不要直接執行 `cargo test`。請使用 `just test`，讓測試依照儲存庫的預設方式執行。
2. 執行被修改專案對應的測試。例如，如果修改了 `codex-rs/tui`，請執行 `just test -p codex-tui`。
3. 上述測試通過後，如果 common、core 或 protocol 有任何修改，請使用 `just test` 執行完整測試套件。一般本機執行時避免使用 `--all-features`，因為它會擴大建置矩陣，並可能大幅增加 `target/` 的磁碟用量；只有在確實需要完整 feature 覆蓋率時才使用。專案特定測試或單一測試可以不詢問使用者就執行，但在執行完整測試套件之前，要先詢問使用者。

在完成對 `codex-rs` 的大型變更之前，請在 `codex-rs` 目錄中執行 `just fix -p <project>`，修正程式碼中的 lint 問題。優先使用 `-p` 限定範圍，避免速度較慢的全 workspace Clippy 建置；只有在修改共用 crate 時，才執行不帶 `-p` 的 `just fix`。執行 `fix` 或 `fmt` 後，不要再次執行測試。

## `codex-core` crate

隨著時間推移，`codex-core` crate（定義於 `codex-rs/core/`）因為是最大的 crate 而逐漸膨脹。因此，人們常會覺得直接把新東西加進 `codex-core`，比起重構並抽出所需的函式庫程式碼更容易；但這樣會讓新程式碼既依賴 `codex-core`，又進一步增加 `codex-core` 的體積。

因此：**請克制，不要把程式碼加進 codex-core！**

尤其是在引入新的概念／功能／API 時，在加入 `codex-core` 之前，請先考慮：

* 是否已經存在 `codex-core` 以外的其他 crate，適合放置你的新程式碼。
* 是否到了該為新功能在 Cargo workspace 中建立新 crate 的時候。必要時重構既有程式碼，以便做到這一點。

同樣地，在進行程式碼審查時，對於會不必要地把程式碼加入 `codex-core` 的 PR，不要猶豫，應提出反對意見。

## 程式碼審查規則

### Crate API 表面

讓 crate 的 API 表面盡可能小。避免大量增加只供測試使用的 helper。

### 模型可見的上下文

Codex 會維護一份上下文（訊息歷史），並在推論 request 中傳送給模型。

1. 不得重寫歷史紀錄——上下文必須以增量方式逐步建立。
2. 避免頻繁修改上下文，以免造成快取未命中。
3. 不得有無上限項目——所有注入模型上下文的內容都必須有界限大小與明確硬上限。
4. 不得有任何單一項目超過 10K tokens。
5. 對於可能超過 >1k tokens 的新單一項目，要標記為 P0。這些項目需要額外人工審查。
6. 所有注入片段都必須在 `core/context` 中定義為 struct，並實作 `ContextualUserFragment` trait。

### 破壞性變更

請檢查外部整合介面是否有破壞性變更：

* app-server API
* 原始 response item 事件（`rawResponseItem/*`），即使仍屬實驗性功能
* CLI 參數
* 設定載入
* 從既有 rollout 恢復 session

### 測試撰寫指引

針對 Agent 的變更，優先使用整合測試而不是單元測試。整合測試位於 `core/suite`，並使用 `test_codex` 建立 Codex 測試執行個體。

凡是會改變 Agent 邏輯的功能，**必須**新增整合測試：

* 提供需要測試的主要邏輯變更與使用者可見行為清單。

如果需要單元測試，請放在專用的測試檔案（`*_tests.rs`）中。
避免在主要實作中加入只供測試使用的函式。

確認是否已有既有 helper，可以讓測試更精簡、更容易閱讀。

### 變更規模指引（800 行）

除非變更是機械式修改，否則總變更行數不應超過 800 行。
若是複雜邏輯變更，規模應控制在 500 行以下。

如果變更更大，請評估是否能拆成可審查的數個階段，並找出最小且邏輯完整、可優先合併的階段。
拆分建議必須根據實際 diff、相依關係與受影響的呼叫處來決定。

## TUI 樣式慣例

請參閱 `codex-rs/tui/styles.md`。

## TUI 程式碼慣例

* 使用 ratatui 的 `Stylize` trait 所提供的精簡樣式 helper。

  * 基本 span：使用 `"text".into()`
  * 有樣式的 span：使用 `"text".red()`、`"text".green()`、`"text".magenta()`、`"text".dim()` 等。
  * 優先使用這些方式，而不是直接用 `Span::styled` 與 `Style` 建立樣式。
  * 範例：patch 摘要中的檔案行

    * 建議寫法：`vec!["  └ ".into(), "M".red(), " ".dim(), "tui/src/app.rs".dim()]`

### TUI 樣式設定（ratatui）

* 優先使用 `Stylize` helper：只要可能，使用 `"text".dim()`、`.bold()`、`.cyan()`、`.italic()`、`.underlined()`，而不是手動建立 `Style`。
* 優先使用簡單轉換：span 使用 `"text".into()`，line 使用 `vec![…].into()`；當型別推論不明確時（例如 `Paragraph::new` / `Cell::from`），使用 `Line::from(spans)` 或 `Span::from(text)`。
* 計算出的樣式：若 `Style` 是在執行階段計算出來的，可以使用 `Span::styled`（`Span::from(text).set_style(style)` 也可以接受）。
* 避免硬編碼白色：不要使用 `.white()`；優先使用預設前景色（不指定顏色）。
* 鏈式呼叫：為了可讀性，透過 chaining 組合 helper（例如 `url.cyan().underlined()`）。
* 單一項目：優先使用 `"text".into()`；只有當目標型別無法從上下文明確判斷，或使用 `.into()` 需要額外型別註記時，才使用 `Line::from(text)` 或 `Span::from(text)`。
* 建立 line：當目標型別明確且不需要額外型別註記時，使用 `vec![…].into()` 建立 `Line`；否則使用 `Line::from(vec![…])`。
* 避免無謂變動：不要在等價形式之間（`Span::styled` ↔ `set_style`、`Line::from` ↔ `.into()`）重構，除非能明確提升可讀性或功能；遵循檔案既有慣例，也不要只為了滿足 `.into()` 而引入型別註記。
* 精簡性：優先選擇經過 rustfmt 後仍能維持單行的形式；如果 `Line::from(vec![…])` 或 `vec![…].into()` 只有其中一種能避免換行，就選那一種。若兩者都會換行，則選擇換行較少的寫法。

### 文字換行

* 一律使用 `textwrap::wrap` 對純字串進行換行。
* 如果你有 ratatui 的 `Line` 並想要換行，請使用 `tui/src/wrapping.rs` 中的 helper，例如 `word_wrap_lines` / `word_wrap_line`。
* 如果需要縮排換行後的行，若可行，請使用 `RtOptions` 的 `initial_indent` / `subsequent_indent` 選項，而不是自行撰寫邏輯。
* 如果有一串 line，需要在每一行前加上前綴（第一行與後續行可以選擇使用不同前綴），請使用 `line_utils` 中的 `prefix_lines` helper。

## 測試

### 測試模組組織方式

* 新增測試模組時，請把內容定義在獨立的同層檔案中，而不是直接內嵌於實作檔案。

* 使用明確的 `#[path = "..._tests.rs"]` 屬性，讓測試檔名具描述性且容易找到：

  ```rust
  #[cfg(test)]
  #[path = "parser_tests.rs"]
  mod tests;
  ```

* 這項規則只適用於新增測試模組時。不要只是為了遵循此慣例，就搬移或重寫既有的內嵌 `#[cfg(test)] mod tests { ... }` 模組。

### 快照測試

這個儲存庫會使用快照測試（透過 `insta`），尤其是在 `codex-rs/tui` 中，用來驗證渲染後的輸出。

**要求：**任何會影響使用者可見 UI 的變更（包含新增 UI），都必須加入
對應的 `insta` 快照覆蓋（如果尚未有快照測試就新增一個，否則
更新既有快照）。PR 中應一併審查並接受快照更新，讓 UI 影響
容易檢視，且未來的 diff 能維持視覺化。

當 UI 或文字輸出是有意變更時，請依下列方式更新快照：

* 執行測試以產生所有更新後的快照：

  * `just test -p codex-tui`
* 檢查有哪些待處理快照：

  * `cargo insta pending-snapshots -p codex-tui`
* 直接讀取儲存庫中產生的 `*.snap.new` 檔案來審查變更，或預覽特定檔案：

  * `cargo insta show -p codex-tui path/to/file.snap.new`
* 只有在你確定要接受這個 crate 中所有新快照時，才執行：

  * `cargo insta accept -p codex-tui`

如果你沒有這個工具：

* `cargo install --locked cargo-insta`

### Benchmark

可以使用 `just bench` 執行 cargo benchmark；新增 benchmark 時使用 divan crate 撰寫。

使用 `just bench-smoke` 以單次迭代方式試跑 benchmark，確認它能正常運作。

### 測試斷言

* 測試應使用 `pretty_assertions::assert_eq`，以取得更清楚的 diff。如果測試模組頂端尚未匯入，請加上它。
* 只要可能，優先進行深層相等比較。對整個物件執行 `assert_eq!()`，不要只比較個別欄位。
* 避免在測試中修改程序環境；優先從上層傳入由環境衍生的旗標或相依項目。

### 在測試中啟動 workspace binary（Cargo vs Bazel）

* 當測試需要啟動第一方 binary 時，優先使用 `codex_utils_cargo_bin::cargo_bin("...")`，而不是 `assert_cmd::Command::cargo_bin(...)` 或 `escargot`。

  * 在 Bazel 下，binary 與資源可能位於 runfiles 中；請使用 `codex_utils_cargo_bin::cargo_bin` 解析絕對路徑，確保在 `chdir` 後路徑仍保持穩定。
* 在 Bazel 下尋找 fixture 檔案或測試資源時，避免使用 `env!("CARGO_MANIFEST_DIR")`。優先使用 `codex_utils_cargo_bin::find_resource!`，讓路徑能在 Cargo 與 Bazel runfiles 兩種情況下都正確解析。

### 整合測試

#### `codex_core` 整合測試

* 撰寫 Codex 端對端測試時，優先使用 `core_test_support::responses` 中的工具。

* 預設使用 `TestCodexBuilder::build_with_auto_env()`，以確保新測試能在
  不同的 app/exec 作業系統上運作。詳情請參閱 `$remote-tests`。

* 所有 `mount_sse*` helper 都會回傳 `ResponseMock`；請保留它，以便對送出的 `/responses` POST body 進行斷言。

* 當測試只應發出一次 POST 時，使用 `ResponseMock::single_request()`；若要檢查所有捕捉到的 `ResponsesRequest`，則使用 `ResponseMock::requests()`。

* `ResponsesRequest` 提供 helper（`body_json`、`input`、`function_call_output`、`custom_tool_call_output`、`call_output`、`header`、`path`、`query_param`），因此斷言可以直接針對結構化 payload，而不必手動深入查找 JSON。

* 使用提供的 `ev_*` 建構函式與 `sse(...)` 建立 SSE payload。

* 優先使用 `wait_for_event`，而不是 `wait_for_event_with_timeout`。

* 優先使用 `mount_sse_once`，而不是 `mount_sse_once_match` 或 `mount_sse_sequence`。

* 典型模式：

  ```rust
  let mock = responses::mount_sse_once(&server, responses::sse(vec![
      responses::ev_response_created("resp-1"),
      responses::ev_function_call(call_id, "shell", &serde_json::to_string(&args)?),
      responses::ev_completed("resp-1"),
  ])).await;

  codex.submit(Op::UserTurn { ... }).await?;

  // 如有需要，對 request body 進行斷言。
  let request = mock.single_request();
  // 使用 request.function_call_output(call_id)、request.json_body() 或其他 helper 進行斷言。
  ```

#### app-server 整合測試

* 測試應涵蓋 app-server 的公開 JSON-RPC API。
* 使用與 core 整合測試類似的 server mocking 方式。
* 預設使用 `TestAppServer::builder().build()` 與 `TestAppServer::send_thread_start_request_with_auto_env()`，
  以確保新測試能在不同的 app/exec 作業系統上運作。詳情請參閱 `$remote-tests`。

## App-server API 開發最佳實務

這些指引適用於 `codex-rs` 中的 app-server protocol 工作，尤其是：

* `app-server-protocol/src/protocol/common.rs`
* `app-server-protocol/src/protocol/v2.rs`
* `app-server/README.md`

### 核心規則

* 所有進行中的 API 開發都應在 app-server v2 進行。不要再向 v1 新增 API 表面。
* payload 命名應保持一致：
  request payload 使用 `*Params`，response 使用 `*Response`，notification 使用 `*Notification`。
* RPC 方法公開為 `<resource>/<method>`，且 `<resource>` 保持單數形式（例如 `thread/read`、`app/list`）。
* 除非 tagged union 或明確的相容性需求需要針對性重新命名，否則在線上傳輸格式中，欄位一律使用 camelCase，並加上 `#[serde(rename_all = "camelCase")]`。
* 除非明確的相容性需求需要針對性重新命名，否則在線上傳輸格式中，字串 enum 值一律使用 camelCase，並搭配 serde 與 TS 的 `rename_all = "camelCase"` 註記。
* 例外：config RPC payload 預期使用 snake_case，以對應 `config.toml` 的 key（請參閱 `app-server-protocol/src/protocol/v2.rs` 中的 config read/write/list API）。
* v2 request/response/notification 型別一律設定 `#[ts(export_to = "v2/")]`，讓產生的 TypeScript 放到正確 namespace。
* v2 API payload 欄位絕對不要使用 `#[serde(skip_serializing_if = "Option::is_none")]`。
  例外：刻意不帶 params 的 client->server request 可以使用：
  `params: #[ts(type = "undefined")] #[serde(skip_serializing_if = "Option::is_none")] Option<()>`。
* 保持 Rust 與 TS 的線上重新命名一致。如果欄位或 variant 使用 `#[serde(rename = "...")]`，就加入對應的 `#[ts(rename = "...")]`。
* 對於 discriminated union，兩個 serializer 都使用明確 tag：
  `#[serde(tag = "type", ...)]` 與 `#[ts(tag = "type", ...)]`。
* API 邊界上的 ID 優先使用單純的 `String`（若需要 UUID 解析／轉換，放在內部處理）。
* timestamp 應為整數 Unix 秒數（`i64`），並命名為 `*_at`（例如 `created_at`、`updated_at`、`resets_at`）。
* 對於實驗性 API 表面：
  使用 `#[experimental("method/or/field")]`；如果需要欄位層級 gating，derive `ExperimentalApi`；如果某個方法只有部分欄位屬於實驗性，則在 `common.rs` 中使用 `inspect_params: true`。

### Client->server request payload（`*Params`）

* 每個 optional 欄位都必須加上 `#[ts(optional = nullable)]`。不要在 client->server request payload（`*Params`）之外使用 `#[ts(optional = nullable)]`。
* optional collection 欄位（例如 `Vec`、`HashMap`）必須使用 `Option<...>` + `#[ts(optional = nullable)]`。不要使用 `#[serde(default)]` 來表示 optional collection，也不要在 v2 payload 欄位使用 `skip_serializing_if`。
* 當你希望布林欄位省略時代表 `false`，請使用 `#[serde(default, skip_serializing_if = "std::ops::Not::not")] pub field: bool`，而不是 `Option<bool>`。
* 對於新的 list 方法，預設實作 cursor pagination：
  request 欄位為 `pub cursor: Option<String>` 與 `pub limit: Option<u32>`，
  response 欄位為 `pub data: Vec<...>` 與 `pub next_cursor: Option<String>`。

### 開發流程

* API 行為改變時，請更新 app-server 文件／範例（至少要更新 `app-server/README.md`）。
* API 結構改變時，重新產生 schema fixture：
  `just write-app-server-schema`
  （如果影響實驗性 API fixture，還要執行 `just write-app-server-schema --experimental`）。
* 使用 `just test -p codex-app-server-protocol` 驗證。
* 避免加入只用來斷言 `common.rs` 中個別 request 欄位實驗性標記的樣板測試；應改為依賴 schema 產生／測試以及行為覆蓋。

## Python 開發最佳實務

### 不考慮 Python 2 相容性

本專案使用 Python 3+。不應使用 `__future__` 模組。

如果需要考量不同 3.xx 小版本之間的功能相容性，請檢查
最近的 `pyproject.toml` 中 `requires-python` 欄位，以確認支援的最低執行階段版本。

## 平台支援

除非某項功能明確限定於特定作業系統，否則測試與功能都必須支援 Linux、macOS 與 Windows。

Codex 支援讓彼此連線的 app-server 與 exec-server 執行在不同作業系統上。關於這類組態的整合測試詳情，請參閱
`$remote-tests` skill。
