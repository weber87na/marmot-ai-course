使用方式

```powershell
cd D:\todo\todo-skill
uv sync
uv run todo-cli list
uv run todo-cli add "準備週報"
uv run todo-cli complete 7
uv run todo-cli edit 7 "完成週報"
uv run todo-cli update 7 --pending
uv run todo-cli health
```
