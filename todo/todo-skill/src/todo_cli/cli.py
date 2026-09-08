"""Command-line interface for the local Todo API."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence
from typing import Any

from .client import (
    DEFAULT_API_BASE_URL,
    DEFAULT_TIMEOUT,
    TodoClient,
    TodoClientError,
    TodoApiError,
)


ENV_API_BASE_URL = "TODO_API_BASE_URL"
ENV_SERVER_URL = "TODO_SERVER_URL"


def _task_id(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("task_id 必須是整數。") from error
    if parsed < 1:
        raise argparse.ArgumentTypeError("task_id 必須是正整數。")
    return parsed


def _add_common_options(parser: argparse.ArgumentParser, *, root: bool = False) -> None:
    suppress = argparse.SUPPRESS if not root else None
    parser.add_argument(
        "--base-url",
        default=(os.getenv(ENV_API_BASE_URL, DEFAULT_API_BASE_URL) if root else suppress),
        help=f"API base URL（預設：${ENV_API_BASE_URL} 或 {DEFAULT_API_BASE_URL}）",
    )
    parser.add_argument(
        "--server-url",
        default=(os.getenv(ENV_SERVER_URL) if root else suppress),
        help=f"服務根網址（預設由 --base-url 推導，也可用 ${ENV_SERVER_URL}）",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=(DEFAULT_TIMEOUT if root else suppress),
        help=f"HTTP timeout 秒數（預設：{DEFAULT_TIMEOUT:g}）",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=(False if root else suppress),
        help="以 JSON 輸出結果",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo-cli",
        description="以 CLI 操作 localhost Todo API。",
    )
    _add_common_options(parser, root=True)
    subparsers = parser.add_subparsers(dest="command", required=True)

    def command(name: str, help_text: str) -> argparse.ArgumentParser:
        child = subparsers.add_parser(name, help=help_text)
        _add_common_options(child)
        return child

    command("health", "檢查 Todo API 健康狀態。").set_defaults(handler="health")
    command("list", "列出所有任務。").set_defaults(handler="list")

    get_parser = command("get", "讀取單一任務。")
    get_parser.add_argument("task_id", type=_task_id)
    get_parser.set_defaults(handler="get")

    add_parser = command("add", "新增任務。")
    add_parser.add_argument("text", nargs="+", help="任務內容")
    add_parser.set_defaults(handler="add")

    edit_parser = command("edit", "依照網站的完整替換流程編輯任務文字。")
    edit_parser.add_argument("task_id", type=_task_id)
    edit_parser.add_argument("text", nargs="+", help="新的任務內容")
    edit_parser.set_defaults(handler="edit")

    complete_parser = command("complete", "標記任務為完成。")
    complete_parser.add_argument("task_id", type=_task_id)
    complete_parser.set_defaults(handler="complete")

    uncomplete_parser = command("uncomplete", "標記任務為未完成。")
    uncomplete_parser.add_argument("task_id", type=_task_id)
    uncomplete_parser.set_defaults(handler="uncomplete")

    toggle_parser = command("toggle", "切換任務完成狀態。")
    toggle_parser.add_argument("task_id", type=_task_id)
    toggle_parser.set_defaults(handler="toggle")

    update_parser = command("update", "使用 API 的 PATCH 部分更新任務。")
    update_parser.add_argument("task_id", type=_task_id)
    update_parser.add_argument("--text", help="新的任務內容")
    state_group = update_parser.add_mutually_exclusive_group()
    state_group.add_argument("--done", dest="done", action="store_const", const=True, help="標記完成")
    state_group.add_argument("--pending", dest="done", action="store_const", const=False, help="標記未完成")
    update_parser.set_defaults(handler="update", done=None)

    delete_parser = command("delete", "刪除任務。")
    delete_parser.add_argument("task_id", type=_task_id)
    delete_parser.add_argument("--yes", action="store_true", help="跳過確認提示")
    delete_parser.set_defaults(handler="delete")

    # Keep the command list order readable in --help output.
    return parser


def _join_words(words: list[str]) -> str:
    return " ".join(words)


def _json_print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _human_task(task: dict[str, Any]) -> str:
    marker = "[x]" if task.get("done") else "[ ]"
    return f"#{task.get('id')} {marker} {task.get('text', '')}"


def _print_result(value: Any, args: argparse.Namespace, *, message: str | None = None) -> None:
    if args.json_output:
        _json_print(value)
    elif message is not None:
        print(message)
    elif isinstance(value, list):
        if not value:
            print("目前沒有任務。")
        else:
            for task in value:
                print(_human_task(task))
    elif isinstance(value, dict) and {"id", "text", "done"}.issubset(value):
        print(_human_task(value))
    else:
        print(value)


def _confirm_delete(task_id: int) -> None:
    if not sys.stdin.isatty():
        raise TodoClientError("非互動模式拒絕刪除；若確定要刪除，請加上 --yes。")
    try:
        answer = input(f"確定刪除任務 #{task_id}？[y/N] ")
    except EOFError as error:
        raise TodoClientError("無法取得刪除確認；請加上 --yes。") from error
    if answer.strip().lower() not in {"y", "yes"}:
        raise TodoClientError("已取消刪除。")


def run(args: argparse.Namespace) -> int:
    client = TodoClient(
        base_url=args.base_url,
        server_url=args.server_url,
        timeout=args.timeout,
    )
    handler = args.handler

    if handler == "health":
        result = client.health()
        _print_result(result, args, message=str(result.get("status", "ok")))
    elif handler == "list":
        _print_result(client.list_tasks(), args)
    elif handler == "get":
        task = client.get_task(args.task_id)
        _print_result(task, args)
    elif handler == "add":
        task = client.create_task(_join_words(args.text))
        _print_result(task, args, message=f"已新增 {_human_task(task)}")
    elif handler == "edit":
        task = client.edit_task(args.task_id, _join_words(args.text))
        _print_result(task, args, message=f"已編輯 {_human_task(task)}")
    elif handler == "complete":
        task = client.set_done(args.task_id, True)
        _print_result(task, args, message=f"已完成 {_human_task(task)}")
    elif handler == "uncomplete":
        task = client.set_done(args.task_id, False)
        _print_result(task, args, message=f"已標記未完成 {_human_task(task)}")
    elif handler == "toggle":
        task = client.toggle_done(args.task_id)
        _print_result(task, args, message=f"已切換 {_human_task(task)}")
    elif handler == "update":
        task = client.update_task(args.task_id, text=args.text, done=args.done)
        _print_result(task, args, message=f"已更新 {_human_task(task)}")
    elif handler == "delete":
        if not args.yes:
            _confirm_delete(args.task_id)
        client.delete_task(args.task_id)
        result = {"deleted": args.task_id}
        _print_result(result, args, message=f"已刪除任務 #{args.task_id}")
    else:  # pragma: no cover - argparse always sets a known handler.
        raise TodoClientError(f"未知命令：{handler}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except (TodoApiError, TodoClientError) as error:
        if getattr(args, "json_output", False):
            payload: dict[str, Any] = {"error": str(error)}
            if isinstance(error, TodoApiError) and error.status is not None:
                payload["status"] = error.status
            _json_print(payload)
        else:
            print(f"錯誤：{error}", file=sys.stderr)
        return 1
