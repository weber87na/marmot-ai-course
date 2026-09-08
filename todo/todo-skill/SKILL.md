---
name: todo-skill
description: Use the reusable Python CLI to list, create, edit, complete, update, or delete tasks in the local Todo API, and check API health or inspect one task.
---

# Todo API CLI

Use the bundled `todo-cli` command to operate the local Todo service behind `http://localhost:5500/todo.html`.

Run commands from this skill directory with `uv run todo-cli ...`, or use `uv run python -m todo_cli ...` when the console script is not available. The default API base URL is `http://127.0.0.1:8000/api`; override it with `--base-url` or `TODO_API_BASE_URL`. `--json` can be placed before or after the subcommand for machine-readable output.

## Web app contract discovered by black-box inspection

The page loads its tasks with `GET /api/tasks`. Its visible actions map to these requests:

| UI action | HTTP request | JSON body |
| --- | --- | --- |
| Load the list | `GET /api/tasks` | — |
| Add task | `POST /api/tasks` | `{"text": "..."}` |
| Check/uncheck | `PUT /api/tasks/{id}` | `{"text": "...", "done": true/false}` |
| Edit text | `PUT /api/tasks/{id}` | full `text` + current `done` |
| Delete | `DELETE /api/tasks/{id}` | — |

The API also exposes `GET /health`, `GET /api/tasks/{id}`, and `PATCH /api/tasks/{id}`. They are useful CLI capabilities but are not called by the current page buttons.

Task text is trimmed and must contain 1–200 characters. A task response has `id`, `text`, and `done` fields. The CLI's `edit`, `complete`, `uncomplete`, and `toggle` commands intentionally use the page's full `PUT` replacement flow; `update` uses the API-only `PATCH` flow.

## Common commands

```text
uv run todo-cli list
uv run todo-cli add "準備週報"
uv run todo-cli edit 7 "準備並寄出週報"
uv run todo-cli complete 7
uv run todo-cli uncomplete 7
uv run todo-cli toggle 7
uv run todo-cli update 7 --text "新的文字" --done
uv run todo-cli get 7 --json
uv run todo-cli health
```

Deletion is guarded: use `delete ID` interactively or pass `delete ID --yes` only when the user explicitly wants that task removed. In scripts, prefer `--json` and check the process exit code.
