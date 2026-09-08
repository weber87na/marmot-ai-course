"""HTTP client for the Todo API discovered from the local web app."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen


DEFAULT_API_BASE_URL = "http://127.0.0.1:8000/api"
DEFAULT_TIMEOUT = 10.0
MAX_TASK_TEXT_LENGTH = 200

Task = dict[str, Any]
Opener = Callable[..., Any]


class TodoClientError(RuntimeError):
    """Raised for local client validation or transport failures."""


class TodoApiError(TodoClientError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        payload: Any = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.payload = payload


def normalize_task_text(text: str) -> str:
    """Apply the same trim and length rules as the web UI/API contract."""

    normalized = text.strip()
    if not normalized:
        raise TodoClientError("任務內容不能是空白。")
    if len(normalized) > MAX_TASK_TEXT_LENGTH:
        raise TodoClientError(f"任務內容最多 {MAX_TASK_TEXT_LENGTH} 個字。")
    return normalized


def _decode_json(raw: bytes) -> Any:
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return raw.decode("utf-8", errors="replace")


def _detail_from_payload(payload: Any, status: int) -> str:
    if isinstance(payload, dict) and "detail" in payload:
        detail = payload["detail"]
        if isinstance(detail, list):
            messages = [
                str(item.get("msg"))
                for item in detail
                if isinstance(item, dict) and item.get("msg")
            ]
            if messages:
                return "；".join(messages)
        elif detail:
            return str(detail)
    if isinstance(payload, str) and payload:
        return payload
    return f"伺服器錯誤（{status}）"


def infer_server_url(api_base_url: str) -> str:
    """Infer the server root used by GET /health from an /api base URL."""

    parsed = urlsplit(api_base_url.rstrip("/"))
    path = parsed.path.rstrip("/")
    if path.lower().endswith("/api"):
        path = path[:-4] or "/"
    return urlunsplit((parsed.scheme, parsed.netloc, path, "", "")).rstrip("/")


@dataclass
class TodoClient:
    """A minimal JSON client for the local Todo service."""

    base_url: str = DEFAULT_API_BASE_URL
    server_url: str | None = None
    timeout: float = DEFAULT_TIMEOUT
    opener: Opener = urlopen

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        if not self.base_url:
            raise TodoClientError("API base URL 不能是空白。")
        self.server_url = (self.server_url or infer_server_url(self.base_url)).rstrip("/")

    def _request_url(
        self,
        url: str,
        *,
        method: str = "GET",
        payload: Any = None,
    ) -> Any:
        body = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = Request(url, data=body, headers=headers, method=method)
        try:
            with self.opener(request, timeout=self.timeout) as response:
                status = int(response.status)
                raw = response.read()
        except HTTPError as error:
            raw = error.read()
            payload_data = _decode_json(raw)
            raise TodoApiError(
                _detail_from_payload(payload_data, error.code),
                status=error.code,
                payload=payload_data,
            ) from error
        except URLError as error:
            reason = getattr(error, "reason", error)
            raise TodoClientError(f"無法連線到 Todo API：{reason}") from error
        except TimeoutError as error:
            raise TodoClientError("Todo API 連線逾時。") from error

        payload_data = _decode_json(raw)
        if status >= 400:
            raise TodoApiError(
                _detail_from_payload(payload_data, status),
                status=status,
                payload=payload_data,
            )
        return payload_data

    def _request(self, path: str, *, method: str = "GET", payload: Any = None) -> Any:
        return self._request_url(f"{self.base_url}{path}", method=method, payload=payload)

    def health(self) -> dict[str, Any]:
        result = self._request_url(f"{self.server_url}/health")
        if not isinstance(result, dict):
            raise TodoClientError("Health API 回傳格式不是 JSON 物件。")
        return result

    def list_tasks(self) -> list[Task]:
        result = self._request("/tasks")
        if not isinstance(result, list):
            raise TodoClientError("任務清單 API 回傳格式不是 JSON 陣列。")
        return result

    def get_task(self, task_id: int) -> Task:
        result = self._request(f"/tasks/{task_id}")
        if not isinstance(result, dict):
            raise TodoClientError("任務 API 回傳格式不是 JSON 物件。")
        return result

    def create_task(self, text: str) -> Task:
        result = self._request("/tasks", method="POST", payload={"text": normalize_task_text(text)})
        if not isinstance(result, dict):
            raise TodoClientError("新增任務 API 回傳格式不是 JSON 物件。")
        return result

    def replace_task(self, task_id: int, text: str, done: bool) -> Task:
        result = self._request(
            f"/tasks/{task_id}",
            method="PUT",
            payload={"text": normalize_task_text(text), "done": bool(done)},
        )
        if not isinstance(result, dict):
            raise TodoClientError("更新任務 API 回傳格式不是 JSON 物件。")
        return result

    def edit_task(self, task_id: int, text: str) -> Task:
        current = self.get_task(task_id)
        return self.replace_task(task_id, text, bool(current.get("done", False)))

    def set_done(self, task_id: int, done: bool) -> Task:
        current = self.get_task(task_id)
        text = current.get("text")
        if not isinstance(text, str):
            raise TodoClientError("任務資料缺少有效的 text 欄位。")
        return self.replace_task(task_id, text, done)

    def toggle_done(self, task_id: int) -> Task:
        current = self.get_task(task_id)
        text = current.get("text")
        if not isinstance(text, str):
            raise TodoClientError("任務資料缺少有效的 text 欄位。")
        return self.replace_task(task_id, text, not bool(current.get("done", False)))

    def update_task(
        self,
        task_id: int,
        *,
        text: str | None = None,
        done: bool | None = None,
    ) -> Task:
        if text is None and done is None:
            raise TodoClientError("至少要提供 --text、--done 或 --pending 其中一項。")
        payload: dict[str, Any] = {}
        if text is not None:
            payload["text"] = normalize_task_text(text)
        if done is not None:
            payload["done"] = done
        result = self._request(f"/tasks/{task_id}", method="PATCH", payload=payload)
        if not isinstance(result, dict):
            raise TodoClientError("部分更新 API 回傳格式不是 JSON 物件。")
        return result

    def delete_task(self, task_id: int) -> None:
        result = self._request(f"/tasks/{task_id}", method="DELETE")
        if result is not None:
            raise TodoClientError("刪除任務 API 回傳了非預期內容。")
