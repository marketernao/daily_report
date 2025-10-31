"""Command-line interface for generating and posting daily reports."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .formatter import DailyReport, generate_report
from .slack import SlackWebhookClient


def _prompt_multiline(prompt: str) -> str:
    print(f"{prompt} (finish with EOF / Ctrl-D):")
    buffer: list[str] = []
    try:
        for line in sys.stdin:
            buffer.append(line.rstrip("\n"))
    except KeyboardInterrupt:  # pragma: no cover - for interactive convenience
        pass
    return "\n".join(buffer).strip()


def _load_value(value: Optional[str], label: str) -> str:
    if value is None:
        return _prompt_multiline(label)
    path = Path(value)
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    return value


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Markdown daily reports.")
    parser.add_argument("--activities", "-a", help="Activities block text or file path.")
    parser.add_argument("--learnings", "-l", help="Learnings block text or file path.")
    parser.add_argument("--todos", "-t", help="Tomorrow's TODO block text or file path.")
    parser.add_argument("--date", help="Report date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--post", action="store_true", help="Post the report to Slack.")
    parser.add_argument("--webhook-url", help="Slack incoming webhook URL.")
    parser.add_argument(
        "--json", action="store_true", help="Output JSON with Markdown and metadata."
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    args = _parse_args(argv or sys.argv[1:])

    if args.date:
        try:
            report_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:  # pragma: no cover - defensive branch
            raise SystemExit("Invalid date format; use YYYY-MM-DD") from exc
    else:
        report_date = datetime.now(timezone.utc).astimezone().date()

    activities_text = _load_value(args.activities, "作業内容を入力してください")
    learnings_text = _load_value(args.learnings, "気づきを入力してください")
    todos_text = _load_value(args.todos, "明日のTODOを入力してください")

    report: DailyReport = generate_report(
        activities_text, learnings_text, todos_text, report_date
    )
    markdown = report.to_markdown()

    if args.json:
        payload = {
            "date": report.report_date.isoformat(),
            "activities": report.activities,
            "learnings": report.learnings,
            "todos": report.todos,
            "markdown": markdown,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(markdown)

    if args.post:
        client = SlackWebhookClient.from_env_or_value(args.webhook_url)
        client.post_markdown(markdown)
        print("✅ Slackへ送信しました。")


if __name__ == "__main__":  # pragma: no cover - entry point guard
    main()
