from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from .db import DEFAULT_DATABASE_PATH, connect, init_db
from .schemas import TaskCreate, TaskRead, TaskReplace, TaskUpdate


ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]


def row_to_task(row: Any) -> TaskRead:
    return TaskRead(
        id=row["id"],
        text=row["text"],
        done=bool(row["done"]),
    )


def task_not_found(task_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found",
    )


def create_app(database_path: Path | str = DEFAULT_DATABASE_PATH) -> FastAPI:
    database_path = Path(database_path)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        init_db(database_path)
        app.state.database_path = database_path
        yield

    app = FastAPI(
        title="Todo API",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/tasks", response_model=list[TaskRead])
    def list_tasks() -> list[TaskRead]:
        with connect(database_path) as connection:
            rows = connection.execute(
                "SELECT id, text, done FROM tasks ORDER BY id ASC"
            ).fetchall()
        return [row_to_task(row) for row in rows]

    @app.get("/api/tasks/{task_id}", response_model=TaskRead)
    def get_task(task_id: int) -> TaskRead:
        with connect(database_path) as connection:
            row = connection.execute(
                "SELECT id, text, done FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()

        if row is None:
            raise task_not_found(task_id)
        return row_to_task(row)

    @app.post(
        "/api/tasks",
        response_model=TaskRead,
        status_code=status.HTTP_201_CREATED,
    )
    def create_task(payload: TaskCreate) -> TaskRead:
        with connect(database_path) as connection:
            cursor = connection.execute(
                "INSERT INTO tasks (text, done) VALUES (?, ?)",
                (payload.text, 0),
            )
            row = connection.execute(
                "SELECT id, text, done FROM tasks WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()

        return row_to_task(row)

    @app.put("/api/tasks/{task_id}", response_model=TaskRead)
    def replace_task(task_id: int, payload: TaskReplace) -> TaskRead:
        with connect(database_path) as connection:
            existing = connection.execute(
                "SELECT id FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()
            if existing is None:
                raise task_not_found(task_id)

            connection.execute(
                "UPDATE tasks SET text = ?, done = ? WHERE id = ?",
                (payload.text, int(payload.done), task_id),
            )
            row = connection.execute(
                "SELECT id, text, done FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()

        return row_to_task(row)

    @app.patch("/api/tasks/{task_id}", response_model=TaskRead)
    def update_task(task_id: int, payload: TaskUpdate) -> TaskRead:
        update_columns: list[str] = []
        update_values: list[object] = []

        if "text" in payload.model_fields_set:
            update_columns.append("text = ?")
            update_values.append(payload.text)
        if "done" in payload.model_fields_set:
            update_columns.append("done = ?")
            update_values.append(int(payload.done))

        with connect(database_path) as connection:
            existing = connection.execute(
                "SELECT id FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()
            if existing is None:
                raise task_not_found(task_id)

            update_values.append(task_id)
            connection.execute(
                f"UPDATE tasks SET {', '.join(update_columns)} WHERE id = ?",
                update_values,
            )
            row = connection.execute(
                "SELECT id, text, done FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()

        return row_to_task(row)

    @app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_task(task_id: int) -> Response:
        with connect(database_path) as connection:
            existing = connection.execute(
                "SELECT id FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()
            if existing is None:
                raise task_not_found(task_id)

            connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app


app = create_app()
