from __future__ import annotations

import unittest

from todo_cli.cli import build_parser


class CliParserTests(unittest.TestCase):
    def test_common_options_work_before_and_after_command(self) -> None:
        parser = build_parser()
        before = parser.parse_args(["--json", "--base-url", "http://example/api", "list"])
        after = parser.parse_args(["list", "--json", "--base-url", "http://example/api"])
        self.assertTrue(before.json_output)
        self.assertTrue(after.json_output)
        self.assertEqual(before.base_url, "http://example/api")
        self.assertEqual(after.base_url, "http://example/api")

    def test_update_requires_a_field_at_runtime(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["update", "1"])
        self.assertIsNone(args.done)
        self.assertIsNone(args.text)


if __name__ == "__main__":
    unittest.main()
