最後介紹怎麼把前端的資料保存到後端, 這裡為了方便所以使用 sqlite 這種檔案式資料庫, 實際環境會使用如 oracle, postgres, mssql, mariadb, mysql 這些重量級的服務

這裡需要使用 [sqlitebrowser](https://sqlitebrowser.org/) 這個免費的工具來建立資料庫

因為平常沒在用這種東西, 我有 vim 中毒, 所以 fork vibe coding 編譯了一個, 如果你也 vim 中讀的話可以用我[這個版本](https://github.com/weber87na/sqlitebrowser/releases/tag/vim-builtin-23)


```markdown
我現在已經有 [frontend](frontend/) 前端的 todo 網站, 你幫我規劃 [backend](backend/) 後端的功能, 使用 python fastapi + uv + sqlite 資料庫, CRUD 的功能都需要, 先製作後端的 api, 做完後建立一個新的 fronted\_with\_api 資料夾, 讓這個前端網頁去串接後端的 api, 功能盡量簡單即可
```

這裡 AI 幫我們進行了規劃, 這種簡單的需求使用 luna 即可, 規劃可以參考 [todo 規劃](todo/規劃.md)

````markdown

# Todo FastAPI 後端與 API 前端整合

## Summary

- 保留現有 `frontend/todo.html`，不修改。
- 建立 `backend/` 的 FastAPI + SQLite CRUD API。
- 同時提供：
  - `PUT`：完整替換任務
  - `PATCH`：部分更新任務
- 建立 `frontend_with_api/todo.html`，使用原生 JavaScript 串接 API。
- 前後端分開啟動。
- 不搬移既有 `localStorage` 資料。
- 單一使用者、無登入、無權限管理。

## Project files

```text
backend/
├─ pyproject.toml
├─ uv.lock
├─ .gitignore
├─ README.md
├─ app/
│  ├─ __init__.py
│  ├─ db.py
│  ├─ schemas.py
│  └─ main.py
├─ tests/
│  └─ test_tasks.py
└─ data/
   └─ todo.db              # 執行時自動建立，不納入版本控制

frontend_with_api/
└─ todo.html
```

`frontend/todo.html` 必須保持不變。

## Backend

### Dependencies

使用 `uv` 管理：

- `fastapi`
- `uvicorn[standard]`
- `pytest`
- `httpx`

Python 版本使用 3.12 以上。

### SQLite

使用 Python 標準庫 `sqlite3`，不使用 ORM。

資料庫位置：

```text
backend/data/todo.db
```

資料表：

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
        CHECK (length(trim(text)) BETWEEN 1 AND 200),
    done INTEGER NOT NULL DEFAULT 0
        CHECK (done IN (0, 1))
);
```

資料庫行為：

- 啟動 FastAPI 時自動建立資料夾與資料表。
- 每次操作使用短生命週期 SQLite connection。
- 啟用 `row_factory=sqlite3.Row`。
- 成功時 commit，例外時 rollback。
- SQL 一律使用參數化查詢。

### Pydantic schemas

建立以下資料模型：

#### `TaskCreate`

- `text: string`
- 必填
- 去除前後空白
- 長度限制 1–200
- 禁止額外欄位

#### `TaskReplace`

- `text: string`
- `done: boolean`
- 兩個欄位皆必填
- 用於 `PUT` 完整替換
- 禁止額外欄位

#### `TaskUpdate`

- `text: string`，可選
- `done: boolean`，可選
- 至少提供一個欄位
- 未提供的欄位保持原值
- 用於 `PATCH`

#### `TaskRead`

- `id: integer`
- `text: string`
- `done: boolean`

`done` 使用嚴格 boolean 驗證；`null`、空白文字與超過 200 字都回傳 `422`。

### App factory

提供：

```python
create_app(database_path=...)
```

正式環境使用：

```text
backend/data/todo.db
```

測試使用 pytest 暫存資料庫。

透過 FastAPI lifespan 在啟動時執行資料庫初始化。

## API

| 方法 | 路徑 | 行為 | 成功狀態 |
|---|---|---|---|
| `GET` | `/health` | 健康檢查 | `200` |
| `GET` | `/api/tasks` | 取得全部任務，依 `id` 升冪 | `200` |
| `GET` | `/api/tasks/{id}` | 取得單一任務 | `200` |
| `POST` | `/api/tasks` | 新增任務，`done=false` | `201` |
| `PUT` | `/api/tasks/{id}` | 完整替換 `text` 與 `done` | `200` |
| `PATCH` | `/api/tasks/{id}` | 部分更新 `text` 或 `done` | `200` |
| `DELETE` | `/api/tasks/{id}` | 永久刪除任務 | `204` |

### PUT 範例

```http
PUT /api/tasks/1
```

```json
{
  "text": "完成報告",
  "done": true
}
```

`PUT` 規則：

- 必須同時提供 `text` 與 `done`
- 會完整覆蓋原本任務內容
- 重複送出相同資料，結果必須一致

### PATCH 範例

```http
PATCH /api/tasks/1
```

```json
{
  "done": true
}
```

`PATCH` 規則：

- 只修改傳入的欄位
- 未傳入的欄位保持原值
- 空物件回傳 `422`

### 錯誤規則

- 任務不存在：`404`
- 輸入驗證失敗：`422`
- `PUT` 缺少 `text` 或 `done`：`422`
- `PATCH` 傳送空物件：`422`

## CORS

允許來源：

```text
http://localhost:5500
http://127.0.0.1:5500
```

允許方法：

```text
GET, POST, PUT, PATCH, DELETE, OPTIONS
```

## frontend_with_api

從現有 `frontend/todo.html` 複製樣式與中文介面，但移除所有 `localStorage` 讀寫。

API base URL：

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

功能：

- 頁面載入：`GET /api/tasks`
- 新增任務：`POST /api/tasks`
- 勾選或取消完成：
  - 使用 `PUT /api/tasks/{id}`
  - 傳送完整的 `text` 與 `done`
- 編輯文字：
  - 使用 `window.prompt()`
  - 使用 `PUT /api/tasks/{id}`
  - 傳送完整的 `text` 與 `done`
- 刪除任務：`DELETE /api/tasks/{id}`
- 使用 `textContent` 顯示任務文字。
- 顯示載入中、錯誤與連線失敗訊息。
- 顯示未完成任務數量。
- 不使用 `localStorage`。
- 不修改原本的 `frontend/todo.html`。

`PATCH` 保留在後端供其他 API client 使用，但目前 `frontend_with_api` 的更新操作統一使用 `PUT`。

## Tests

`backend/tests/test_tasks.py` 必須涵蓋：

- Health check
- 空列表查詢
- POST 新增任務
- GET 列表與單筆任務
- PUT 完整更新
- PUT 缺少欄位回傳 `422`
- PUT 內容驗證
- PUT 重複送出結果一致
- PATCH 部分更新
- PATCH 空 body 回傳 `422`
- 不存在任務回傳 `404`
- DELETE 後任務消失
- SQLite 資料重新建立 App 後仍存在
- PUT CORS 預檢請求

測試指令：

```powershell
cd backend
uv sync
uv run pytest
```

預期結果：

```text
12 passed
```

## 啟動方式

後端：

```powershell
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

前端另開終端機：

```powershell
cd D:\todo
python -m http.server 5500 --directory frontend_with_api
```

網址：

```text
前端：http://127.0.0.1:5500/todo.html
Swagger：http://127.0.0.1:8000/docs
Health：http://127.0.0.1:8000/health
```

## Assumptions

- 使用 `frontend_with_api` 作為新前端資料夾名稱。
- 不匯入既有 `localStorage` 任務。
- `PUT` 是完整替換。
- `PATCH` 是部分更新。
- 新前端的更新操作統一使用 `PUT`。
- 編輯文字使用簡單 `window.prompt()`。
- 不加入時間、分類、搜尋、登入、多使用者、分頁或軟刪除。
- 不刪除或重設既有 `backend/data/todo.db`，避免破壞現有任務資料。
````