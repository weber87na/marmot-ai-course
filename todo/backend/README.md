# Todo API

## Install dependencies

```powershell
uv sync
```

## Run the API

```powershell
uv run uvicorn app.main:app --reload --port 8000
```

The API is available at `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`
- SQLite database: `backend/data/todo.db`

Task update endpoints:

- `PUT /api/tasks/{id}` replaces both `text` and `done`.
- `PATCH /api/tasks/{id}` updates only the fields provided.

## Run tests

```powershell
uv run pytest
```
