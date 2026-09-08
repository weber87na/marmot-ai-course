from __future__ import annotations

import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from todo_cli.client import TodoApiError, TodoClient, TodoClientError, infer_server_url


class FakeTodoHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    calls: list[tuple[str, str, object]] = []

    def log_message(self, format: str, *args: object) -> None:
        return

    def _body(self) -> object:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8")) if raw else None

    def _send(self, status: int, payload: object = None) -> None:
        raw = b"" if payload is None else json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        if raw:
            self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        FakeTodoHandler.calls.append(("GET", path, None))
        if path == "/health":
            self._send(200, {"status": "ok"})
        elif path == "/api/tasks":
            self._send(200, [{"id": 1, "text": "one", "done": False}])
        elif path == "/api/tasks/1":
            self._send(200, {"id": 1, "text": "one", "done": False})
        else:
            self._send(404, {"detail": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        body = self._body()
        FakeTodoHandler.calls.append(("POST", path, body))
        self._send(201, {"id": 2, "text": body["text"], "done": False})

    def do_PUT(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        body = self._body()
        FakeTodoHandler.calls.append(("PUT", path, body))
        self._send(200, {"id": 1, **body})

    def do_PATCH(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        body = self._body()
        FakeTodoHandler.calls.append(("PATCH", path, body))
        self._send(200, {"id": 1, "text": body.get("text", "one"), "done": body.get("done", False)})

    def do_DELETE(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        FakeTodoHandler.calls.append(("DELETE", path, None))
        self._send(204)


class TodoClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        FakeTodoHandler.calls = []
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeTodoHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.root = f"http://127.0.0.1:{cls.server.server_port}"
        cls.client = TodoClient(base_url=f"{cls.root}/api")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def setUp(self) -> None:
        FakeTodoHandler.calls.clear()

    def test_infer_server_url(self) -> None:
        self.assertEqual(infer_server_url("http://127.0.0.1:8000/api/"), "http://127.0.0.1:8000")

    def test_crud_and_extra_api_methods(self) -> None:
        self.assertEqual(self.client.health(), {"status": "ok"})
        self.assertEqual(self.client.list_tasks()[0]["id"], 1)
        self.assertEqual(self.client.get_task(1)["text"], "one")
        self.assertEqual(self.client.create_task("  new task  ")["text"], "new task")
        self.assertEqual(self.client.edit_task(1, "edited")["text"], "edited")
        self.assertTrue(self.client.set_done(1, True)["done"])
        self.assertTrue(self.client.toggle_done(1)["done"])
        self.assertEqual(self.client.update_task(1, text="patched")["text"], "patched")
        self.client.delete_task(1)

        methods = [call[0] for call in FakeTodoHandler.calls]
        self.assertEqual(methods, ["GET", "GET", "GET", "POST", "GET", "PUT", "GET", "PUT", "GET", "PUT", "PATCH", "DELETE"])

    def test_client_validation(self) -> None:
        with self.assertRaisesRegex(TodoClientError, "不能是空白"):
            self.client.create_task("   ")
        with self.assertRaisesRegex(TodoClientError, "最多 200"):
            self.client.create_task("x" * 201)
        with self.assertRaisesRegex(TodoClientError, "至少要提供"):
            self.client.update_task(1)

    def test_api_error_detail(self) -> None:
        with self.assertRaises(TodoApiError) as context:
            self.client.get_task(999)
        self.assertEqual(context.exception.status, 404)
        self.assertEqual(str(context.exception), "not found")


if __name__ == "__main__":
    unittest.main()
